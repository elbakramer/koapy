import threading


class Singleton:

    _instance = None
    _lock = threading.RLock()

    @classmethod
    def _get_instance_without_check(
        cls, *args, **kwargs
    ):  # pylint: disable=unused-argument
        return cls._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        with cls._lock:
            if not isinstance(cls._instance, cls):
                cls._instance = cls(*args, **kwargs)
            cls.get_instance = cls._get_instance_without_check
            return cls._instance
