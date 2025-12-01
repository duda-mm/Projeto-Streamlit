class Sala:
    def __init__(self, id, nome, capacidade, recursos, descrição):
        self.set_id(id)
        self.set_nome(nome)
        self.set_capacidade(capacidade)
        self.set_recursos(recursos)
        self.set_descrição(descrição)

    def set_id(self, id):
        if id < 0: raise ValueError("ID não pode ser negativo.")
        self.__id = id
    def set_nome(self, nome): 
        if nome == "": raise ValueError("Nome não pode ser vazio.")
        self.__nome = nome
    def set_capacidade(self, capacidade): 
        if capacidade < 0: raise ValueError("Capacidade não pode ser negativa.")
        self.__capacidade = capacidade
    def set_recursos(self, recursos): 
        if recursos == "": raise ValueError("Recursos não pode ser vazio.")
        self.__recursos = recursos
    def set_descricao(self, descricao): 
        if descricao == "": raise ValueError("Descrição não pode ser vazia.")
        self.__descricao = descricao

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_capacidade(self): return self.__capacidade
    def get_recursos(self): return self.__recursos
    def get_descricao(self): return self.__descricao