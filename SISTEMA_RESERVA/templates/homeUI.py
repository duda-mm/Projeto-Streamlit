import streamlit as st

class HomeUI:
    @staticmethod
    def render(controller):
        usuario = st.session_state.get('usuario_logado')
        st.title(f"🏠 Painel Principal")
        st.write(f"Olá, **{usuario.get_nome()}**.")
        st.info("Utilize o menu lateral para acessar as funções do seu perfil.")