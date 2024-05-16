import uuid
from abc import ABCMeta, abstractmethod
from typing import Optional, Dict, Type, TypeVar

from flask import Blueprint
from flask_restful import Resource, Api

from flask_projects.core.vars.abs import ApplicationAbs, HttpAbs


T = TypeVar('T', bound=Resource)


class RestfulRouterBasic(metaclass=ABCMeta):
    """
        路由基类
    """

    def __init__(self, application: ApplicationAbs = None, http: HttpAbs = None):
        self.application = application
        self.http = http

        self.dict_resource: Optional[Dict[str, Type[T]]] = None
        self.name_bp: Optional[str] = str(uuid.uuid4())
        self.url_prefix: Optional[str] = ''

    def init_router(self, application: ApplicationAbs, http: HttpAbs):
        self.application = application
        self.http = http

    def bind(self):
        app = self.application.getter_app()

        if not self.dict_resource or not self.name_bp:
            raise ValueError('name_bp、dict_resource cannot be None')

        if self.url_prefix and '/' not in self.url_prefix:
            raise ValueError('url_prefix must contain \'/\'')

        blueprint = Blueprint(self.name_bp.replace('.py', ''), __name__, url_prefix=self.url_prefix)
        api = Api(blueprint)

        for url, resource_cls in self.dict_resource.items():
            api.add_resource(resource_cls, url)

            self.http.insert(f'{self.url_prefix}{url}', resource_cls.methods, resource_cls)

        app.register_blueprint(blueprint, url_prefix=self.url_prefix)

    @abstractmethod
    def register(self):
        ...


class ResourceBaisc(Resource):

    ...
