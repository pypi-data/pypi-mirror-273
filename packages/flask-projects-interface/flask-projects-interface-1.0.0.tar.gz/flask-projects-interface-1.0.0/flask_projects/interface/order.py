from abc import abstractmethod

from flask_projects.interface.base import ProjectInterfaceBase


class OrderAbs(ProjectInterfaceBase):

    name: str = '...'  # 每一个order必须要有唯一名称，用于core模块进行管理

    @abstractmethod
    def get_orders(self) -> list:

        ...
