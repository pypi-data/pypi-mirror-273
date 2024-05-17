from dataclasses import dataclass

from mloggers import FileLogger, LogLevel


@dataclass
class SomeObject:
    a: int
    b: str


@dataclass
class SomeJSONObject:
    c: float
    d: bool

    def to_json(self):
        return {"c": self.c, "d": self.d}


logger = FileLogger("test.log", default_priority=LogLevel.DEBUG)
logger.info("Hello, world!")
o1 = SomeObject(1, "hello")
o2 = SomeJSONObject(1.0, True)
logger.debug(
    {
        "a": 1,
        "b": "hello",
        "object": o1,
        "json_object": o2,
    }
)
logger.debug(
    {
        "a": 1,
        "b": "hello",
        "object": o1,
        "json_object": o2,
    }
)
