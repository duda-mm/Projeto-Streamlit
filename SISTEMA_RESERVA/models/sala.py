class Sala:
    def __init__(self, id_sala, nome, capacidade, descricao):
        self.set_id_sala(id_sala)
        self.set_nome(nome)
        self.set_capacidade(capacidade)
        self.set_descricao(descricao)
    
    def set_id_sala(self, id_sala):
        if id_sala is not None and int(id_sala) < 0: 
            raise ValueError('ID inválido')
        self.__id_sala = id_sala

    def get_id_sala(self):
        return self.__id_sala
    
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
        return f'ID: {self.__id_sala} | SALA: {self.__nome} | CAPACIDADE: {self.__capacidade}'