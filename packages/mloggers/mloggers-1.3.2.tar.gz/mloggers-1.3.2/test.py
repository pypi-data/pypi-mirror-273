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
logger.debug(
    {
        "a": 1,
        "b": "hello",
        "object": SomeObject(1, "hello"),
        "json_object": SomeJSONObject(1.0, True),
    }
)
