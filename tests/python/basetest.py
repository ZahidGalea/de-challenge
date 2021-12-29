import unittest
from abc import ABC, abstractmethod


class Config:
    def __init__(self) -> None:
        pass


class TestBase(unittest.TestCase, ABC):
    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.config = Config()

    @abstractmethod
    def setUp(self) -> None:
        pass

    @staticmethod
    def safe_mkdir(path: str):
        import errno
        import os

        try:
            os.makedirs(path, exist_ok=True)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
