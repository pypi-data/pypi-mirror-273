"""VAST Database transaction.

A transcation is used as a context manager, since every Database-related operation in VAST requires a transaction.

    with session.transaction() as tx:
        tx.bucket("bucket").create_schema("schema")
"""

import logging
from dataclasses import dataclass
from typing import Optional

import botocore

from . import bucket, errors, schema, session, table

log = logging.getLogger(__name__)

TABULAR_BC_BUCKET = "vast-big-catalog-bucket"
VAST_CATALOG_SCHEMA_NAME = 'vast_big_catalog_schema'
VAST_CATALOG_TABLE_NAME = 'vast_big_catalog_table'

TABULAR_AUDERY_BUCKET = "vast-audit-log-bucket"
AUDERY_SCHEMA_NAME = 'vast_audit_log_schema'
AUDERY_TABLE_NAME = 'vast_audit_log_table'


@dataclass
class Transaction:
    """A holder of a single VAST transaction."""

    _rpc: "session.Session"
    txid: Optional[int] = None

    def __enter__(self):
        """Create a transaction and store its ID."""
        response = self._rpc.api.begin_transaction()
        self.txid = int(response.headers['tabular-txid'])
        log.debug("opened txid=%016x", self.txid)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """On success, the transaction is committed. Otherwise, it is rolled back."""
        txid = self.txid
        self.txid = None
        if (exc_type, exc_value, exc_traceback) == (None, None, None):
            log.debug("committing txid=%016x", txid)
            self._rpc.api.commit_transaction(txid)
        else:
            log.exception("rolling back txid=%016x due to:", txid)
            self._rpc.api.rollback_transaction(txid)

    def __repr__(self):
        """Don't show the session details."""
        if self.txid is None:
            return 'InvalidTransaction'
        return f'Transaction(id=0x{self.txid:016x})'

    def bucket(self, name: str) -> "bucket.Bucket":
        """Return a VAST Bucket, if exists."""
        try:
            self._rpc.s3.head_bucket(Bucket=name)
        except botocore.exceptions.ClientError as e:
            log.warning("res: %s", e.response)
            if e.response['Error']['Code'] == '404':
                raise errors.MissingBucket(name)
            raise
        return bucket.Bucket(name, self)

    def catalog(self, fail_if_missing=True) -> Optional["table.Table"]:
        """Return VAST Catalog table."""
        b = bucket.Bucket(TABULAR_BC_BUCKET, self)
        s = schema.Schema(VAST_CATALOG_SCHEMA_NAME, b)
        return s.table(name=VAST_CATALOG_TABLE_NAME, fail_if_missing=fail_if_missing)

    def audit_log(self, fail_if_missing=True) -> Optional["table.Table"]:
        """Return VAST AuditLog table."""
        b = bucket.Bucket(TABULAR_AUDERY_BUCKET, self)
        s = schema.Schema(AUDERY_SCHEMA_NAME, b)
        return s.table(name=AUDERY_TABLE_NAME, fail_if_missing=fail_if_missing)
