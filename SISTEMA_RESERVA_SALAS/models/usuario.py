class Usuario:
    def __init__(self, id, nome, email, fone, senha):
        self.set_id(id)
        self.set_nome(nome)
        self.set_email(email)
        self.set_fone(fone)
        self.set_senha(senha)

    def set_id(self, id):
        if id < 0: raise ValueError("ID não pode ser negativo.")
        self.__id = id
    def set_nome(self, nome): 
        if nome == "": raise ValueError("Nome não pode ser vazio.")
        self.__nome = nome
    def set_email(self, email): 
        if email == "": raise ValueError("E-mail não pode ser vazio.")
        self.__email = email
    def set_fone(self, fone): 
        if fone == "": raise ValueError("Telefone não pode ser vazio.")
        self.__fone = fone
    def set_senha(self, senha): 
        if senha == "": raise ValueError("Senha não pode ser vazia.")
        self.__senha = senha

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_email(self): return self.__email
    def get_fone(self): return self.__fone
    def get_senha(self): return self.__senha