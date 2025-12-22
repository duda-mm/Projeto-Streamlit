class Espaco:
    def __init__(self, id_espaco, nome, capacidade, descricao):
        self.set_id_espaco(id_espaco)
        self.set_nome(nome)
        self.set_capacidade(capacidade)
        self.set_descricao(descricao)
    
    def set_id_espaco(self, id_espaco):
        if id_espaco is not None and int(id_espaco) < 0: 
            raise ValueError('ID inválido')
        self.__id_espaco = id_espaco

    def get_id_espaco(self):
        return self.__id_espaco
    
    def set_nome(self, nome):
        if not nome or str(nome).strip() == '': 
            raise ValueError('Nome inválido')
        self.__nome = nome

    def get_nome(self):
        return self.__nome
    
    def set_capacidade(self, capacidade):
        if int(capacidade) <= 0: 
            raise ValueError('Capacidade deve ser maior que zero')
        self.__capacidade = int(capacidade)

    def get_capacidade(self):
        return self.__capacidade
    
    def set_descricao(self, descricao):
        self.__descricao = descricao if descricao else ""

    def get_descricao(self):
        return self.__descricao
    
    def __str__(self):
        return f'ID: {self.__id_espaco} | ESPAÇO: {self.__nome} | CAPACIDADE: {self.__capacidade}'