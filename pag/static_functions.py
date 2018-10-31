import os

import psutil
import pag
import subprocess


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


def send2Ftp(in_file: str, addr: str, dir: str, user: str, password: str):
    import ftplib
    #
    print('Uploading...')
    session = ftplib.FTP(addr, user, password)
    if dir is not '':
        session.cwd(dir)
    file = open(in_file, 'rb')  # file to send
    session.storbinary('STOR ' + in_file, file)  # send the file
    file.close()  # close file and FTP
    session.quit()
    print('Done')

def docx2pdf(in_file: str, out_file: str):
    import comtypes.client

    print('Creating PDF...')
    in_path = os.path.abspath(in_file)
    out_path = os.path.abspath(out_file)
    wdFormatPDF = 17

    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(in_path)
    doc.SaveAs(out_path, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()
    print('Done')


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

    print(Conv.to_int(a))
    print(Conv.to_int(b))
    print(Conv.to_int(c))
    print(Conv.to_int(d))
    print(Conv.to_int(e))
    print(Conv.to_int(f))

    # a = '0x1'
    # print(int(a, 16))

    # cmd('start','explorer.exe', 'c:/windows')
