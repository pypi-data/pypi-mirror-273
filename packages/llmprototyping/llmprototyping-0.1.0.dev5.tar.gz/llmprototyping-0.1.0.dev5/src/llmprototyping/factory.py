from .error import LLMPException

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = cls.__call__(*args, **kwargs)
            print(cls)
            print(instance)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Factory(metaclass=Singleton):
    __cls_registry = {}
    _class = None

    @classmethod
    def __get_registry(cls):
        if cls not in Factory.__cls_registry:
            Factory.__cls_registry[cls] = {}
        return Factory.__cls_registry[cls]

    @classmethod
    @property
    def available_models(cls):
        registry = cls.__get_registry()
        return [x for x in registry.keys()]

    @classmethod
    def model_registered(cls, name):
        registry = cls.__get_registry()
        return name in registry

    @classmethod
    def register(cls, name, class_obj, alias = None):
        if issubclass(class_obj, cls._class):
            registry = cls.__get_registry()
            registry[name] = class_obj
            if alias is not None:
                registry[alias] = class_obj
        else:
            raise LLMPException.param_error(f"error registering {class_obj}: type mismatch; expected {cls._class}")

    @classmethod
    def build(cls, name, data={}):
        registry = cls.__get_registry()
        obj_cls = registry.get(name)
        if obj_cls:
            return obj_cls.from_dict(data)
        else:
            raise LLMPException.not_found(f"No model registered with name '{name}'")
