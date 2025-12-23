import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
from models.banco import BancoDados
from models.dao import UsuarioDAO, SalaDAO, ReservaDAO
from models.usuario import Usuario
from models.sala import Sala
from models.reserva import Reserva

class SistemaController:
    def __init__(self):
        self.db = BancoDados()
        self.db.criar_tabelas() 
        self.usuario_dao = UsuarioDAO(self.db)
        self.sala_dao = SalaDAO(self.db)
        self.reserva_dao = ReservaDAO(self.db)


    def _sucesso_e_reload(self, mensagem):
        st.success(mensagem)
        time.sleep(1.2)
        st.rerun()

    def _pode_alterar_cancelar(self, data_inicio_reserva):
        """Verifica se a ação está sendo feita com 7 dias de antecedência"""
      
        if isinstance(data_inicio_reserva, str):
            try:
                data_reserva = datetime.strptime(data_inicio_reserva, '%Y-%m-%d %H:%M:%S')
            except:
              
                data_reserva = pd.to_datetime(data_inicio_reserva)
        else:
            data_reserva = data_inicio_reserva

        agora = datetime.now()
        prazo_minimo = agora + timedelta(days=7)
        
        
        if data_reserva < prazo_minimo:
            return False
        return True

    def _formatar_df(self, df):
        if df.empty: return df
        
        df_visual = df.copy()
        
        if 'data_inicio' in df_visual.columns:
            df_visual['data_inicio'] = pd.to_datetime(df_visual['data_inicio'])
            df_visual['Início'] = df_visual['data_inicio'].dt.strftime('%d/%m/%Y %H:%M')
        
        if 'data_fim' in df_visual.columns:
            df_visual['data_fim'] = pd.to_datetime(df_visual['data_fim'])
            df_visual['Fim'] = df_visual['data_fim'].dt.strftime('%d/%m/%Y %H:%M')
            
        cols = [c for c in ['ID', 'Usuario', 'Sala', 'Início', 'Fim', 'status'] if c in df_visual.columns]
        if not cols: return df 
        return df_visual[cols]


    def tentar_login(self, email, senha):
        usuario = self.usuario_dao.autenticar(email, senha)
        if usuario:
            st.session_state['usuario_logado'] = usuario
            st.success(f"Bem-vindo, {usuario.get_nome()}!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Email ou senha incorretos.")

    def logout(self):
        st.session_state['usuario_logado'] = None
        st.rerun()

    def cadastrar_novo_usuario(self, nome, email, senha, tipo):
        novo_user = Usuario(None, nome, email, senha, tipo)
        sucesso, msg = self.usuario_dao.inserir(novo_user)
        if sucesso: st.success(msg)
        else: st.error(msg)

   
    def criar_sala(self, nome, capacidade, descricao):
        nova_sala = Sala(None, nome, capacidade, descricao)
        sucesso, msg = self.sala_dao.inserir(nova_sala)
        if sucesso: self._sucesso_e_reload(msg)
        else: st.error(msg)

    def atualizar_sala(self, id_sala, nome, cap, desc):
        sala = Sala(id_sala, nome, cap, desc)
        sucesso, msg = self.sala_dao.atualizar(sala)
        if sucesso: self._sucesso_e_reload(msg)
        else: st.error(msg)

    def excluir_sala(self, id_sala):
        sucesso, msg = self.sala_dao.excluir(id_sala)
        if sucesso: self._sucesso_e_reload(msg)
        else: st.error(msg)

    def obter_salas(self):
        return self.sala_dao.listar_todos()

    def obter_salas_df(self):
        return self.sala_dao.listar_todos_df()


    def criar_reserva(self, id_user, sala_obj, data, ini, fim):
        if ini >= fim:
            st.error("Horário final deve ser maior que o inicial.")
            return

        dt_ini = f"{data} {ini}"
        dt_fim = f"{data} {fim}"
        
        data_hora_reserva = datetime.combine(data, ini)
        if data_hora_reserva < datetime.now():
             st.error("Não é possível agendar para o passado.")
             return
        
        nova_reserva = Reserva(
            id_reserva=None,
            id_usuario=id_user,
            id_sala=sala_obj.get_id_sala(),
            data_inicio=dt_ini,
            data_fim=dt_fim
        )
        
        sucesso, msg = self.reserva_dao.inserir(nova_reserva)
        if sucesso: self._sucesso_e_reload(msg)
        else: st.error(msg)

 
    def atualizar_reserva(self, id_reserva, id_sala, data, ini, fim, data_original):
        if not self._pode_alterar_cancelar(data_original):
            st.error("Ação bloqueada pelo sistema: Necessário 7 dias de antecedência.")
            return

        if ini >= fim:
            st.error("Horário final deve ser maior que o inicial.")
            return

        dt_ini = f"{data} {ini}"
        dt_fim = f"{data} {fim}"

        sucesso, msg = self.reserva_dao.atualizar_datas(id_reserva, id_sala, dt_ini, dt_fim)
        if sucesso: self._sucesso_e_reload(msg)
        else: st.error(msg)

  
    def excluir_reserva(self, id_reserva, data_original):
        if not self._pode_alterar_cancelar(data_original):
            st.error("Ação bloqueada pelo sistema: Necessário 7 dias de antecedência.")
            return
        
        sucesso, msg = self.reserva_dao.excluir(id_reserva)
        if sucesso: self._sucesso_e_reload(msg)
        else: st.error(msg)

    def mudar_status_reserva(self, id_reserva, novo_status):
        if self.reserva_dao.mudar_status(id_reserva, novo_status):
            self._sucesso_e_reload(f"Reserva {novo_status}!")
        else:
            st.error("Erro ao atualizar status.")

    
    def obter_minhas_reservas_raw(self, id_user):
        return self.reserva_dao.listar_por_usuario(id_user)

   
    def obter_minhas_reservas(self, id_user):
        return self._formatar_df(self.reserva_dao.listar_por_usuario(id_user))

    def obter_reservas_pendentes(self):
        return self._formatar_df(self.reserva_dao.listar_por_status("Pendente"))

    def obter_reservas_avaliadas(self):
        return self._formatar_df(self.reserva_dao.listar_avaliadas())
        
    def obter_todas_reservas(self):
        return self._formatar_df(self.reserva_dao.listar_todas())