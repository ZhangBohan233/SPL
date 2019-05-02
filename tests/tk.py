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

    # hbox.master = frame
    t2 = tkinter.Label(hbox)
    t2.configure(text="text")
    # t2.master = hbox
    t2.grid()
    b3 = tkinter.Button(hbox)
    b3.configure(text="btn")
    # b3.master = hbox
    b3.grid(row=0, column=1)
    # hbox.configure(master=frame)
    # # setattr(hbox, "master", frame)

    hbox.grid(row=0)

    frame.grid()

    root.mainloop()
