class Avaliador:
    def __init__(self, id_avaliador, nome, email, senha):
        self.set_id_avaliador(id_avaliador)
        self.set_nome(nome)
        self.set_email(email)
        self.set_senha(senha)
        self.set_tipo("Avaliador") 
    
    def set_id_avaliador(self, id_avaliador):
        if id_avaliador is not None and int(id_avaliador) < 0: 
            raise ValueError('ID inválido')
        self.__id_avaliador = id_avaliador

    def get_id_avaliador(self):
        return self.__id_avaliador
    
    def set_nome(self, nome):
        if not nome or str(nome).strip() == '': 
            raise ValueError('Nome inválido')
        self.__nome = nome

    def get_nome(self):
        return self.__nome
    
    def set_email(self, email):
        if not email or str(email).strip() == '': 
            raise ValueError('Email inválido')
        self.__email = email

    def get_email(self):
        return self.__email
    
    def set_senha(self, senha):
        if not senha or str(senha).strip() == '': 
            raise ValueError('Senha inválida')
        self.__senha = senha

    def get_senha(self):
        return self.__senha

    def set_tipo(self, tipo):
        self.__tipo = tipo

    def get_tipo(self):
        return self.__tipo
    
    def __str__(self):
        return f'ID: {self.__id_avaliador} | NOME: {self.__nome} | EMAIL: {self.__email} | TIPO: {self.__tipo}'