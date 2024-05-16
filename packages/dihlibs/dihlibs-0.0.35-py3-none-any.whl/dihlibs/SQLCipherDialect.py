from sqlcipher3 import dbapi2 as sqlcipher
from sqlalchemy.dialects.sqlite.base import SQLiteDialect
from sqlalchemy.engine.url import make_url
import sqlcipher3
from sqlalchemy.dialects.sqlite.base import SQLiteDialect
import sqlcipher3.dbapi2 as sqlcipher


class SQLCipherDialect(SQLiteDialect):
    name = "sqlcipher"
    driver = "sqlcipher"
    paramstyle = "qmark"
    supports_statement_cache = True
    key = None
    from sqlcipher3.dbapi2 import Error, DatabaseError, OperationalError, IntegrityError

    @classmethod
    def dbapi(cls):
        return sqlcipher

    def create_connect_args(self, url):
        parsed_url = make_url(url)
        self.key = parsed_url.query.get("key", None)
        opts = url.translate_connect_args()
        opts.pop("key", None)
        return [[], opts]

    def connect(self, *cargs, **cparams):
        dbapi_con = super().connect(*cargs, **cparams)
        if self.key:
            dbapi_con.execute(f"PRAGMA key='{self.key}'")
        return dbapi_con
