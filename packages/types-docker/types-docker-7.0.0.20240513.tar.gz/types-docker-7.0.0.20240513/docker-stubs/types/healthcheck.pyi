from .base import DictType

class Healthcheck(DictType):
    def __init__(self, **kwargs) -> None: ...
    @property
    def test(self): ...
    @test.setter
    def test(self, value) -> None: ...
    @property
    def interval(self): ...
    @interval.setter
    def interval(self, value) -> None: ...
    @property
    def timeout(self): ...
    @timeout.setter
    def timeout(self, value) -> None: ...
    @property
    def retries(self): ...
    @retries.setter
    def retries(self, value) -> None: ...
    @property
    def start_period(self): ...
    @start_period.setter
    def start_period(self, value) -> None: ...
