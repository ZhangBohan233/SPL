import tkinter


if __name__ == "__main__":
    root = tkinter.Tk()

    frame = tkinter.Frame()
    setattr(frame, "master", root)

    ey = tkinter.Entry(frame)
    a = tkinter.Text(frame)
    a.grid()

    a.insert('end', "aaaaaaaaaaa")

    print(a.get("1.0", 'end'))

    frame.pack()

    root.mainloop()
