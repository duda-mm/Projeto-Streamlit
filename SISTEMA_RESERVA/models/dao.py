import sqlite3
import pandas as pd
from models.usuario import Usuario
from models.sala import Sala

class UsuarioDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    def inserir(self, usuario):
        conn = self.db_manager.conectar()
        try:
            sql = "INSERT INTO Usuario (email, senha, tipo, nome) VALUES (?, ?, ?, ?)"
            conn.execute(sql, (usuario.email, usuario.senha, usuario.tipo, usuario.nome))
            conn.commit()
            return True, "Usuário cadastrado com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Erro: Email já cadastrado."
        except Exception as e:
            return False, f"Erro: {e}"
        finally:
            conn.close()
    def autenticar(self, email, senha):
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE email = ? AND senha = ?", (email, senha))
        row = cursor.fetchone()
        conn.close()
        if row: return Usuario(id_usuario=row[0], email=row[1], senha=row[2], tipo=row[3], nome=row[4])
        return None
    def listar_todos_df(self):
        conn = self.db_manager.conectar()
        try: df = pd.read_sql_query("SELECT id_usuario, nome, email, tipo FROM Usuario", conn)
        except: df = pd.DataFrame()
        conn.close()
        return df
    def listar_com_reservas_df(self):
        conn = self.db_manager.conectar()
        query = "SELECT DISTINCT u.id_usuario, u.nome, u.email, u.tipo FROM Usuario u INNER JOIN Reserva r ON u.id_usuario = r.id_usuario"
        try: df = pd.read_sql_query(query, conn)
        except: df = pd.DataFrame()
        conn.close()
        return df

class SalaDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    def listar_todas(self):
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sala")
        rows = cursor.fetchall()
        conn.close()
        return [Sala(*row) for row in rows]
    def listar_todas_df(self):
        conn = self.db_manager.conectar()
        try: df = pd.read_sql_query("SELECT * FROM Sala", conn)
        except: df = pd.DataFrame()
        conn.close()
        return df
    def inserir(self, sala):
        conn = self.db_manager.conectar()
        try:
            sql = "INSERT INTO Sala (nome, capacidade, descricao) VALUES (?, ?, ?)"
            conn.execute(sql, (sala.nome, sala.capacidade, sala.descricao))
            conn.commit()
            return True, "Sala salva com sucesso!"
        except Exception as e: return False, str(e)
        finally: conn.close()
    def excluir(self, id_sala):
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Reserva WHERE id_sala = ?", (id_sala,))
            qtd = cursor.fetchone()[0]
            if qtd > 0: return False, f"Impossível excluir: Sala possui {qtd} reserva(s) registradas."
            cursor.execute("DELETE FROM Sala WHERE id_sala = ?", (id_sala,))
            conn.commit()
            if cursor.rowcount > 0: return True, "Sala excluída com sucesso."
            else: return False, "Erro: Sala não encontrada."
        except Exception as e: return False, f"Erro técnico: {e}"
        finally: conn.close()
    def inserir_teste(self):
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM Sala")
        if cursor.fetchone()[0] == 0:
            salas = [("Auditório Principal", 100, "Projetor 4K"), ("Lab TI", 30, "PCs")]
            cursor.executemany("INSERT INTO Sala (nome, capacidade, descricao) VALUES (?, ?, ?)", salas)
            conn.commit()
        conn.close()

class ReservaDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    def inserir(self, id_usuario, id_sala, inicio, fim):
        conn = self.db_manager.conectar()
        try:
            check_sql = "SELECT * FROM Reserva WHERE id_sala = ? AND status != 'Negada' AND data_inicio < ? AND data_fim > ?"
            cursor = conn.cursor()
            cursor.execute(check_sql, (id_sala, fim, inicio))
            if cursor.fetchone(): return False, "Conflito de Agendamento: Sala já reservada neste horário."
            sql = "INSERT INTO Reserva (id_usuario, id_sala, data_inicio, data_fim) VALUES (?, ?, ?, ?)"
            conn.execute(sql, (id_usuario, id_sala, inicio, fim))
            conn.commit()
            return True, "Reserva solicitada com sucesso!"
        except Exception as e: return False, f"Erro: {e}"
        finally: conn.close()
    def listar_por_usuario(self, id_usuario):
        conn = self.db_manager.conectar()
        sql = "SELECT r.id_reserva, s.nome as Sala, r.data_inicio, r.data_fim, r.status FROM Reserva r JOIN Sala s ON r.id_sala = s.id_sala WHERE r.id_usuario = ?"
        try: df = pd.read_sql_query(sql, conn, params=(id_usuario,))
        except: df = pd.DataFrame()
        conn.close()
        return df
    def listar_todas_completo(self):
        conn = self.db_manager.conectar()
        sql = "SELECT r.id_reserva, u.nome as Usuario, s.nome as Sala, r.data_inicio, r.data_fim, r.status FROM Reserva r JOIN Sala s ON r.id_sala = s.id_sala JOIN Usuario u ON r.id_usuario = u.id_usuario"
        try: df = pd.read_sql_query(sql, conn)
        except: df = pd.DataFrame()
        conn.close()
        return df
    def listar_por_status(self, status):
        conn = self.db_manager.conectar()
        sql = "SELECT r.id_reserva, u.nome as Usuario, s.nome as Sala, r.data_inicio, r.data_fim, r.status FROM Reserva r JOIN Sala s ON r.id_sala = s.id_sala JOIN Usuario u ON r.id_usuario = u.id_usuario WHERE r.status = ?"
        try: df = pd.read_sql_query(sql, conn, params=(status,))
        except: df = pd.DataFrame()
        conn.close()
        return df
    def listar_avaliadas(self):
        conn = self.db_manager.conectar()
        sql = "SELECT r.id_reserva, u.nome as Usuario, s.nome as Sala, r.data_inicio, r.data_fim, r.status FROM Reserva r JOIN Sala s ON r.id_sala = s.id_sala JOIN Usuario u ON r.id_usuario = u.id_usuario WHERE r.status IN ('Confirmada', 'Negada')"
        try: df = pd.read_sql_query(sql, conn)
        except: df = pd.DataFrame()
        conn.close()
        return df
    def atualizar_status(self, id_reserva, novo_status):
        conn = self.db_manager.conectar()
        try:
            conn.execute("UPDATE Reserva SET status = ? WHERE id_reserva = ?", (novo_status, id_reserva))
            conn.commit()
            return True
        except: return False
        finally: conn.close()