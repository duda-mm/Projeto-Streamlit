import streamlit as st

class MinhasReservasUI:
    @staticmethod
    def render(controller):
        st.header("Minhas Reservas")
        usuario = st.session_state['usuario_logado']
        
        df = controller.obter_minhas_reservas(usuario.id_usuario)
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Você ainda não possui reservas.")