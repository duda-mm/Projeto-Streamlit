import sqlite3
import pandas as pd
from models.usuario import Usuario
from models.sala import Sala
from models.reserva import Reserva
from models.espaco import Espaco
from models.avaliador import Avaliador

class UsuarioDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def inserir(self, usuario):
        conn = self.db_manager.conectar()
        try:
            sql = "INSERT INTO Usuario (email, senha, tipo, nome) VALUES (?, ?, ?, ?)"
            conn.execute(sql, (usuario.get_email(), usuario.get_senha(), usuario.get_tipo(), usuario.get_nome()))
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
        sql = "SELECT id_usuario, nome, email, senha, tipo FROM Usuario WHERE email = ? AND senha = ?"
        cursor.execute(sql, (email, senha))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Usuario(row[0], row[1], row[2], row[3], row[4])
        return None

class AvaliadorDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def inserir(self, avaliador):
        conn = self.db_manager.conectar()
        try:
            sql = "INSERT INTO Avaliador (nome, email, senha, tipo) VALUES (?, ?, ?, ?)"
            conn.execute(sql, (avaliador.get_nome(), avaliador.get_email(), avaliador.get_senha(), avaliador.get_tipo()))
            conn.commit()
            return True, "Avaliador cadastrado com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Erro: Email já cadastrado."
        except Exception as e:
            return False, f"Erro: {e}"
        finally:
            conn.close()

    def listar_todos(self):
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_avaliador, nome, email, senha FROM Avaliador")
        rows = cursor.fetchall()
        conn.close()
        
        avaliadores = []
        for row in rows:
            avaliadores.append(Avaliador(row[0], row[1], row[2], row[3]))
        return avaliadores

class SalaDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def inserir(self, sala):
        conn = self.db_manager.conectar()
        try:
            sql = "INSERT INTO Sala (nome, capacidade, descricao) VALUES (?, ?, ?)"
            conn.execute(sql, (sala.get_nome(), sala.get_capacidade(), sala.get_descricao()))
            conn.commit()
            return True, "Sala cadastrada com sucesso!"
        except Exception as e:
            return False, f"Erro: {e}"
        finally:
            conn.close()

    def atualizar(self, sala):
        conn = self.db_manager.conectar()
        try:
            sql = "UPDATE Sala SET nome=?, capacidade=?, descricao=? WHERE id_sala=?"
            conn.execute(sql, (sala.get_nome(), sala.get_capacidade(), sala.get_descricao(), sala.get_id_sala()))
            conn.commit()
            return True, "Sala atualizada!"
        except Exception as e:
            return False, f"Erro ao atualizar: {e}"
        finally:
            conn.close()

    def excluir(self, id_sala):
        conn = self.db_manager.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Reserva WHERE id_sala = ?", (id_sala,))
            if cursor.fetchone()[0] > 0:
                return False, "Não é possível excluir: existem reservas para esta sala."
            
            cursor.execute("DELETE FROM Sala WHERE id_sala = ?", (id_sala,))
            conn.commit()
            return True, "Sala excluída com sucesso!"
        except Exception as e:
            return False, f"Erro: {e}"
        finally:
            conn.close()

    def listar_todos(self):
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_sala, nome, capacidade, descricao FROM Sala")
        rows = cursor.fetchall()
        conn.close()
        
        salas = []
        for row in rows:
            salas.append(Sala(row[0], row[1], row[2], row[3]))
        return salas
    
    def listar_todos_df(self):
        conn = self.db_manager.conectar()
        try:
            df = pd.read_sql_query("SELECT * FROM Sala", conn)
        except:
            df = pd.DataFrame()
        conn.close()
        return df

class EspacoDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def inserir(self, espaco):
        conn = self.db_manager.conectar()
        try:
            sql = "INSERT INTO Espaco (nome, capacidade, descricao) VALUES (?, ?, ?)"
            conn.execute(sql, (espaco.get_nome(), espaco.get_capacidade(), espaco.get_descricao()))
            conn.commit()
            return True, "Espaço cadastrado com sucesso!"
        except Exception as e:
            return False, f"Erro: {e}"
        finally:
            conn.close()

    def atualizar(self, espaco):
        conn = self.db_manager.conectar()
        try:
            sql = "UPDATE Espaco SET nome=?, capacidade=?, descricao=? WHERE id_espaco=?"
            conn.execute(sql, (espaco.get_nome(), espaco.get_capacidade(), espaco.get_descricao(), espaco.get_id_espaco()))
            conn.commit()
            return True, "Espaço atualizado!"
        except Exception as e:
            return False, f"Erro ao atualizar: {e}"
        finally:
            conn.close()

    def excluir(self, id_espaco):
        conn = self.db_manager.conectar()
        try:
           
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Espaco WHERE id_espaco = ?", (id_espaco,))
            conn.commit()
            return True, "Espaço excluído com sucesso!"
        except Exception as e:
            return False, f"Erro: {e}"
        finally:
            conn.close()

    def listar_todos(self):
        conn = self.db_manager.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_espaco, nome, capacidade, descricao FROM Espaco")
        rows = cursor.fetchall()
        conn.close()
        
        espacos = []
        for row in rows:
            espacos.append(Espaco(row[0], row[1], row[2], row[3]))
        return espacos

    def listar_todos_df(self):
        conn = self.db_manager.conectar()
        try:
            df = pd.read_sql_query("SELECT * FROM Espaco", conn)
        except:
            df = pd.DataFrame()
        conn.close()
        return df

class ReservaDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def inserir(self, reserva):
        conn = self.db_manager.conectar()
        try:
            sql_check = """
                SELECT COUNT(*) FROM Reserva 
                WHERE id_sala = ? AND status != 'Negada'
                AND (
                    (data_inicio < ? AND data_fim > ?) OR
                    (data_inicio >= ? AND data_inicio < ?) OR
                    (data_fim > ? AND data_fim <= ?)
                )
            """
            params = (
                reserva.get_id_sala(),
                reserva.get_data_fim(), reserva.get_data_inicio(),
                reserva.get_data_inicio(), reserva.get_data_fim(),
                reserva.get_data_inicio(), reserva.get_data_fim()
            )
            cursor = conn.cursor()
            cursor.execute(sql_check, params)
            if cursor.fetchone()[0] > 0:
                return False, "Horário indisponível para esta sala."

            sql = "INSERT INTO Reserva (id_usuario, id_sala, data_inicio, data_fim, status) VALUES (?, ?, ?, ?, ?)"
            conn.execute(sql, (
                reserva.get_id_usuario(), 
                reserva.get_id_sala(), 
                reserva.get_data_inicio(), 
                reserva.get_data_fim(),
                reserva.get_status()
            ))
            conn.commit()
            return True, "Reserva solicitada com sucesso!"
        except Exception as e:
            return False, f"Erro: {e}"
        finally:
            conn.close()

    def mudar_status(self, id_reserva, novo_status):
        conn = self.db_manager.conectar()
        try:
            conn.execute("UPDATE Reserva SET status=? WHERE id_reserva=?", (novo_status, id_reserva))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def _listar_base(self, where_clause="", params=()):
        conn = self.db_manager.conectar()
        sql = f"""
            SELECT r.id_reserva as ID, u.nome as Usuario, s.nome as Sala, 
                   r.data_inicio, r.data_fim, r.status 
            FROM Reserva r 
            JOIN Sala s ON r.id_sala = s.id_sala 
            JOIN Usuario u ON r.id_usuario = u.id_usuario 
            {where_clause}
            ORDER BY r.data_inicio DESC
        """
        try:
            df = pd.read_sql_query(sql, conn, params=params)
        except:
            df = pd.DataFrame()
        conn.close()
        return df

    def listar_por_usuario(self, id_usuario):
        return self._listar_base("WHERE r.id_usuario = ?", (id_usuario,))

    def listar_por_status(self, status):
        return self._listar_base("WHERE r.status = ?", (status,))

    def listar_avaliadas(self):
        return self._listar_base("WHERE r.status IN ('Confirmada', 'Negada')")
    
    def listar_todas(self):
        return self._listar_base()