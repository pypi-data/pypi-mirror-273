from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    """Metaclass for Enum classes that allows to check if a value is a valid member of the Enum."""

    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class StrEnum(str, Enum, metaclass=MetaEnum):
    def __str__(self):
        """Return the string representation of the enum using its value."""
        return self.value
