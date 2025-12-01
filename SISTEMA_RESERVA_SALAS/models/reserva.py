class Reserva:
    def __init__(self, id, data, id_usuario=0, id_sala=0, avaliacao=False):
        self.set_id(id)
        self.set_data(data)
        self.set_id_usuario(id_usuario)
        self.set_id_sala(id_sala)
        self.set_avaliacao(avaliacao)

    def set_id(self, id): 
        if id < 0: raise ValueError("ID não pode ser negativo.")
        self.__id = id
    def set_data(self, data):
        if data.year < datetime.today().year: raise ValueError("O ano não pode ser menor que o ano atual.")
        self.__data = data
    def set_id_usuario(self, id_usuario): 
        if id_usuario != None and id_usuario < 0: raise ValueError("O ID do usuário não pode ser negativo.")
        self.__id_usuario = id_usuario
    def set_id_sala(self, id_sala): 
        if id_sala != None and id_sala < 0: raise ValueError("O ID da sala não pode ser negativo.")
        self.__id_sala = id_sala
    def set_avaliacao(self, avaliacao):
        self.__avaliacao = avaliacao

    def get_id(self): 
        return self.__id
    def get_data(self): 
        return self.__data
    def get_id_usuario(self): 
        return self.__id_cliente
    def get_id_sala(self): 
        return self.__id_servico
    def get_avaliacao(self): 
        return self.__avaliacao