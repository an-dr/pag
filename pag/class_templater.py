from tkinter import *
import re
import os


class Templater:
    def __init__(self, in_str, out_path=None, input_is_path=False):
        self.input = in_str
        self.path_to_write = out_path
        self.cur_row = 0
        self.fields = {}
        self.text_in = ""
        self.test_out = "No text yet"
        self.window = Tk()
        self.mode_input_is_path = input_is_path
        self.__load_input()
        self.__ui()

    def __ui_add_var_field(self, field_dict: dict, var_name):
        lbl = Label(self.window, text=var_name)
        lbl.grid(column=0, row=self.cur_row)
        txt = Entry(self.window, width=10)
        txt.grid(column=1, row=self.cur_row)
        field_dict.update({var_name: txt})
        self.cur_row += 1

    def __ui(self):
        match = re.findall(r'\$\{[^\}]+\}', self.text_in)
        if len(match):
            for m in match:
                self.__ui_add_var_field(self.fields, m)
        self.window.title("Create a template")
        btn = Button(self.window, text="Done!", command=self.__on_click)
        self.window.geometry('100x' + str((self.cur_row + 1) * 23))
        btn.grid(column=1, row=self.cur_row)
        self.window.mainloop()

    def __load_input(self):
        if self.mode_input_is_path:
            if not os.path.exists(self.input):
                print("There is no input file")
                return
            with open(self.input) as f:
                self.text_in = f.read()
        else:
            self.text_in = self.input

    def __get_output_text(self):
        text_out = self.text_in  # type: str
        variables = self.get_variables()
        for var, val in variables.items():
            text_out = text_out.replace(var, val)
        self.test_out = text_out

    def __on_click(self):
        self.window.title("Clicked!")
        self.__get_output_text()
        print(self.get_variables())
        print(self.test_out)
        if self.path_to_write is not None:
            self.write()
        self.window.destroy()

    def get_variables(self):
        variables = {}
        for var, field in self.fields.items():
            variables.update({var: field.get()})
        return variables

    def write(self):
        if os.path.exists(self.path_to_write):
            raise FileExistsError
        f = open(self.path_to_write, 'w+')
        f.write(self.test_out)


if __name__ == '__main__':
    text_in = "Hello, ${Name}\n" \
              "Today is ${Weather}"
    a = Templater(text_in, "C:/Users/dongr/out.txt")
