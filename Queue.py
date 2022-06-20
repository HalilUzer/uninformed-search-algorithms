class FIFOFringe:

    def __init__(self) -> None:
        self.values = []


    def push(self, value):
        self.values.append(value)


    def pop(self):
        return self.values.pop(0)

    def is_empty(self):
        return len(self.values) == 0

    def is_not_empty(self):
        return len(self.values) != 0


    def __len__(self):
        return len(self.values)


class LIFOFringe:

    def __init__(self) -> None:
        self.values = []
        
    def push(self, value):
        self.values.append(value)

    def pop(self):
        return self.values.pop()

    def is_empty(self):
        return len(self.values) == 0

    def is_not_empty(self):
        return len(self.values) != 0

    def __len__(self):
        return len(self.values)