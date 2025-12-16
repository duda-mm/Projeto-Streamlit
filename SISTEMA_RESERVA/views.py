import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta, timezone
from models.banco import BancoDados
from models.dao import UsuarioDAO, SalaDAO, ReservaDAO
from models.usuario import Usuario
from models.sala import Sala

class SistemaController:
    def __init__(self):
        self.db = BancoDados()
        self.db.criar_tabelas() 
        self.usuario_dao = UsuarioDAO(self.db)
        self.sala_dao = SalaDAO(self.db)
        self.reserva_dao = ReservaDAO(self.db)
        self.sala_dao.inserir_teste()


    def _sucesso_e_reload(self, mensagem):
        st.success(mensagem)
        time.sleep(1.0)
        st.rerun()

    def _formatar_df(self, df):

        if df.empty:
            return df
      
        if 'data_inicio' in df.columns:
            df['data_inicio'] = pd.to_datetime(df['data_inicio'])
            df['Início'] = df['data_inicio'].dt.strftime('%d/%m/%Y %H:%M')
        
        if 'data_fim' in df.columns:
            df['data_fim'] = pd.to_datetime(df['data_fim'])
            df['Fim'] = df['data_fim'].dt.strftime('%d/%m/%Y %H:%M')

        
        colunas_visiveis = [col for col in ['id_reserva', 'Usuario', 'Sala', 'Início', 'Fim', 'status'] if col in df.columns]
        
       
        df_final = df[colunas_visiveis].rename(columns={
            'id_reserva': 'ID',
            'status': 'Status'
        })
        
        return df_final

  
    def tentar_login(self, email, senha):
        usuario = self.usuario_dao.autenticar(email, senha)
        if usuario:
            st.session_state['usuario_logado'] = usuario
            st.rerun()
        else:
            st.error("Email ou senha incorretos.")

    def logout(self):
        st.session_state['usuario_logado'] = None
        st.rerun()

    def cadastrar_novo_usuario(self, nome, email, senha, tipo):
        novo_user = Usuario(email=email, senha=senha, tipo=tipo, nome=nome)
        sucesso, msg = self.usuario_dao.inserir(novo_user)
        if sucesso: self._sucesso_e_reload(msg)
        else: st.error(msg)


    def obter_salas(self): return self.sala_dao.listar_todas()
    def obter_salas_df(self): return self.sala_dao.listar_todas_df()

    def criar_sala(self, nome, cap, desc):
        sucesso, msg = self.sala_dao.inserir(Sala(None, nome, cap, desc))
        if sucesso: self._sucesso_e_reload(msg)
        else: st.error(msg)

    def excluir_sala(self, id_sala):
        sucesso, msg = self.sala_dao.excluir(id_sala)
        if sucesso: self._sucesso_e_reload(msg)
        else: st.error(msg)

    def criar_reserva(self, id_user, sala, data, ini, fim):
      
        if str(ini) >= str(fim): 
            st.error("Horário inválido: Fim deve ser maior que início.")
            return

       
        fuso_brasilia = timezone(timedelta(hours=-3))
        agora_brasilia = datetime.now(fuso_brasilia).replace(tzinfo=None)
        
        data_hora_reserva = datetime.combine(data, ini)
        
        if data_hora_reserva < agora_brasilia:
            st.error(f"Não é possível agendar para o passado. (Horário atual: {agora_brasilia.strftime('%d/%m/%Y %H:%M')})")
            return

        dt_ini = f"{data} {ini}"
        dt_fim = f"{data} {fim}"
        
        sucesso, msg = self.reserva_dao.inserir(id_user, sala.id_sala, dt_ini, dt_fim)
        if sucesso: self._sucesso_e_reload(msg)
        else: st.error(msg)

  
    def obter_minhas_reservas(self, id): 
        df = self.reserva_dao.listar_por_usuario(id)
        return self._formatar_df(df)

    def obter_reservas_pendentes(self): 
        df = self.reserva_dao.listar_por_status("Pendente")
        return self._formatar_df(df)

    def obter_reservas_avaliadas(self): 
        df = self.reserva_dao.listar_avaliadas()
        return self._formatar_df(df)

    def obter_todas_reservas(self): 
        df = self.reserva_dao.listar_todas_completo()
        return self._formatar_df(df)
    
    def mudar_status_reserva(self, id_res, status):
        if self.reserva_dao.atualizar_status(id_res, status):
            self._sucesso_e_reload(f"Reserva {status} com sucesso!")
        else: st.error("Erro.")