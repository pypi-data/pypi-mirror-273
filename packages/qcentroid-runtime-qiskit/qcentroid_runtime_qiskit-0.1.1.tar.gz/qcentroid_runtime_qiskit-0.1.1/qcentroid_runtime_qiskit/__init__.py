import sys
import logging

logger = logging.getLogger(__name__)


class QCentroidRuntimeQiskit:
    _singleton = None

    @staticmethod
    def getVersion() -> str:
        # compatible with python 3.7 version
        if sys.version_info >= (3, 8):
            from importlib import metadata
        else:
            import importlib_metadata as metadata

        if __name__:
            return metadata.version(__name__)

        return "unknown"

    def __init__(self, params):
        if "token" in params:
            self.__token = params.get("token", "")
        if "instance" in params:
            self.__instance = params.get("instance", "")

    @classmethod
    def get_instance(cls, params: dict = {}):
        if cls._singleton is None:
            cls._singleton = cls(params)
        return cls._singleton

    def execute(self, circuit):
        # TODO write execution code
        # use self.__token and self.__instance hidden variables
        pass


__all__ = ["QCentroidRuntimeQiskit"]
