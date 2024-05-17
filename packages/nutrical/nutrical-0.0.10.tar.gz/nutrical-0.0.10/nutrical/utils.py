import pint
from numbers import Number

UREG = pint.UnitRegistry()


def add_amount(a, b):
    """amount addition

    Returns
    -------
    pint.Quantity
        Addition is only defined when both inputs are pint.Quantity.
        For str and Number, the unit is unrecognized and thus addition
        cannot be performed.
    """
    if isinstance(a, pint.Quantity) and isinstance(b, pint.Quantity):
        try:
            return a + b
        except:
            return None
    return None


def parse_amount(x):
    """Parse amount

    Returns
    -------
    Number | str | pint.Quantity
        Depending on the input and whether the parsing succeeded, the 
        returned value could either be `Number`, `str`, or `pint.Quantity`.

        When input x is `str`, the returned value is either 
        `pint.Quantity` or `str`, depending on whether pint recognizes the
        unit in the passed in value.

        If the input x is `pint.Quantity` or `Number`, no parsing is done 
        and the input is returned as output.
    """
    if isinstance(x, pint.Quantity) or isinstance(x, Number) or x is None:
        return x
    if isinstance(x, str):
        try:
            return UREG(x)
        except:
            return x
    raise Exception("Unsupported input type. Only (str|Number|pint.Quantity) are allowed.")


def parse_unit(x):
    if isinstance(x, pint.Quantity) or x is None:
        return x
    if isinstance(x, str):
        try:
            return UREG(x)
        except:
            Warning("Failed to parse unit. Return None.")
            return None
    raise Exception("Unsupported input type. Only (str|pint.Quantity) are allowed.")



def round2(x, ndigits=None):
    if x is None: return None
    return round(x, ndigits=ndigits)
