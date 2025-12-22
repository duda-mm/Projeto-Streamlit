import streamlit as st
import datetime
from datetime import timedelta, timezone

class ReservarUI:
    @staticmethod
    def render(controller):
        st.header("📅 Nova Reserva")
        salas = controller.obter_salas()

        opcoes_salas = {str(sala): sala for sala in salas}
        
        if not opcoes_salas:
            st.warning("Nenhuma sala cadastrada.")
            return

        fuso_brasilia = timezone(timedelta(hours=-3))
        hoje_brasilia = datetime.datetime.now(fuso_brasilia).date()

        with st.form("form_reserva"):
            c1, c2 = st.columns(2)
            with c1:
                sala_nome = st.selectbox("Escolha a Sala", list(opcoes_salas.keys()))
                data = st.date_input("Data da Reserva", min_value=hoje_brasilia, value=hoje_brasilia)
            with c2:
                inicio = st.time_input("Hora Início", datetime.time(9,0))
                fim = st.time_input("Hora Fim", datetime.time(10,0))
            
            sala_obj = opcoes_salas[sala_nome]
           
            st.caption(f"Info: {sala_obj.get_descricao()}")
            
            if st.form_submit_button("Solicitar Reserva"):
                usuario = st.session_state['usuario_logado']
                
                controller.criar_reserva(usuario.get_id_usuario(), sala_obj, data, inicio, fim)