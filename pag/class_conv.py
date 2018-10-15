import time
import pag


class Conv:

    @staticmethod
    def int_to_hexstr(in_int: int, n_symb: int = 8, leadzero: bool = True) -> str:
        raw_str = str(hex(in_int))
        minus = ''
        if raw_str[0] == '-':
            halfraw_str = raw_str[3:]
            minus = '-'
        else:
            halfraw_str = raw_str[2:]
        out_str = halfraw_str.zfill(n_symb)
        if leadzero:
            out_str = minus + '0x' + out_str
        return out_str

    @staticmethod
    def define_str_num_type(num_str: str) -> int:
        """
        16 - hex
        10 - dec
        8 - oct
        2 - bin
        11 - no_prefix, can converted to dec
        0 - no idea
        :param num_str: str to define
        :return: base of num system
        """
        pre = num_str[0:2]
        if pre == '0x':
            return 16
        elif pre == '0b':
            return 2
        elif pre == '0o':
            return 8
        # elif pre == '0d':
        #     return 10
        else:
            try:
                int(num_str)
                return 10
            except ValueError:
                return 0

    @staticmethod
    def to_int(in_v: str):
        base = Conv.define_str_num_type(in_v)
        if type(in_v) == int:
            return in_v
        if base == 11:
            return int(in_v)
        else:
            try:
                return int(in_v, base)
            except ValueError:
                return 0

    @staticmethod
    def to_str(in_var, int_as_hex=True):
        if type(in_var) == str:  # <--------------  str
            return
        elif type(in_var) == pag.Path:  # <-----------  Path
            return in_var.s()
        elif type(in_var) == int:  # <-----------   int
            if int_as_hex:
                return Conv.int_to_hexstr(in_var)
            else:
                return str(in_var)
        else:
            return None

    @staticmethod
    def printhex(in_var):
        pstr = Conv.to_str(hex(in_var))
        print(pstr)
        return pstr

    @staticmethod
    def printinf(inf_str: str, in_val, int_as_hex: bool = False):
        pstr = inf_str + Conv.to_str(in_val, int_as_hex=int_as_hex)
        print(pstr)
        return pstr

    @staticmethod
    def info(in_msg, samelime=False, _hex_=False) -> None:
        if type(in_msg) == int:
            if _hex_:
                in_msg = Conv.to_str(in_msg)
            else:
                in_msg = str(int)
        # ---------------------------------------------------
        if samelime:
            print(in_msg, end="", flush=True)
        else:
            print(in_msg)
        time.sleep(2)
