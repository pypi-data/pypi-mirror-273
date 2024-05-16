from abc import abstractmethod

from flask_projects.interface.base import ProjectInterfaceBase
from flask_projects.interface.container import ContainerAbs


class LogicAbs(ProjectInterfaceBase):

    name: str = '...'  # 每一个logic必须要有唯一名称，用于core模块进行管理

    @abstractmethod
    def execute(self, container: ContainerAbs):

        ...
