import enum


class ClassicalEnum(int, enum.Enum):
    def __str__(self) -> str:
        return f"{type(self).__name__}.{self.name}"

    def __repr__(self) -> str:
        return str(self)
