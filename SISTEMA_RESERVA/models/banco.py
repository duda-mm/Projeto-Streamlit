import sqlite3

class BancoDados:
    def __init__(self, nome_banco="gestao_reservas.db"):
        self.nome_banco = nome_banco

    def conectar(self):
        return sqlite3.connect(self.nome_banco, check_same_thread=False)

    def criar_tabelas(self):
        conexao = self.conectar()
        cursor = conexao.cursor()
        
        sqls = [
            """CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(100) NOT NULL UNIQUE,
                senha VARCHAR(100) NOT NULL,
                tipo VARCHAR(50) NOT NULL,
                nome VARCHAR(150) NOT NULL
            );""",
            """CREATE TABLE IF NOT EXISTS Sala (
                id_sala INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL,
                capacidade INTEGER NOT NULL,
                descricao VARCHAR(255)
            );""",
            """CREATE TABLE IF NOT EXISTS Reserva (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_sala INTEGER NOT NULL,
                data_inicio DATETIME NOT NULL,
                data_fim DATETIME NOT NULL,
                status VARCHAR(20) DEFAULT 'Pendente',
                FOREIGN KEY(id_usuario) REFERENCES Usuario(id_usuario),
                FOREIGN KEY(id_sala) REFERENCES Sala(id_sala)
            );"""
        ]
        for sql in sqls:
            cursor.execute(sql)
        conexao.commit()
        conexao.close()