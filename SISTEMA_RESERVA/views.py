import pandas as pd
from datetime import datetime, timedelta, timezone
from models.banco import BancoDados
from models.dao import UsuarioDAO, SalaDAO, ReservaDAO
from models.usuario import Usuario
from models.sala import Sala
from models.reserva import Reserva

class SistemaController:
    def atualizar_usuario(self, id_usuario, nome, email, senha, tipo_original):
        # Cria um objeto temporário com os novos dados
        usuario_atualizado = Usuario(id_usuario, nome, email, senha, tipo_original)
        
        sucesso, msg = self.usuario_dao.atualizar(usuario_atualizado)
        return sucesso, msg, usuario_atualizado
    
    def __init__(self):
        self.db = BancoDados()
        self.db.criar_tabelas() 
        self.usuario_dao = UsuarioDAO(self.db)
        self.sala_dao = SalaDAO(self.db)
        self.reserva_dao = ReservaDAO(self.db)

    def _obter_agora_brasil(self):
        """Retorna a data/hora atual de Brasília sem info de fuso (naive) para comparações."""
        fuso_br = timezone(timedelta(hours=-3))
        return datetime.now(fuso_br).replace(tzinfo=None)

    def _pode_alterar_cancelar(self, data_inicio_reserva):
        """Verifica se a ação está sendo feita com 7 dias de antecedência (Fuso BR)."""
        if isinstance(data_inicio_reserva, str):
            try:
                data_reserva = datetime.strptime(data_inicio_reserva, '%Y-%m-%d %H:%M:%S')
            except:
                data_reserva = pd.to_datetime(data_inicio_reserva)
        else:
            data_reserva = data_inicio_reserva

       
        if hasattr(data_reserva, 'tzinfo') and data_reserva.tzinfo is not None:
            data_reserva = data_reserva.replace(tzinfo=None)

        agora = self._obter_agora_brasil()
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
        return self.usuario_dao.autenticar(email, senha)

    def cadastrar_novo_usuario(self, nome, email, senha, tipo):
        novo_user = Usuario(None, nome, email, senha, tipo)
        return self.usuario_dao.inserir(novo_user)

    def criar_sala(self, nome, capacidade, descricao):
        nova_sala = Sala(None, nome, capacidade, descricao)
        return self.sala_dao.inserir(nova_sala)

    def atualizar_sala(self, id_sala, nome, cap, desc):
        sala = Sala(id_sala, nome, cap, desc)
        return self.sala_dao.atualizar(sala)

    def excluir_sala(self, id_sala):
        return self.sala_dao.excluir(id_sala)

    def obter_salas(self):
        return self.sala_dao.listar_todos()

    def obter_salas_df(self):
        return self.sala_dao.listar_todos_df()

    def criar_reserva(self, id_user, sala_obj, data, ini, fim):
        if ini >= fim:
            return False, "Horário final deve ser maior que o inicial."

        dt_ini = f"{data} {ini}"
        dt_fim = f"{data} {fim}"
        
        
        data_hora_reserva = datetime.combine(data, ini)
        
        
        agora_br = self._obter_agora_brasil()
        
        if data_hora_reserva < agora_br:
             return False, "Não é possível agendar para o passado."
        
        nova_reserva = Reserva(
            id_reserva=None,
            id_usuario=id_user,
            id_sala=sala_obj.get_id_sala(),
            data_inicio=dt_ini,
            data_fim=dt_fim
        )
        
        return self.reserva_dao.inserir(nova_reserva)

    def atualizar_reserva(self, id_reserva, id_sala, data, ini, fim, data_original):
        if not self._pode_alterar_cancelar(data_original):
            return False, "Ação bloqueada pelo sistema: Necessário 7 dias de antecedência."

        if ini >= fim:
            return False, "Horário final deve ser maior que o inicial."

        dt_ini = f"{data} {ini}"
        dt_fim = f"{data} {fim}"

        return self.reserva_dao.atualizar_datas(id_reserva, id_sala, dt_ini, dt_fim)

    def excluir_reserva(self, id_reserva, data_original):
        if not self._pode_alterar_cancelar(data_original):
            return False, "Ação bloqueada pelo sistema: Necessário 7 dias de antecedência."
        
        return self.reserva_dao.excluir(id_reserva)

    def mudar_status_reserva(self, id_reserva, novo_status):
        if self.reserva_dao.mudar_status(id_reserva, novo_status):
            return True, f"Reserva {novo_status}!"
        else:
            return False, "Erro ao atualizar status."

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