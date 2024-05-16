from abc import abstractmethod

from flask import Flask


class AppFactoryAbs:

    @abstractmethod
    def get_app(self) -> Flask:

        ...
