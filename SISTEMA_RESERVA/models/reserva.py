class Reserva:
    def __init__(self, id_reserva, id_usuario, id_sala, data_inicio, data_fim, status='Pendente'):
        self.set_id_reserva(id_reserva)
        self.set_id_usuario(id_usuario)
        self.set_id_sala(id_sala)
        self.set_data_inicio(data_inicio)
        self.set_data_fim(data_fim)
        self.set_status(status)
    
    def set_id_reserva(self, id_reserva):
        if id_reserva is not None and int(id_reserva) < 0: 
            raise ValueError('ID Reserva inválido')
        self.__id_reserva = id_reserva

    def get_id_reserva(self): 
        return self.__id_reserva
    
    def set_id_usuario(self, id_usuario):
        if int(id_usuario) < 0: 
            raise ValueError('ID Usuario inválido')
        self.__id_usuario = id_usuario

    def get_id_usuario(self): 
        return self.__id_usuario
    
    def set_id_sala(self, id_sala):
        if int(id_sala) < 0: 
            raise ValueError('ID Sala inválido')
        self.__id_sala = id_sala

    def get_id_sala(self): 
        return self.__id_sala
    
    def set_data_inicio(self, data_inicio):
        self.__data_inicio = str(data_inicio)

    def get_data_inicio(self): 
        return self.__data_inicio
    
    def set_data_fim(self, data_fim):
        self.__data_fim = str(data_fim)

    def get_data_fim(self): 
        return self.__data_fim

    def set_status(self, status):
        self.__status = status

    def get_status(self): 
        return self.__status
    
    def __str__(self):
        return f'ID: {self.__id_reserva} | STATUS: {self.__status} | INICIO: {self.__data_inicio} | FIM: {self.__data_fim}'