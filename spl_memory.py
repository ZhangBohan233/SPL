class Memory:
    def __init__(self):
        self.object_counter = 0
        self.store = 0

    def allocate(self):
        """
        returns the current pointer.

        :return:
        """
        p = self.object_counter
        self.object_counter += 1
        return p

    def store_status(self):
        self.store = self.object_counter

    def restore_status(self):
        self.object_counter = self.store


MEMORY = Memory()
