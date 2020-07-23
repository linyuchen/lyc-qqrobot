from dataclasses import dataclass

@dataclass
class Test:
    a: str


@dataclass
class Test2(Test):
    b: str


t = Test2(b=1)
print(t.a)

