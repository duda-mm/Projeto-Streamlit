import streamlit as st
import time

class LoginUI:
    @staticmethod
    def render(controller):
        st.header("Acesso ao Sistema")
        
        with st.form("form_login"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                usuario = controller.tentar_login(email, senha)
                if usuario:
                    st.session_state['usuario_logado'] = usuario
                    st.success(f"Bem-vindo, {usuario.get_nome()}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Email ou senha incorretos.")