class B:
    def __init__(self):
        pass


class A(B):
    def __init__(self):
        B.__init__(self)

    def asd(self):
        pass

    def efg(self):
        pass

    def fgh(self):
        return self.efg()

    def jkl(self):
        return 1 + 2 + 3


if __name__ == "__main__":
    import time
    st = time.time()
    for i in range(1000000):
        A()
    end = time.time()
    print(end - st)
