import streamlit as st

class LoginUI:
    @staticmethod
    def render(controller):
        st.header("Acesso ao Sistema")
        
        with st.form("form_login"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                controller.tentar_login(email, senha)