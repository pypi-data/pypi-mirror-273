from app.{{cookiecutter.integration_id}} import {{cookiecutter.classname}}
from app.model.request_body import RequestBody
from pykson import Pykson
import json

pykson = Pykson()
integration_class = {{cookiecutter.classname}}()


