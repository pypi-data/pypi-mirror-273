from __future__ import annotations
import getpass
import logging
import time

from typing import Iterable, List, Optional
from contextlib import contextmanager
import datetime as dt
from datetime import datetime, timedelta

from tenacity import retry, TryAgain
from tenacity.wait import wait_fixed
from tenacity.stop import stop_after_delay

from exasol.saas.client import (
    openapi,
    Limits,
)
from exasol.saas.client.openapi.models.status import Status
from exasol.saas.client.openapi.api.databases import (
    create_database,
    delete_database,
    list_databases,
    get_database,
)
from exasol.saas.client.openapi.api.clusters import (
    get_cluster_connection,
    list_clusters,
)
from exasol.saas.client.openapi.api.security import (
    list_allowed_i_ps,
    add_allowed_ip,
    delete_allowed_ip,
)


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def timestamp_name(project_short_tag: str | None = None) -> str:
    """
    project_short_tag: Abbreviation of your project
    """
    timestamp = f'{datetime.now().timestamp():.0f}'
    owner = getpass.getuser()
    candidate = f"{timestamp}{project_short_tag or ''}-{owner}"
    return candidate[:Limits.MAX_DATABASE_NAME_LENGTH]


def wait_for_delete_clearance(start: dt.datetime):
    lifetime = datetime.now() - start
    if lifetime < Limits.MIN_DATABASE_LIFETIME:
        wait = Limits.MIN_DATABASE_LIFETIME - lifetime
        LOG.info(f"Waiting {int(wait.seconds)} seconds"
                 " before deleting the database.")
        time.sleep(wait.seconds)


class DatabaseStartupFailure(Exception):
    """
    If a SaaS database instance during startup reports a status other than
    successful.
    """


def create_saas_client(
        host: str,
        pat: str,
        raise_on_unexpected_status: bool = True,
) -> openapi.AuthenticatedClient:
    return openapi.AuthenticatedClient(
        base_url=host,
        token=pat,
        raise_on_unexpected_status = raise_on_unexpected_status,
    )


class OpenApiAccess:
    """
    This class is meant to be used only in the context of the API
    generator repository while integration tests in other repositories are
    planned to only use fixture ``saas_database_id()``.
    """

    def __init__(self, client: openapi.AuthenticatedClient, account_id: str):
        self._client = client
        self._account_id = account_id

    def create_database(
            self,
            name: str,
            cluster_size: str = "XS",
            region: str = "eu-central-1",
    ) -> Optional[openapi.models.Database]:
        def minutes(x: timedelta) -> int:
            return x.seconds // 60

        cluster_spec = openapi.models.CreateDatabaseInitialCluster(
            name="my-cluster",
            size=cluster_size,
            auto_stop=openapi.models.AutoStop(
                enabled=True,
                idle_time=minutes(Limits.AUTOSTOP_MIN_IDLE_TIME),
            ),
        )
        LOG.info(f"Creating database {name}")
        return create_database.sync(
            self._account_id,
            client=self._client,
            body=openapi.models.CreateDatabase(
                name=name,
                initial_cluster=cluster_spec,
                provider="aws",
                region=region,
            )
        )

    @contextmanager
    def _ignore_failures(self, ignore: bool = False):
        before = self._client.raise_on_unexpected_status
        self._client.raise_on_unexpected_status = not ignore
        yield self._client
        self._client.raise_on_unexpected_status = before

    def delete_database(self, database_id: str, ignore_failures=False):
        with self._ignore_failures(ignore_failures) as client:
            return delete_database.sync_detailed(
                self._account_id, database_id, client=client)

    def list_database_ids(self) -> Iterable[str]:
        dbs = list_databases.sync(self._account_id, client=self._client) or []
        return (db.id for db in dbs)

    @contextmanager
    def database(
            self,
            name: str,
            keep: bool = False,
            ignore_delete_failure: bool = False,
    ):
        db = None
        start = datetime.now()
        try:
            db = self.create_database(name)
            yield db
            wait_for_delete_clearance(start)
        finally:
            db_repr = f"{db.name} with ID {db.id}" if db else None
            if db and not keep:
                LOG.info(f"Deleting database {db_repr}")
                response = self.delete_database(db.id, ignore_delete_failure)
                if response.status_code == 200:
                    LOG.info(f"Successfully deleted database {db_repr}.")
                else:
                    LOG.warning(f"Ignoring status code {response.status_code}.")
            elif not db:
                LOG.warning("Cannot delete db None")
            else:
                LOG.info(f"Keeping database {db_repr} as keep = {keep}")

    def get_database(
            self,
            database_id: str,
    ) -> Optional[openapi.models.database.Database]:
        return get_database.sync(
            self._account_id,
            database_id,
            client=self._client,
        )

    def wait_until_running(
            self,
            database_id: str,
            timeout: timedelta = timedelta(minutes=30),
            interval: timedelta = timedelta(minutes=2),
    ):
        success = [
            Status.RUNNING,
        ]

        @retry(wait=wait_fixed(interval), stop=stop_after_delay(timeout))
        def poll_status():
            db = self.get_database(database_id)
            if db.status not in success:
                print(f'status = {db.status}')
                raise TryAgain
            return db.status

        if poll_status() not in success:
            raise DatabaseStartupFailure()


    def clusters(
            self,
            database_id: str,
    ) -> Optional[List[openapi.models.Cluster]]:
        return list_clusters.sync(
            self._account_id,
            database_id,
            client=self._client,
        )

    def get_connection(
            self,
            database_id: str,
            cluster_id: str,
    ) -> Optional[openapi.models.ClusterConnection]:
        return get_cluster_connection.sync(
            self._account_id,
            database_id,
            cluster_id,
            client=self._client,
        )

    def list_allowed_ip_ids(self) -> Iterable[str]:
        ips = list_allowed_i_ps.sync(
            self._account_id,
            client=self._client,
        ) or []
        return (x.id for x in ips)

    def add_allowed_ip(
            self,
            cidr_ip: str = "0.0.0.0/0",
    ) -> Optional[openapi.models.allowed_ip.AllowedIP]:
        """
        Suggested values for cidr_ip:
        * 185.17.207.78/32
        * 0.0.0.0/0 = all ipv4
        * ::/0 = all ipv6
        """
        rule = openapi.models.CreateAllowedIP(
            name=timestamp_name(),
            cidr_ip=cidr_ip,
        )
        return add_allowed_ip.sync(
            self._account_id,
            client=self._client,
            body=rule,
        )

    def delete_allowed_ip(self, id: str, ignore_failures=False):
        with self._ignore_failures(ignore_failures) as client:
            return delete_allowed_ip.sync_detailed(
                self._account_id, id, client=client)

    @contextmanager
    def allowed_ip(
            self,
            cidr_ip: str = "0.0.0.0/0",
            keep: bool = False,
            ignore_delete_failure: bool = False,
    ):
        ip = None
        try:
            ip = self.add_allowed_ip(cidr_ip)
            yield ip
        finally:
            if ip and not keep:
                self.delete_allowed_ip(ip.id, ignore_delete_failure)
