import streamlit as st

class AdminReservasUI:
    @staticmethod
    def render(controller):
        st.header("📅 Visão Geral de Agendamentos")
        df = controller.obter_todas_reservas()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Sem reservas no sistema.")