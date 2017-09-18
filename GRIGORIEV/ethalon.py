from func import euclidian_measure

class Reference:
    def __init__(self, num):
        self.num = num
        self.references = []

    def add_reference(self, reference):
        self.references.append(reference)

    def most_similar(self, vector):
        return min([euclidian_measure(_, vector) for _ in self.references])
