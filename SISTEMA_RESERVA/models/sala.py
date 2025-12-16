class Sala:
    def __init__(self, id_sala, nome, capacidade, descricao):
        self.id_sala = id_sala
        self.nome = nome
        self.capacidade = capacidade
        self.descricao = descricao
    
    def __str__(self):
        return f"{self.nome} | {self.capacidade} pessoa(s)"