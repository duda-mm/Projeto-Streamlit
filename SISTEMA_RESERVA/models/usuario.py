class Usuario:
    def __init__(self, id_usuario, nome, email, senha, tipo):
        self.set_id_usuario(id_usuario)
        self.set_nome(nome)
        self.set_email(email)
        self.set_senha(senha)
        self.set_tipo(tipo)
    
    def set_id_usuario(self, id_usuario):
        
        if id_usuario is not None and int(id_usuario) < 0: 
            raise ValueError('ID inválido')
        self.__id_usuario = id_usuario

    def get_id_usuario(self):
        return self.__id_usuario
    
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
        if not tipo or str(tipo).strip() == '': 
            raise ValueError('Tipo inválido')
        self.__tipo = tipo

    def get_tipo(self):
        return self.__tipo
    
    def __str__(self):
        return f'ID: {self.__id_usuario} | NOME: {self.__nome} | EMAIL: {self.__email} | TIPO: {self.__tipo}'