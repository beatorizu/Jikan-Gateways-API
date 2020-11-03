class Character:
    def __init__(self, j):
        self.__dict__ = j

    def __str__(self):
        return str(self.__dict__)
