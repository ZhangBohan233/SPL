import tkinter


if __name__ == "__main__":
    root = tkinter.Tk()

    frame = tkinter.Frame()
    frame.master = root
    # setattr(frame, "master", root)

    ey = tkinter.Entry(frame)
    a = tkinter.Text(frame)
    a.grid()

    a.insert('end', "aaaaaaaaaaa")

    print(a.get("1.0", 'end'))

    menu = tkinter.Menu(root)
    file_menu = tkinter.Menu(menu)
    file_menu.add_command(label="Open", command=lambda: print(2))
    menu.add_cascade(label="File", menu=file_menu)
    root.configure(menu=menu)

    frame.grid()

    root.mainloop()
