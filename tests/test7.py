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


class Int:
    def __init__(self, b):
        self.value: bytes = b

    def __add__(self, other):
        pass


if __name__ == "__main__":
    import time

    # for i in range(1000000):
    #     A()
    lst = []
    for i in range(1_000_000):
        lst.append(Int(i.to_bytes(8, "big")))
    st = time.time()
    for x in lst:
        y = x + x
    end = time.time()
    print(end - st)
