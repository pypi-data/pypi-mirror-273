from typing import Any, Optional
from DMT.core import SpecifierStr, get_sub_specifiers


def sub_specifier_parameter(arg_name: str, val: Any) -> Optional[SpecifierStr]:
    """Return the sub_specifier for given XStep argument with name arg_name and value val."""
    if isinstance(val, SpecifierStr):
        return val
    elif isinstance(val, str):
        return get_sub_specifiers(val)[0]
    elif val is None:
        return None

    raise ValueError(f"{arg_name}: '{val}' is not a valid SpecifierStr!")
