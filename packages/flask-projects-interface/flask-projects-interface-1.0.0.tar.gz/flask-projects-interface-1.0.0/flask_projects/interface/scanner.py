from abc import abstractmethod

from flask_projects.interface.base import ProjectInterfaceBase


class ScannerAbs(ProjectInterfaceBase):

    name: str = '...'  # 每一个scanner必须要有唯一名称，用于core模块进行管理

    @abstractmethod
    def scan(self, path_dir: str):

        ...
