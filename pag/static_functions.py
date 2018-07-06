import os
import time
import psutil
import pag
import subprocess
from pag.static_function_backcomp import *


class Process:
    @staticmethod
    def is_running(proc_name: str) -> bool:
        for proc in psutil.process_iter():
            if proc.name() == proc_name:
                return True
        return False

    @staticmethod
    def kill(proc_name: str) -> bool:
        if Process.is_running(proc_name):
            os.system("Taskkill /IM " + proc_name + " /f /t")
            return Process.is_running(proc_name)
        else:
            return True

    @staticmethod
    def run(file_path, params="") -> bool:
        if not Process.is_running(file_path.last_str()):
            cmd = file_path.s() + " " + params
            os.system(cmd)
            return True


def input_formatter(in_str: str, n_symb=None,
                    lead_zeros=False,
                    only_nums=False,
                    hex_nums=False) -> str:
    formated = in_str
    if only_nums:  # <----------------------- only_nums/hex_nums handling
        str_nums = ""
        for s in formated:
            try:
                if hex_nums:
                    int(s, 16)  # just check
                else:
                    int(s, 0)  # just check
                char = s
            except ValueError:
                char = '0'
            str_nums = str_nums + char
        formated = str_nums
    if n_symb is not None:  # <-------------- n_symb handling
        formated = formated[-n_symb:]
    if lead_zeros:  # <-------------- lead_zeros handling
        formated = formated.zfill(n_symb)
    else:
        formated_len = len(formated)
        if formated_len < n_symb:
            f_ = '_' * (n_symb - formated_len)
            formated = f_ + formated
    return formated


def create_folder(directory: str) -> int:
    if not os.path.exists(directory):
        os.makedirs(directory)
        return 0
    else:
        return 1


def pt(out: str, pr: int = 1) -> None:
    if pr == 0:
        return
    if pr == 1:
        print(out)
        return
    if pr == 2:
        print(" .", end="", flush=True)
        print(out)
        return
    if pr >= 3:
        print("dbg>>> " + get_time_string() + ": ", end="", flush=True)
        print(out)
        return


def is_file_or_folder(p: str) -> int:
    if os.path.isfile(p):
        return 1
    elif os.path.isdir(p):
        return 2
    else:
        return 0


# @staticmethod
def cls():
    """Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


# @staticmethod
def get_time_string():
    import datetime
    t = str(datetime.date.today()) + "_" \
        + ('{:02d}'.format(datetime.datetime.now().hour)) + "_" \
        + ('{:02d}'.format(datetime.datetime.now().minute)) + "_" \
        + ('{:02d}'.format(datetime.datetime.now().second))
    return t


def get_py_file_folder():
    p = str(os.path.realpath(__file__))
    return pag.Path(p)


def get_py_file_drive() -> str:
    return get_py_file_folder().s()[0:2]


def set_working_dir_to(work_dir=''):
    if work_dir is '':
        work_dir = str(os.path.realpath(__file__))
    os.chdir(work_dir)


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
                return int_to_hexstr(in_var)
            else:
                return str(in_var)
        else:
            return None




def printhex(in_var):
    pstr = to_str(hex(in_var))
    print(pstr)
    return pstr


def printinf(inf_str: str, in_val, int_as_hex: bool = False):
    pstr = inf_str + to_str(in_val, int_as_hex=int_as_hex)
    print(pstr)
    return pstr


def info(in_msg, samelime=False, _hex_=False) -> None:
    if type(in_msg) == int:
        if _hex_:
            in_msg = to_str(in_msg)
        else:
            in_msg = str(int)
    # ---------------------------------------------------
    if samelime:
        print(in_msg, end="", flush=True)
    else:
        print(in_msg)
    time.sleep(2)


def cmd(*params, win=True):
    """
    can handle pag.Path and str

    """
    cmd_str = ''
    p_str = ''
    for p in params:
        if type(p) == str:
            p_str = p
        elif type(p) == pag.Path:
            if win:
                p_str = "\"" + p.s().replace('/', '\\') + "\""
            else:
                p_str = "\"" + p.s() + "\""
        else:
            p_str = ''
        cmd_str = cmd_str + ' ' + p_str
    cmd_str = cmd_str[1:]
    proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    print(err)
    return out


if __name__ == '__main__':
    a = '0xaab'
    b = '0b010100'
    c = '0o12349'
    d = '031231'
    e = '0324234kj'
    f = '0324234'

    print(to_int(a))
    print(to_int(b))
    print(to_int(c))
    print(to_int(d))
    print(to_int(e))
    print(to_int(f))

    # a = '0x1'
    # print(int(a, 16))

    # cmd('start','explorer.exe', 'c:/windows')