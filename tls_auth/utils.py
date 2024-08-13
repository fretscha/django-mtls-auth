from abc import ABC, abstractmethod
from importlib import import_module
from typing import Type

from .settings import USER_DATA_EXTRACTOR_CLASS


def get_user_data_extractor_class() -> Type["UserDataExtractor"]:
    """
    Load the UserDataExtractor class specified in Django settings.
    """
    class_path = USER_DATA_EXTRACTOR_CLASS
    module_path, class_name = class_path.rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, class_name)


def dn_to_dict(dn: str) -> dict[str, str]:
    """
    Convert a DN string to a dict.

    :param dn: string
    :return: dict
    """
    return {key.strip(): value.strip() for key, value in (component.split("=") for component in dn.split(","))}


class UserDataExtractor(ABC):
    @abstractmethod
    def get_userdata(self, dn: str) -> dict[str, str]:
        """
        Extracts user data from the subjectDN string.

        :param subject_dn: The subjectDN string from the client certificate.
        :return: A dictionary containing the extracted user data.
        """
        pass


class DefaultUserDataExtractor(UserDataExtractor):
    def get_userdata(self, dn: str) -> dict[str, str]:
        """
        remark: it is mandatory to extract the username from the DN, other fields are optional

        DN = "emailAddress=thomas.muster@example.com,CN=thomas.muster@example.com,SN=Muster,GN=Thomas"

        :param dn: string
        :return: dict
        """
        _dn = dn_to_dict(dn)
        ret = {}
        # username is mandatory
        assert "CN" in _dn, "CN is a mandatory field in the DN"
        ret["username"] = _dn.get("CN", "")
        ret["last_name"] = _dn.get("SN", "").title()
        ret["first_name"] = _dn.get("GN", "").title()
        ret["email"] = _dn.get("E", "")
        return ret
