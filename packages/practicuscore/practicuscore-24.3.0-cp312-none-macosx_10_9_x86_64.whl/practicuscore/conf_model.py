import json
from dataclasses import dataclass
from typing import Union, List
import base64

from practicuscore.api_base import PrtDataClassJsonMixin, ConnConf, WorkerFileConnConf, SqLiteConnConf, S3ConnConf, MYSQLConnConf, \
    PostgreSQLConnConf, RedshiftConnConf, SnowflakeConnConf, MSSQLConnConf, OracleConnConf, HiveConnConf, \
    AthenaConnConf, ElasticSearchConnConf, OpenSearchConnConf, CustomDBConnConf, TrinoConnConf, DremioConnConf, \
    HanaConnConf, TeradataConnConf, Db2ConnConf, DynamoDBConnConf, CockroachDBConnConf, ClouderaConnConf, \
    ConnConfFactory


@dataclass
class DefinedConnectionConfiguration(PrtDataClassJsonMixin):
    uuid: str
    key: str
    cloud: str
    region_name: str
    conn_conf: Union[
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
    ]
    can_write: bool = True
    owner_email: str = "?@?.?"


@dataclass
class DefinedConnectionConfigurations(PrtDataClassJsonMixin):
    defined_conn_conf_list: List[DefinedConnectionConfiguration]

    def to_base64_str(self) -> str:
        return str(base64.b64encode(bytes(self.to_json(), encoding="utf-8")), "utf-8")

    @staticmethod
    def from_base64_str(data: str) -> 'DefinedConnectionConfigurations':
        json_str = str(base64.b64decode(data), "utf-8")
        defined_conn_confs = DefinedConnectionConfigurations.from_json(json_str)

        # Why the below?
        # When we load DefinedConnectionConfigurations using json, Dataclasses json cannot properly detect the type of
        # child conn_conf classes. e.g. S3ConnConf becomes ConnConf and all it's info, aws_access_key etc gets lost
        # So we create a proper S3ConnConf and override
        # Future: Dataclasses jason parent marshmallow have a schema() features;
        # E.g. you dump a class, it saves __type="actual class name" with it. and uses that to deserialize (I think)
        def_conn_conf_dict = json.loads(json_str)
        raw_dict_conn_conf_list = def_conn_conf_dict["defined_conn_conf_list"]
        assert len(defined_conn_confs.defined_conn_conf_list) == len(raw_dict_conn_conf_list)
        for i in range(len(defined_conn_confs.defined_conn_conf_list)):
            conn_conf_from_raw = ConnConfFactory.create_or_get(raw_dict_conn_conf_list[i]["conn_conf"])
            defined_conn_confs.defined_conn_conf_list[i].conn_conf = conn_conf_from_raw

        return defined_conn_confs


# if __name__ == '__main__':
#     cn_cnf = WorkerFileConnConf(file_path="/users/blah")
#     a = DefinedConnectionConfiguration(uuid="a", key="a", cloud="a", region_name="a", conn_conf=cn_cnf)
#     cn_cnf2 = WorkerFileConnConf(file_path="/users/blah2")
#     b = DefinedConnectionConfiguration(uuid="b", key="b", cloud="b", region_name="b", conn_conf=cn_cnf2)
#
#     l = DefinedConnectionConfigurations(defined_conn_conf_list=[a, b])
#
#     _json = l.to_json()
#     print(_json)
#     l2 = DefinedConnectionConfigurations.from_json(_json)
#
#     print(l2.defined_conn_conf_list[1].uuid)
#
#     b64 = l2.to_base64_str()
#     print(b64)
#     l3 = DefinedConnectionConfigurations.from_base64_str(b64)
#     print(l3.to_json())
