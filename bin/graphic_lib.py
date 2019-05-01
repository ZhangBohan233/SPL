import tkinter
import spl_interpreter as inter
import bin.spl_lib as lib
from tkinter import filedialog


class Graphic(lib.NativeType):
    def __init__(self, name: lib.String):
        lib.NativeType.__init__(self)

        true_name = "tkinter." + name.literal + "()"
        self.tk: tkinter.Label = eval(true_name)

    @classmethod
    def type_name__(cls) -> str:
        return "Graphic"

    def set_bg(self, color: lib.String):
        self.tk.configure(bg=color.literal)

    def configure(self, key: lib.String, value):
        cfg = {key.literal: value}
        self.tk.configure(cfg)

    def get(self, key: lib.String):
        return self.tk[key.literal]

    def set_attr(self, attr: lib.String, value):
        setattr(self.tk, attr.literal, value)

    def callback(self, env, cmd: lib.String, ftn):
        cfg = {cmd.literal: lambda: inter.call_function(None, [], (0, "callback"), ftn, env)}
        self.tk.configure(cfg)

    @staticmethod
    def file_dialog(types: lib.Pair):
        return filedialog.askopenfilename(filetypes=[(str(types[ext]), str(ext)) for ext in types])

    def call(self, func_name: lib.String, pos_args: lib.List, kwargs: lib.Pair):
        args = []
        for pa in pos_args:
            args.append(str(pa))
        for kwa in kwargs:
            args.append("{}={}".format(kwa, kwargs[kwa]))
        arguments = ", ".join(args)
        command = "self.tk.{}({})".format(func_name, arguments)
        res = eval(command)
        if isinstance(res, str):
            return lib.String(res)
        else:
            return res


class Window(lib.NativeType):
    def __init__(self):
        lib.NativeType.__init__(self)

        self.window = tkinter.Tk()

    @classmethod
    def type_name__(cls) -> str:
        return "Window"

    def set_root(self, root: Graphic):
        root.tk.master = self.window
        root.tk.grid()

    def show(self):
        self.window.mainloop()
