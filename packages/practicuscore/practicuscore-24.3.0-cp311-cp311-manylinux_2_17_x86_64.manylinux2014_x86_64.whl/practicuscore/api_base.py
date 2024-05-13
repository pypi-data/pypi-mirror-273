import os.path
import sys
from abc import ABC
import platform
from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import List, Optional, Union, cast, Type, Tuple

import dataclasses_json

from practicuscore.core_def import PRTEng, PRTConn, CoreDef, OPResult


class PrtDataClassJsonMixin(dataclasses_json.DataClassJsonMixin):
    dataclass_json_config = dataclasses_json.config(  # type: ignore
        undefined=dataclasses_json.Undefined.EXCLUDE,
        exclude=lambda f: f is None  # type: ignore
    )["dataclasses_json"]


class PRTValidator(ABC):
    @staticmethod
    def validate(dataclass_obj) -> Tuple[Optional[str], Optional[str]]:
        """
        Validates all fields on a dataclass, *if only* it has "validators" metadata.
        "validators" can be a single tuple (lambda_func, "err message") OR a list of validation tuples
           i.e. use a single validator:
            some_field: int = field(
                metadata={
                    "validators": (lambda x: x > 0, "Must be > 0")
                })
           OR multiple validators:
            some_field: int = field(
                metadata={
                    "validators": [(lambda x: x > 0, "Must be > 0"),
                                   (lambda x: x < 10, "Must be < 10")]
                })
        :param dataclass_obj: The dataclass object to validate. Must have validators defined
        :return: if a field has errors, (field name, error message) tuple. Or (None, None)
        """
        for fld in fields(dataclass_obj):
            if "validators" in fld.metadata:
                validator_or_validators = fld.metadata["validators"]

                if isinstance(validator_or_validators, tuple):
                    validators = [validator_or_validators]
                else:
                    validators = validator_or_validators
                for validator_tuple in validators:
                    assert isinstance(validator_tuple, tuple), \
                        "Validator must be a tuple in the form of (validator_lambda, 'error message')"
                    validator_func, validator_err_msg = validator_tuple
                    field_val = getattr(dataclass_obj, fld.name)
                    try:
                        failed = False
                        if not validator_func(field_val):
                            failed = True
                    except Exception as ex:
                        failed = True
                        validator_err_msg = f"Exception occurred while checking for '{validator_err_msg}', " \
                                            f"\nException: {ex}"

                    if failed:
                        return fld.name, validator_err_msg  # return info about *first* encountered issue

        return None, None  # no issues, nothing to return


@dataclass
class RequestMeta(PrtDataClassJsonMixin):
    meta_type: str = "Request"
    meta_name: str = ""
    req_time: Optional[datetime] = None
    req_core_v: str = CoreDef.CORE_VERSION
    req_os: str = platform.system()
    req_os_v: str = platform.release()
    req_py_minor_v: int = sys.version_info.minor


@dataclass
class PRTRequest(PrtDataClassJsonMixin):
    # Creating a meta class here caused a nasty bug. meta became a shared object between child classes
    #   i.e. when __post_init() below updated meta_name for one type of Request class, al others got the new name
    # meta: RequestMeta = RequestMeta()
    meta: Optional[RequestMeta] = None

    @property
    def name(self) -> str:
        assert self.meta is not None
        return self.meta.meta_name

    def __post_init__(self):
        self.meta = RequestMeta()
        self.meta.meta_name = self.__class__.__name__.rsplit("Request", 1)[0]
        # do not assign defaults in class definition. Gets assigned static one time
        self.meta.req_time = datetime.utcnow()


@dataclass
class ResponseMeta(PrtDataClassJsonMixin):
    meta_type: str = "Response"
    meta_name: str = ""
    resp_node_v: str = ""  # assigned later right before sending to client
    resp_py_minor_v: int = sys.version_info.minor


@dataclass
class PRTResponse(PrtDataClassJsonMixin):
    meta: Optional[ResponseMeta] = None
    op_result: Optional[OPResult] = None

    # meta: ResponseMeta = ResponseMeta()  Don't instantiate here. Read notes for PRTRequest

    @property
    def name(self) -> str:
        assert self.meta is not None
        return self.meta.meta_name

    def __post_init__(self):
        self.meta = ResponseMeta()
        self.meta.meta_name = self.__class__.__name__.rsplit("Response", 1)[0]
        # do not assign defaults in class definition. Gets assigned static one time
        self.meta.req_time = datetime.utcnow()


@dataclass
class EmptyResponse(PRTResponse):
    # used when there's an error, no response can be created and we hae op_result send back
    pass


# Connection configuration classes

@dataclass
class UIMap(PrtDataClassJsonMixin):
    # Helps map an individual ConnConf field to a single GUI element.
    # i.e. MYSQL related field "db_host" should be visible as "Database Host Address", it is required, ...
    visible_name: Optional[str] = None
    auto_display: bool = True  # some fields are displayed manually and not automated
    tip: Optional[str] = None
    default_value: Optional[str] = None
    is_required: bool = True
    is_password: bool = False


@dataclass
class ConnConf(PrtDataClassJsonMixin):
    connection_type: Optional[PRTConn] = None
    is_enriched: Optional[bool] = None
    uuid: Optional[str] = None
    ws_uuid: Optional[str] = None
    ws_name: Optional[str] = None
    sampling_method: Optional[str] = None
    sample_size: Optional[int] = None
    sample_size_app: Optional[int] = None
    column_list: Optional[List[str]] = None
    filter: Optional[str] = None

    def __str__(self):
        return str(self.to_json())

    def __repr__(self):
        return str(self)

    @property
    def enriched(self) -> bool:
        return bool(self.is_enriched) if self.is_enriched is not None else False

    @property
    def conn_type(self) -> PRTConn:
        assert self.connection_type is not None
        return self.connection_type

    @property
    def friendly_desc(self) -> str:
        # override with children class for a better user-friendly
        return str(self.connection_type)

    @property
    def friendly_long_desc(self) -> str:
        return self.friendly_desc

    def copy_secure(self) -> 'ConnConf':
        import copy
        return copy.copy(self)

    def copy_with_credentials(self, credentials: Optional[dict] = None) -> 'ConnConf':
        return self.copy_secure()

    def apply_conf_to(self, other: 'ConnConf'):
        self._apply_conf_to(other)
        self.is_enriched = True

    def _apply_conf_to(self, other: 'ConnConf'):
        pass

    def internal_equals(self, other: 'ConnConf') -> bool:
        pass

    def __eq__(self, other: 'ConnConf') -> bool:
        if not isinstance(other, ConnConf):
            return False
        other = cast(ConnConf, other)
        equals = (self.conn_type == other.conn_type
                  and self.sample_size == other.sample_size
                  and self.sample_size_app == other.sample_size_app
                  and self.column_list == other.column_list
                  and self.filter == other.filter)
        if not equals:
            return False
        return self.internal_equals(other)


@dataclass
class InMemoryConnConf(ConnConf):
    connection_type: PRTConn = PRTConn.IN_MEMORY
    df: Optional[object] = None

    def __repr__(self):
        return str(self)

    @property
    def friendly_desc(self) -> str:
        return "In memory dataframe"

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, InMemoryConnConf):
            return False
        other = cast(InMemoryConnConf, other)
        return self.df.__eq__(other.df)


@dataclass
class LocalFileConnConf(ConnConf):
    connection_type: PRTConn = PRTConn.LOCAL_FILE
    file_path: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="File Path",
                        tip="Type path on local disk")
    })

    def __repr__(self):
        return str(self)

    @property
    def friendly_desc(self) -> str:
        try:
            if self.file_path:
                return os.path.splitext(os.path.basename(self.file_path))[0]
        except:
            pass

        return self.conn_type.lower()

    @property
    def friendly_long_desc(self) -> str:
        final_desc = self.file_path
        if final_desc and len(final_desc) > 30:
            final_desc = f"{final_desc[:15]} ... {final_desc[-10:]}"
        return final_desc if final_desc else "?"

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, LocalFileConnConf):
            return False
        other = cast(LocalFileConnConf, other)
        return self.file_path == other.file_path

    @property
    def is_prt_file(self) -> bool:
        if self.file_path:
            return self.file_path.endswith(CoreDef.APP_FILE_TYPE)
        return False


@dataclass
class WorkerFileConnConf(ConnConf):
    connection_type: PRTConn = PRTConn.WORKER_FILE
    file_path: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="File Path",
                        tip="Type path on Worker local disk. E.g. /home/ubuntu/data/file.csv")
    })

    def __repr__(self):
        return str(self)

    @property
    def friendly_desc(self) -> str:
        try:
            if self.file_path:
                return os.path.splitext(os.path.basename(self.file_path))[0]
        except:
            pass

        return self.conn_type.lower()

    @property
    def friendly_long_desc(self) -> str:
        final_desc = self.file_path
        if final_desc and len(final_desc) > 30:
            final_desc = f"{final_desc[:15]} ... {final_desc[-10:]}"
        return final_desc if final_desc else "?"

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, WorkerFileConnConf):
            return False
        other = cast(WorkerFileConnConf, other)
        return self.file_path == other.file_path

    @property
    def is_prt_file(self) -> bool:
        if self.file_path:
            return self.file_path.endswith(CoreDef.APP_FILE_TYPE)
        return False


@dataclass
class S3ConnConf(ConnConf):
    connection_type: PRTConn = PRTConn.S3
    aws_region: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None
    endpoint_url: Optional[str] = None
    s3_bucket: Optional[str] = None
    s3_keys: Optional[List[str]] = None
    default_prefix: Optional[str] = None

    def __repr__(self):
        return str(self)

    @property
    def friendly_desc(self) -> str:
        try:
            if self.s3_keys:
                if len(self.s3_keys) >= 1:
                    s3_key = self.s3_keys[0]
                    if s3_key.find(".") > -1:
                        return os.path.splitext(os.path.basename(s3_key))[0]
                    else:
                        return os.path.basename(os.path.normpath(s3_key))
        except:
            pass
        return self.conn_type.lower()

    @property
    def friendly_long_desc(self) -> str:
        if self.s3_bucket:
            bucket_desc = f"s3://{self.s3_bucket}"
        else:
            # k8s currently send no bucket name..
            bucket_desc = f"s3://_bucket_"
        keys_desc = "?"
        if self.s3_keys:
            if len(self.s3_keys) == 1:
                keys_desc = self.s3_keys[0]
            else:
                keys_desc = f"{self.s3_keys[0]} .."

        final_desc = f"{bucket_desc}/{keys_desc}"
        if len(final_desc) > 30:
            final_desc = f"{final_desc[:15]} ... {final_desc[-10:]}"
        return final_desc

    def copy_secure(self) -> ConnConf:
        copy_conn_conf = super().copy_secure()
        assert isinstance(copy_conn_conf, S3ConnConf)
        copy_conn_conf = cast(S3ConnConf, copy_conn_conf)
        copy_conn_conf.aws_access_key_id = None
        copy_conn_conf.aws_secret_access_key = None
        copy_conn_conf.aws_session_token = None
        return copy_conn_conf

    def copy_with_credentials(self, credentials: Optional[dict] = None) -> ConnConf:
        copy_conn_conf = super().copy_secure()
        copy_conn_conf = cast(S3ConnConf, copy_conn_conf)
        if credentials is not None:
            if "aws_access_key_id" in credentials:
                copy_conn_conf.aws_access_key_id = str(credentials["aws_access_key_id"])
            if "aws_secret_access_key" in credentials:
                copy_conn_conf.aws_secret_access_key = str(credentials["aws_secret_access_key"])
            if "aws_session_token" in credentials:
                copy_conn_conf.aws_session_token = str(credentials["aws_session_token"])
        return copy_conn_conf

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, S3ConnConf):
            return False
        other = cast(S3ConnConf, other)
        return self.aws_region == other.aws_region \
            and self.aws_access_key_id == other.aws_access_key_id \
            and self.aws_secret_access_key == other.aws_secret_access_key \
            and self.aws_session_token == other.aws_session_token \
            and self.s3_bucket == other.s3_bucket \
            and self.s3_keys == other.s3_keys

    def _apply_conf_to(self, other: 'ConnConf'):
        assert isinstance(other, S3ConnConf), "apply credentials failed. other must be S3ConnConf"
        other = cast(S3ConnConf, other)
        other.aws_region = self.aws_region
        other.aws_access_key_id = self.aws_access_key_id
        other.aws_secret_access_key = self.aws_secret_access_key
        other.s3_bucket = self.s3_bucket
        other.endpoint_url = self.endpoint_url


@dataclass
class RelationalConnConf(ConnConf):
    sql_query: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="SQL Query",
                        auto_display=False),
        "validators": (lambda x: x and len(x) > 0, "No SQL query provided")
    })

    target_table_name: Optional[str] = None
    target_schema: Optional[str] = None
    target_table_if_exists: Optional[str] = None
    chunk_size: Optional[int] = None
    prefer_db_api: Optional[bool] = None

    def __repr__(self):
        return str(self)

    def _find_table_name(self, keyword: str) -> Optional[str]:
        if self.sql_query:
            table_ind = self.sql_query.lower().find(f"{keyword} ") + len(f"{keyword} ")
            if table_ind > -1:
                desc = self.sql_query[table_ind:].strip().lower()
                next_stop = desc.find(" ")
                if next_stop > -1:
                    desc = desc[:next_stop]
                next_stop = desc.find(",")
                if next_stop > -1:
                    desc = desc[:next_stop]
                next_stop = desc.find("\n")
                if next_stop > -1:
                    desc = desc[:next_stop]

                desc = desc.strip()
                if desc:
                    return desc
        return None

    @property
    def friendly_desc(self) -> str:
        try:
            table_name = self._find_table_name("from")
            if not table_name:
                table_name = self._find_table_name("into")

            if table_name:
                return table_name

            if self.sql_query:
                return self.sql_query[:10] + f"{'..' if len(self.sql_query) > 10 else ''}"
        except:
            pass
        assert self.connection_type is not None
        return self.connection_type.lower()

    @property
    def friendly_long_desc(self) -> str:
        assert self.connection_type is not None
        table_name: Optional[str]
        if self.target_table_name:
            table_name = self.target_table_name
            if self.target_schema:
                table_name = f"{self.target_schema}.{table_name}"
            return f"{self.connection_type.capitalize()} table: {table_name}"
        else:
            table_name = self._find_table_name("from")
            if not table_name:
                table_name = self._find_table_name("into")

            if self.target_schema and table_name:
                table_name = f"{self.target_schema}.{table_name}"

            desc = ""
            if table_name:
                desc = f": {table_name}"
            elif self.sql_query:
                desc += f": {self.sql_query[:20]}{'...' if len(self.sql_query) > 20 else ''}"
            desc = desc.replace("\n", " ")
            final_desc = f"{self.connection_type.capitalize()}{desc}"
            if len(final_desc) > 30:
                final_desc = f"{final_desc[:15]} ... {final_desc[-10:]}"
            return final_desc

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, RelationalConnConf):
            return False
        other = cast(RelationalConnConf, other)
        return self.sql_query == other.sql_query and self.target_table_name == other.target_table_name


@dataclass
class SqLiteConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.SQLITE
    file_path: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="File Path",
                        tip="Type path on Worker local disk. E.g. /home/ubuntu/data/database.db",
                        default_value=CoreDef.NODE_HOME_PATH + "/samples/chinook.db"),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, SqLiteConnConf):
            return False
        other = cast(SqLiteConnConf, other)
        return self.file_path == other.file_path

    def _apply_conf_to(self, other: 'ConnConf'):
        assert isinstance(other, SqLiteConnConf), "apply credentials failed. other must be SqLiteConnConf"
        other = cast(SqLiteConnConf, other)
        other.file_path = self.file_path


@dataclass
class MYSQLConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.MYSQL
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="3306"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, MYSQLConnConf):
            return False
        other = cast(MYSQLConnConf, other)
        return self.db_host == other.db_host \
            and self.db_name == other.db_name \
            and self.db_port == other.db_port \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'MYSQLConnConf'):
        assert isinstance(other, MYSQLConnConf), "apply credentials failed. other must be MYSQLConnConf"
        other = cast(MYSQLConnConf, other)
        other.db_host = self.db_host
        other.db_name = self.db_name
        other.db_port = self.db_port
        other.user = self.user
        other.password = self.password


@dataclass
class PostgreSQLConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.POSTGRESQL
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="5432"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, PostgreSQLConnConf):
            return False
        other = cast(PostgreSQLConnConf, other)
        return self.db_host == other.db_host \
            and self.db_name == other.db_name \
            and self.db_port == other.db_port \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'PostgreSQLConnConf'):
        assert isinstance(other, PostgreSQLConnConf), "apply credentials failed. other must be PostgreSQLConnConf"
        other = cast(PostgreSQLConnConf, other)
        other.db_host = self.db_host
        other.db_name = self.db_name
        other.db_port = self.db_port
        other.user = self.user
        other.password = self.password


@dataclass
class RedshiftConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.REDSHIFT
    # redshift_db_address: Optional[str] = None  # dummy
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="5439"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, RedshiftConnConf):
            return False
        other = cast(RedshiftConnConf, other)
        return self.db_host == other.db_host \
            and self.db_name == other.db_name \
            and self.db_port == other.db_port \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'RedshiftConnConf'):
        assert isinstance(other, RedshiftConnConf), "apply credentials failed. other must be RedshiftConnConf"
        other = cast(RedshiftConnConf, other)
        other.db_host = self.db_host
        other.db_name = self.db_name
        other.db_port = self.db_port
        other.user = self.user
        other.password = self.password


@dataclass
class SnowflakeConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.SNOWFLAKE
    db_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_schema: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Schema",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    warehouse_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Warehouse Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    role: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Role",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    account: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Account Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        ),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, SnowflakeConnConf):
            return False
        other = cast(SnowflakeConnConf, other)
        return self.db_name == other.db_name \
            and self.db_schema == other.db_schema \
            and self.warehouse_name == other.warehouse_name \
            and self.user == other.user \
            and self.role == other.role \
            and self.account == other.account \
            and self.password == other.password

    def _apply_conf_to(self, other: 'SnowflakeConnConf'):
        assert isinstance(other, SnowflakeConnConf), "apply credentials failed. other must be SnowflakeConnConf"
        other = cast(SnowflakeConnConf, other)
        other.db_name = self.db_name
        other.db_schema = self.db_schema
        other.warehouse_name = self.warehouse_name
        other.user = self.user
        other.role = self.role
        other.account = self.account
        other.password = self.password


@dataclass
class MSSQLConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.MSSQL
    # redshift_db_address: Optional[str] = None  # dummy
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    # driver: Optional[str] = field(default=None, metadata={
    #     "ui_map": UIMap(visible_name="Driver Name",
    #                     default_value="SQL Server Native Client 10.0"),
    #     "validators": (lambda x: x and len(x) > 0, "No value provided")
    # })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="1433"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, MSSQLConnConf):
            return False
        other = cast(MSSQLConnConf, other)
        return self.db_host == other.db_host \
            and self.db_name == other.db_name \
            and self.db_port == other.db_port \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'MSSQLConnConf'):
        assert isinstance(other, MSSQLConnConf), "apply credentials failed. other must be MSSQLConnConf"
        other = cast(MSSQLConnConf, other)
        other.db_host = self.db_host
        other.db_name = self.db_name
        other.db_port = self.db_port
        other.user = self.user
        other.password = self.password


@dataclass
class OracleConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.ORACLE
    # redshift_db_address: Optional[str] = None  # dummy
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    service_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Service Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    sid: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Sid",
                        is_required=False,
                        default_value="")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="1521"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, OracleConnConf):
            return False
        other = cast(OracleConnConf, other)
        return self.db_host == other.db_host \
            and self.service_name == other.service_name \
            and self.sid == other.sid \
            and self.db_port == other.db_port \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'OracleConnConf'):
        assert isinstance(other, OracleConnConf), "apply credentials failed. other must be OracleConnConf"
        other = cast(OracleConnConf, other)
        other.db_host = self.db_host
        other.service_name = self.service_name
        other.sid = self.sid
        other.db_port = self.db_port
        other.user = self.user
        other.password = self.password


@dataclass
class HiveConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.HIVE
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="10000"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, HiveConnConf):
            return False
        other = cast(HiveConnConf, other)
        return self.db_host == other.db_host \
            and self.db_name == other.db_name \
            and self.db_port == other.db_port \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'HiveConnConf'):
        assert isinstance(other, HiveConnConf), "apply credentials failed. other must be HiveConnConf"
        other = cast(HiveConnConf, other)
        other.db_host = self.db_host
        other.db_name = self.db_name
        other.db_port = self.db_port
        other.user = self.user
        other.password = self.password


@dataclass
class ClouderaConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.CLOUDERA
    host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Cloudera Host",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="21050"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, ClouderaConnConf):
            return False
        other = cast(ClouderaConnConf, other)
        return self.host == other.host \
            and self.port == other.port \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'ClouderaConnConf'):
        assert isinstance(other, ClouderaConnConf), "apply credentials failed. other must be ClouderaConnConf"
        other = cast(ClouderaConnConf, other)
        other.host = self.host
        other.port = self.port
        other.user = self.user
        other.password = self.password


@dataclass
class AthenaConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.ATHENA
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    s3_dir: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="S3 Location",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="443"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    access_key: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="AWS Access key ID",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    secret_key: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="AWS Secret access key",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, AthenaConnConf):
            return False
        other = cast(AthenaConnConf, other)
        return self.db_host == other.db_host \
            and self.db_name == other.db_name \
            and self.s3_dir == other.s3_dir \
            and self.db_port == other.db_port \
            and self.access_key == other.access_key \
            and self.secret_key == other.secret_key

    def _apply_conf_to(self, other: 'AthenaConnConf'):
        assert isinstance(other, AthenaConnConf), "apply credentials failed. other must be AthenaConnConf"
        other = cast(AthenaConnConf, other)
        other.db_host = self.db_host
        other.db_name = self.db_name
        other.db_port = self.db_port
        other.s3_dir = self.s3_dir
        other.access_key = self.access_key
        other.secret_key = self.secret_key


@dataclass
class ElasticSearchConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.ELASTICSEARCH
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test-2.latest-elasticsearch.abc-3.xyz.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value=""),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, ElasticSearchConnConf):
            return False
        other = cast(ElasticSearchConnConf, other)
        return self.db_host == other.db_host \
            and self.db_port == other.db_port \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'ElasticSearchConnConf'):
        assert isinstance(other, ElasticSearchConnConf), "apply credentials failed. other must be ElasticSearchConnConf"
        other = cast(ElasticSearchConnConf, other)
        other.db_host = self.db_host
        other.db_port = self.db_port
        other.user = self.user
        other.password = self.password


@dataclass
class OpenSearchConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.OPENSEARCH
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. search-test-abcde.us-east-1.es.amazonaws.com",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="443"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, OpenSearchConnConf):
            return False
        other = cast(OpenSearchConnConf, other)
        return self.db_host == other.db_host \
            and self.db_port == other.db_port \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'OpenSearchConnConf'):
        assert isinstance(other, OpenSearchConnConf), "apply credentials failed. other must be OpenSearchConnConf"
        other = cast(OpenSearchConnConf, other)
        other.db_host = self.db_host
        other.db_port = self.db_port
        other.user = self.user
        other.password = self.password


@dataclass
class TrinoConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.TRINO
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. localhost",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="8080"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    catalog: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Catalog",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_schema: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Schema",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, TrinoConnConf):
            return False
        other = cast(TrinoConnConf, other)
        return self.db_host == other.db_host \
            and self.db_port == other.db_port \
            and self.catalog == other.catalog \
            and self.db_schema == other.db_schema \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'TrinoConnConf'):
        assert isinstance(other, TrinoConnConf), "apply credentials failed. other must be TrinoConnConf"
        other = cast(TrinoConnConf, other)
        other.db_host = self.db_host
        other.db_port = self.db_port
        other.catalog = self.catalog
        other.db_schema = self.db_schema
        other.user = self.user
        other.password = self.password


@dataclass
class DremioConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.DREMIO
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. localhost",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="31010"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, DremioConnConf):
            return False
        other = cast(TrinoConnConf, other)
        return self.db_host == other.db_host \
            and self.db_port == other.db_port \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'DremioConnConf'):
        assert isinstance(other, DremioConnConf), "apply credentials failed. other must be DremioConnConf"
        other = cast(DremioConnConf, other)
        other.db_host = self.db_host
        other.db_port = self.db_port
        other.user = self.user
        other.password = self.password


@dataclass
class HanaConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.HANA
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="39015"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    db_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        is_required=False,
                        default_value="")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, HanaConnConf):
            return False
        other = cast(HanaConnConf, other)
        return self.db_host == other.db_host \
            and self.db_port == other.db_port \
            and self.db_name == other.db_name \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'HanaConnConf'):
        assert isinstance(other, HanaConnConf), "apply credentials failed. other must be HanaConnConf"
        other = cast(HanaConnConf, other)
        other.db_host = self.db_host
        other.db_port = self.db_port
        other.db_name = self.db_name
        other.user = self.user
        other.password = self.password


@dataclass
class TeradataConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.TERADATA
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, TeradataConnConf):
            return False
        other = cast(TeradataConnConf, other)
        return self.db_host == other.db_host \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'TeradataConnConf'):
        assert isinstance(other, TeradataConnConf), "apply credentials failed. other must be TeradataConnConf"
        other = cast(TeradataConnConf, other)
        other.db_host = self.db_host
        other.user = self.user
        other.password = self.password


@dataclass
class Db2ConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.DB2
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="39015"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    db_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, Db2ConnConf):
            return False
        other = cast(Db2ConnConf, other)
        return self.db_host == other.db_host \
            and self.db_port == other.db_port \
            and self.db_name == other.db_name \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'Db2ConnConf'):
        assert isinstance(other, Db2ConnConf), "apply credentials failed. other must be Db2ConnConf"
        other = cast(Db2ConnConf, other)
        other.db_host = self.db_host
        other.db_port = self.db_port
        other.db_name = self.db_name
        other.user = self.user
        other.password = self.password


@dataclass
class DynamoDBConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.DYNAMODB
    access_key: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="AWS Access Key Id",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    secret_key: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="AWS Secret Access Key",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    region: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="AWS Region Name",
                        tip="E.g. us-east-1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, DynamoDBConnConf):
            return False
        other = cast(DynamoDBConnConf, other)
        return self.access_key == other.access_key \
            and self.secret_key == other.secret_key \
            and self.region == other.region

    def _apply_conf_to(self, other: 'DynamoDBConnConf'):
        assert isinstance(other, DynamoDBConnConf), "apply credentials failed. other must be DynamoDBConnConf"
        other = cast(DynamoDBConnConf, other)
        other.access_key = self.access_key
        other.secret_key = self.secret_key
        other.region = self.region


@dataclass
class CockroachDBConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.COCKROACHDB
    db_host: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: Optional[int] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="26257"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    db_name: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    user: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, CockroachDBConnConf):
            return False
        other = cast(CockroachDBConnConf, other)
        return self.db_host == other.db_host \
            and self.db_port == other.db_port \
            and self.db_name == other.db_name \
            and self.user == other.user \
            and self.password == other.password

    def _apply_conf_to(self, other: 'CockroachDBConnConf'):
        assert isinstance(other, CockroachDBConnConf), "apply credentials failed. other must be CockroachDBConnConf"
        other = cast(CockroachDBConnConf, other)
        other.db_host = self.db_host
        other.db_port = self.db_port
        other.db_name = self.db_name
        other.user = self.user
        other.password = self.password


@dataclass
class CustomDBConnConf(RelationalConnConf):
    connection_type: PRTConn = PRTConn.CUSTOM_DB
    # redshift_db_address: Optional[str] = None  # dummy
    conn_string: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Connection String",
                        tip="Any SQLAlchemy compatible db conn str (might require driver installation)",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def __repr__(self):
        return str(self)

    def internal_equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, CustomDBConnConf):
            return False
        other = cast(CustomDBConnConf, other)
        return self.conn_string == other.conn_string

    def _apply_conf_to(self, other: 'CustomDBConnConf'):
        assert isinstance(other, CustomDBConnConf), "apply credentials failed. other must be CustomDBConnConf"
        other = cast(CustomDBConnConf, other)
        other.conn_string = self.conn_string


class ConnConfFactory:
    @staticmethod
    def create_or_get(conn_conf_json_dict_or_obj) -> ConnConf:
        # due to json serialization this method can get json, dict or actual class
        conn_conf: Optional[ConnConf]
        if isinstance(conn_conf_json_dict_or_obj, str):
            import json
            conn_conf_json_dict_or_obj = json.loads(conn_conf_json_dict_or_obj)

        if isinstance(conn_conf_json_dict_or_obj, dict):
            if 'connection_type' in conn_conf_json_dict_or_obj:
                conn_type_str = conn_conf_json_dict_or_obj['connection_type']
            else:
                print("WARNING: Using _conn_type in connection json will be retired. Please replace this connection with a newer version")
                # future: retire in 2024-12. _conn_type is legacy definition for connection_type
                conn_type_str = conn_conf_json_dict_or_obj['_conn_type']
            if conn_type_str == PRTConn.LOCAL_FILE:
                conn_conf = LocalFileConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.WORKER_FILE:
                conn_conf = WorkerFileConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.S3:
                conn_conf = S3ConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.SQLITE:
                conn_conf = SqLiteConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.MYSQL:
                conn_conf = MYSQLConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.POSTGRESQL:
                conn_conf = PostgreSQLConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.REDSHIFT:
                conn_conf = RedshiftConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.SNOWFLAKE:
                conn_conf = SnowflakeConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.MSSQL:
                conn_conf = MSSQLConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.ORACLE:
                conn_conf = OracleConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.HIVE:
                conn_conf = HiveConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.ATHENA:
                conn_conf = AthenaConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.ELASTICSEARCH:
                conn_conf = ElasticSearchConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.OPENSEARCH:
                conn_conf = OpenSearchConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.TRINO:
                conn_conf = TrinoConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.DREMIO:
                conn_conf = DremioConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.HANA:
                conn_conf = HanaConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.TERADATA:
                conn_conf = TeradataConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.DB2:
                conn_conf = Db2ConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.DYNAMODB:
                conn_conf = DynamoDBConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.COCKROACHDB:
                conn_conf = CockroachDBConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.CLOUDERA:
                conn_conf = ClouderaConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.CUSTOM_DB:
                conn_conf = CustomDBConnConf.from_dict(conn_conf_json_dict_or_obj)
            else:
                raise AttributeError(f"Unknown connection type {conn_type_str}")
        elif issubclass(type(conn_conf_json_dict_or_obj), ConnConf):
            conn_conf = conn_conf_json_dict_or_obj
        else:
            raise SystemError(f"Unknown conn_conf type {type(conn_conf_json_dict_or_obj)}")

        if conn_conf is not None:
            return conn_conf
        else:
            raise SystemError(f"Unknown conn_conf {conn_conf_json_dict_or_obj}")


# Engine Configuration Classes
@dataclass
class EngConf(PrtDataClassJsonMixin):
    _eng_type: Optional[PRTEng] = None

    @property
    def eng_type(self) -> PRTEng:
        return self._eng_type  # type: ignore[return-value]


@dataclass
class AutoEngConf(EngConf):
    _eng_type: PRTEng = PRTEng.AUTO


@dataclass
class PandasEngConf(EngConf):
    _eng_type: PRTEng = PRTEng.PANDAS


@dataclass
class DaskEngConf(PandasEngConf):
    _eng_type: PRTEng = PRTEng.DASK
    worker_count: Optional[int] = None


@dataclass
class RapidsEngConf(PandasEngConf):
    _eng_type: PRTEng = PRTEng.RAPIDS


@dataclass
class RapidsDaskEngConf(DaskEngConf):
    _eng_type: PRTEng = PRTEng.RAPIDS_DASK
    worker_count: Optional[int] = None


@dataclass
class SparkEngConf(PandasEngConf):
    _eng_type: PRTEng = PRTEng.SPARK


class EngConfFactory:
    @staticmethod
    def create_or_get(eng_conf_json_dict_or_obj) -> EngConf:
        # due to json serialization this method can get json, dict or actual class
        if not eng_conf_json_dict_or_obj:
            return PandasEngConf()

        if isinstance(eng_conf_json_dict_or_obj, str):
            if eng_conf_json_dict_or_obj.strip().startswith("{"):
                import json
                eng_conf_json_dict_or_obj = json.loads(eng_conf_json_dict_or_obj)
            else:
                # simple engine name, might be coming from exported code library
                eng_conf_json_dict_or_obj = {'_eng_type': eng_conf_json_dict_or_obj}

        if isinstance(eng_conf_json_dict_or_obj, dict):
            eng_type_str = str(eng_conf_json_dict_or_obj['_eng_type']).upper()
            if eng_type_str == PRTEng.AUTO:
                return AutoEngConf.from_dict(eng_conf_json_dict_or_obj)
            elif eng_type_str == PRTEng.PANDAS:
                return PandasEngConf.from_dict(eng_conf_json_dict_or_obj)
            elif eng_type_str == PRTEng.DASK:
                return DaskEngConf.from_dict(eng_conf_json_dict_or_obj)
            elif eng_type_str == PRTEng.RAPIDS:
                return RapidsEngConf.from_dict(eng_conf_json_dict_or_obj)
            elif eng_type_str == PRTEng.RAPIDS_DASK:
                return RapidsDaskEngConf.from_dict(eng_conf_json_dict_or_obj)
            elif eng_type_str == PRTEng.SPARK:
                return SparkEngConf.from_dict(eng_conf_json_dict_or_obj)
            else:
                raise AttributeError(f"Unknown engine type {eng_type_str}")
        elif isinstance(eng_conf_json_dict_or_obj, EngConf):
            return eng_conf_json_dict_or_obj
        elif isinstance(eng_conf_json_dict_or_obj, PRTEng):
            if eng_conf_json_dict_or_obj == PRTEng.AUTO:
                return AutoEngConf()
            elif eng_conf_json_dict_or_obj == PRTEng.PANDAS:
                return PandasEngConf()
            elif eng_conf_json_dict_or_obj == PRTEng.DASK:
                return DaskEngConf()
            elif eng_conf_json_dict_or_obj == PRTEng.RAPIDS:
                return RapidsEngConf()
            elif eng_conf_json_dict_or_obj == PRTEng.RAPIDS_DASK:
                return RapidsDaskEngConf()
            elif eng_conf_json_dict_or_obj == PRTEng.SPARK:
                return SparkEngConf()
            else:
                raise AttributeError(f"Unknown PRTEng type {eng_conf_json_dict_or_obj}")
        else:
            raise SystemError(f"Unknown eng_conf type {type(eng_conf_json_dict_or_obj)}")


@dataclass
class PRTDataRequest(PRTRequest):
    # ** We needed to add dict to this list since when dataclass_json cannot figure out type
    #    it returns dict instead of actual class. need to override or use as dict
    conn_conf: Optional[Union[
        dict,
        ConnConf,
        WorkerFileConnConf,
        SqLiteConnConf,
        S3ConnConf,
        MYSQLConnConf,
        PostgreSQLConnConf,
        RedshiftConnConf,
        SnowflakeConnConf,
        MSSQLConnConf,
        OracleConnConf,
        HiveConnConf,
        AthenaConnConf,
        ElasticSearchConnConf,
        OpenSearchConnConf,
        TrinoConnConf,
        DremioConnConf,
        HanaConnConf,
        TeradataConnConf,
        Db2ConnConf,
        DynamoDBConnConf,
        CockroachDBConnConf,
        ClouderaConnConf,
        CustomDBConnConf,
    ]] = None

    eng_conf: Optional[Union[
        dict,
        PandasEngConf,
        DaskEngConf,
        RapidsEngConf,
        RapidsDaskEngConf,
        SparkEngConf,
    ]] = None

    # MySQLConnDef,
    # AuroraMySQLConnDef,


class ConnConfClassFactory:
    @staticmethod
    def get_conn_conf_class(conn_type: PRTConn) -> Union[
        Type[WorkerFileConnConf],
        Type[S3ConnConf],
        Type[SqLiteConnConf],
        Type[PostgreSQLConnConf],
        Type[MYSQLConnConf],
        Type[RedshiftConnConf],
        Type[SnowflakeConnConf],
        Type[MSSQLConnConf],
        Type[OracleConnConf],
        Type[HiveConnConf],
        Type[AthenaConnConf],
        Type[ElasticSearchConnConf],
        Type[OpenSearchConnConf],
        Type[TrinoConnConf],
        Type[DremioConnConf],
        Type[HanaConnConf],
        Type[TeradataConnConf],
        Type[Db2ConnConf],
        Type[DynamoDBConnConf],
        Type[CockroachDBConnConf],
        Type[ClouderaConnConf],
        Type[CustomDBConnConf]
    ]:
        if conn_type == PRTConn.WORKER_FILE:
            return WorkerFileConnConf
        elif conn_type == PRTConn.S3:
            return S3ConnConf
        elif conn_type == PRTConn.SQLITE:
            return SqLiteConnConf
        elif conn_type == PRTConn.POSTGRESQL:
            return PostgreSQLConnConf
        elif conn_type == PRTConn.MYSQL:
            return MYSQLConnConf
        elif conn_type == PRTConn.REDSHIFT:
            return RedshiftConnConf
        elif conn_type == PRTConn.SNOWFLAKE:
            return SnowflakeConnConf
        elif conn_type == PRTConn.MSSQL:
            return MSSQLConnConf
        elif conn_type == PRTConn.ORACLE:
            return OracleConnConf
        elif conn_type == PRTConn.HIVE:
            return HiveConnConf
        elif conn_type == PRTConn.ATHENA:
            return AthenaConnConf
        elif conn_type == PRTConn.ELASTICSEARCH:
            return ElasticSearchConnConf
        elif conn_type == PRTConn.OPENSEARCH:
            return OpenSearchConnConf
        elif conn_type == PRTConn.TRINO:
            return TrinoConnConf
        elif conn_type == PRTConn.DREMIO:
            return DremioConnConf
        elif conn_type == PRTConn.HANA:
            return HanaConnConf
        elif conn_type == PRTConn.TERADATA:
            return TeradataConnConf
        elif conn_type == PRTConn.DB2:
            return Db2ConnConf
        elif conn_type == PRTConn.DYNAMODB:
            return DynamoDBConnConf
        elif conn_type == PRTConn.COCKROACHDB:
            return CockroachDBConnConf
        elif conn_type == PRTConn.CLOUDERA:
            return ClouderaConnConf
        elif conn_type == PRTConn.CUSTOM_DB:
            return CustomDBConnConf
        else:
            raise SystemError(f"Unable to find conn_conf class for conn_type :{conn_type.name}")
