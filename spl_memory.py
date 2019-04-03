class Memory:
    def __init__(self):
        self.object_counter = 0

    def allocate(self):
        """
        returns the current pointer.

        :return:
        """
        p = self.object_counter
        self.object_counter += 1
        return p

    def free_last(self):
        self.object_counter -= 1


MEMORY = Memory()
