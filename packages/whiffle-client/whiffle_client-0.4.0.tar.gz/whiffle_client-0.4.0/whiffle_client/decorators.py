from pathlib import Path
import yaml

from functools import wraps

from yamlinclude import YamlIncludeConstructor
from whiffle_client.loaders import csv_loader_constructor

YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader)
yaml.add_constructor("!include-csv", csv_loader_constructor)


def load_data(class_type, resource_type=None):
    def wrap(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            data = kwargs.get("data", None)
            if isinstance(data, str) or isinstance(data, Path):
                # Data provided as yaml path
                data = yaml.load(open(data), Loader=yaml.FullLoader)
                # TODO: gather from the yaml just the data_type matching the resource_type
                #       Goal here is to provide
                data_type = data.pop("type", None)
                data = class_type(**data)
            elif isinstance(data, dict):
                # Data directly provided as dict
                data = class_type(**data)
            if data:
                kwargs["data"] = data._get_api_params()
            else:
                raise ValueError("Please provide valid data or path to valid data")
            return func(self, *args, **kwargs)

        return wrapper

    return wrap


def request_ok(func):
    def wrapper(self, *args, **kwargs):
        request = func(self, *args, **kwargs)
        try:
            request.raise_for_status()
            return request
        except Exception:
            raise ValueError(request.json())

    return wrapper
