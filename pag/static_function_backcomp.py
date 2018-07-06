from pag.static_functions import Conv
# === Compability functions


def int_to_hexstr(in_int: int, n_symb: int = 8, leadzero: bool = True) -> str:
    return Conv.int_to_hexstr(in_int, n_symb, leadzero)


def to_int(in_v: str):
    return Conv.to_int(in_v)


def to_str(in_var, int_as_hex=True):
    return Conv.to_str(in_var, int_as_hex)