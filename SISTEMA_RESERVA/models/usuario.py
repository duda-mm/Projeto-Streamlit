class Usuario:
    def __init__(self, email, senha, tipo, nome, id_usuario=None):
        self.id_usuario = id_usuario
        self.email = email
        self.senha = senha
        self.tipo = tipo
        self.nome = nome