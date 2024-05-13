import hashlib
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Union

from practicuscore import get_logger, Log
from practicuscore.util import CryptoUtil


class K8sAuthToken:
    def __init__(self, refresh_token: str, access_token: str, username: Optional[str] = None) -> None:
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.username = username


@dataclass
class K8sClusterDefinition:
    name: str = ""
    region_name: str = ""


class K8sConfig:
    def __init__(self, host_url: str, email: str, refresh_token: Optional[str] = None, username: Optional[str] = None):
        super().__init__()
        self.host_url = host_url
        self.email = email
        self.refresh_token: str | None = refresh_token
        self.password: Optional[str] = None
        self.cluster_name: Optional[str] = None
        self.region_name: Optional[str] = None
        self._username: Optional[str] = username

    def to_dict(self) -> dict:
        conf_dict = {
            'host_url': self.host_url,
            'email': self.email,
            'username': self.username,
        }

        if self.password is not None:
            conf_dict['password'] = self.password

        if self.refresh_token is not None:
            conf_dict['refresh_token'] = self.refresh_token

        if self.cluster_name is not None:
            conf_dict['cluster_name'] = self.cluster_name

        if self.region_name is not None:
            conf_dict['region_name'] = self.region_name

        return conf_dict

    @staticmethod
    def from_dict(dict_item: dict) -> 'K8sConfig':
        username = dict_item['username'] if 'username' in dict_item else None
        k8s_config = K8sConfig(
            host_url=dict_item['host_url'], email=dict_item['email'], refresh_token=dict_item['refresh_token'],
            username=username)
        if 'password' in dict_item:
            k8s_config.password = dict_item['password']
        if 'cluster_name' in dict_item:
            k8s_config.cluster_name = dict_item['cluster_name']
        if 'region_name' in dict_item:
            k8s_config.region_name = dict_item['region_name']
        return k8s_config

    def set_password(self, password_plain_text: str):
        self.password = CryptoUtil.encrypt(password_plain_text)

    @property
    def password_in_plain_text(self) -> Optional[str]:
        if self.password:
            return CryptoUtil.decrypt(self.password)
        else:
            return None

    @property
    def ssl(self) -> bool:
        return self.host_url.startswith("https")

    @property
    def host_dns(self) -> str:
        return self.host_url.replace("https://", "").replace("http://", "")

    @property
    def hash_text(self) -> str:
        return f"{self.host_url}-{self.email}-{self.refresh_token}-{self.password}"

    @property
    def hash_key(self) -> str:
        m = hashlib.md5()
        m.update(bytes(self.hash_text, "utf-8"))
        return str(m.hexdigest())

    @property
    def username(self) -> str:
        try:
            if self._username:
                return self._username
            else:
                return self.email.split("@")[0]
        except Exception as e:
            print(f"ERROR: Could not get user name from email of k8s region. Err: {e}")
            return "practicus_ai"

    @property
    def key(self) -> str:
        return f"{self.username}@{self.host_dns}"


class ModelPrefix:
    logger = get_logger(Log.SDK)

    def __init__(self, key: str, prefix: str) -> None:
        super().__init__()
        self.key = key
        self.prefix = prefix

    def get_csv_header(self) -> str:
        # Updating? change __str__()
        return "key,prefix"

    def __str__(self):
        # Updating? change get_csv_header()
        return f"{self.key},{self.prefix}"

    def __repr__(self):
        header_items = self.get_csv_header().split(",")
        row_items = str(self).split(",")
        final_items: list[str] = []
        if len(header_items) == len(row_items):
            for i in range(len(header_items)):
                final_items.append(f"{header_items[i]}: {row_items[i]}")
            return "\n".join(final_items)
        else:
            self.logger.warning(
                "Header items do not match string items for ModelPrefix. Will return a simpler representation.")
            return str(self)


class ModelDeployment:
    logger = get_logger(Log.SDK)

    def __init__(self, key: str, name: str) -> None:
        super().__init__()
        self.key = key
        self.name = name

    def get_csv_header(self) -> str:
        # Updating? change __str__()
        return "key,name"

    def __str__(self):
        # Updating? change get_csv_header()
        return f"{self.key},{self.name}"

    def __repr__(self):
        header_items = self.get_csv_header().split(",")
        row_items = str(self).split(",")
        final_items: list[str] = []
        if len(header_items) == len(row_items):
            for i in range(len(header_items)):
                final_items.append(f"{header_items[i]}: {row_items[i]}")
            return "\n".join(final_items)
        else:
            self.logger.warning(
                "Header items do not match string items for ModelDeployment. Will return a simpler representation.")
            return str(self)


class ModelVersionInfo:
    def __init__(self, version_tag: str, version: Optional[str] = None):
        self.version_tag = version_tag
        self.version = version

    @staticmethod
    def create_from_version(version: str) -> 'ModelVersionInfo':
        return ModelVersionInfo(version_tag=f"v{version}", version=version)

    @staticmethod
    def create_latest() -> 'ModelVersionInfo':
        return ModelVersionInfo(version_tag="latest")

    @staticmethod
    def create_production() -> 'ModelVersionInfo':
        return ModelVersionInfo(version_tag="production")

    @staticmethod
    def create_staging() -> 'ModelVersionInfo':
        return ModelVersionInfo(version_tag="staging")


class ModelMetaVersion:
    def __init__(self, version_id: int, version: str, model_deployment: ModelDeployment, stage: Optional[str] = None) -> None:
        super().__init__()
        self.id = version_id
        self.version = version
        self.stage = stage
        self.model_deployment = model_deployment

    def to_model_version_info(self) -> ModelVersionInfo:
        return ModelVersionInfo.create_from_version(self.version)


class ModelMeta:

    def __init__(self, model_id: int, name: str, model_prefix: ModelPrefix, model_versions: List[ModelMetaVersion]) \
            -> None:
        super().__init__()
        self.model_id = model_id
        self.name = name
        self.model_prefix = model_prefix
        self.model_versions = model_versions

    @property
    def production_version(self) -> Optional[ModelMetaVersion]:
        for model_meta_version in self.model_versions:
            if model_meta_version.stage == "Production":
                return model_meta_version
        return None

    @property
    def staging_version(self) -> Optional[ModelMetaVersion]:
        for model_meta_version in self.model_versions:
            if model_meta_version.stage == "Staging":
                return model_meta_version
        return None


class ExternalServiceType(str, Enum):
    AIRFLOW = "AIRFLOW"
    MLFLOW = "MLFLOW"
    JUPYTER_LAB = "JUPYTER_LAB"
    SPARKUI = "SPARKUI"
    GRAFANA = "GRAFANA"

    @classmethod
    def from_value(cls, value: Union[str, Enum]) -> 'ExternalServiceType':
        str_val = str(value.value if hasattr(value, "value") else value).upper()
        for i, enum_val in enumerate(cls):
            # noinspection PyUnresolvedReferences
            if str(enum_val.value).upper() == str_val:
                return cls(enum_val)

        raise ValueError(f'{value} is not a valid {cls}')


# Pages that use hardware acceleration can fail on Chrome + K8s workspace
# Sample test site: https://webglsamples.org/blob/blob.html
# https://bugs.chromium.org/p/chromium/issues/detail?id=1506249#c2
KNOWN_COMPLEX_WEB_SERVICES = [ExternalServiceType.JUPYTER_LAB]


class ExternalService(ABC):
    def __init__(
            self, key: str, name: str, service_type: ExternalServiceType, url: Optional[str] = None,
            oauth_key: Optional[str] = None, db_key: Optional[str] = None, obj_key: Optional[str] = None,
            git_key: Optional[str] = None, configuration: Optional[dict] = None,
    ) -> None:
        self.key: str = key
        self.name: str = name
        self.service_type: ExternalServiceType = service_type
        self.url: Optional[str] = url
        self.oauth_key: Optional[str] = oauth_key
        self.db_key: Optional[str] = db_key
        self.obj_key: Optional[str] = obj_key
        self.git_key: Optional[str] = git_key
        self.configuration: dict = configuration if configuration is not None else {}


class WorkflowService(ExternalService):
    MY_SVC_TYPE = ExternalServiceType.AIRFLOW

    def __init__(
            self, key: str, name: str, url: Optional[str] = None,
            oauth_key: Optional[str] = None, db_key: Optional[str] = None, obj_key: Optional[str] = None,
            git_key: Optional[str] = None, configuration: Optional[dict] = None,
    ) -> None:
        super().__init__(
            key=key, name=name, service_type=self.MY_SVC_TYPE, url=url, oauth_key=oauth_key,
            db_key=db_key, obj_key=obj_key, git_key=git_key, configuration=configuration)

        assert self.url, f"url must be defined for {type(self)}. key: {key}, name: {name}"
        assert self.git_key, f"git_key must be defined for {type(self)}. key: {key}, name: {name}"


class ExperimentService(ExternalService):
    MY_SVC_TYPE = ExternalServiceType.MLFLOW

    def __init__(
            self, key: str, name: str, url: Optional[str] = None,
            oauth_key: Optional[str] = None, db_key: Optional[str] = None, obj_key: Optional[str] = None,
            git_key: Optional[str] = None, configuration: Optional[dict] = None,
    ) -> None:
        super().__init__(
            key=key, name=name, service_type=self.MY_SVC_TYPE, url=url, oauth_key=oauth_key,
            db_key=db_key, obj_key=obj_key, git_key=git_key, configuration=configuration)

        assert self.url, f"url must be defined for {type(self)}. key: {key}, name: {name}"


class ObservabilityService(ExternalService):
    MY_SVC_TYPE = ExternalServiceType.GRAFANA

    def __init__(
            self, key: str, name: str, url: Optional[str] = None,
            oauth_key: Optional[str] = None, db_key: Optional[str] = None, obj_key: Optional[str] = None,
            git_key: Optional[str] = None, configuration: Optional[dict] = None,
    ) -> None:
        super().__init__(
            key=key, name=name, service_type=self.MY_SVC_TYPE, url=url, oauth_key=oauth_key,
            db_key=db_key, obj_key=obj_key, git_key=git_key, configuration=configuration)

        assert self.url, f"url must be defined for {type(self)}. key: {key}, name: {name}"
