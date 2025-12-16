import streamlit as st

class CadastroUI:
    @staticmethod
    def render(controller):
        st.header("📝 Novo Cadastro")
        
        with st.form("form_cadastro"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            tipo = st.selectbox("Tipo de Usuário", ["Usuário Comum", "Avaliador", "Administrador"])
            
            submit = st.form_submit_button("Cadastrar")
            
            if submit:
                if nome and email and senha:
                    controller.cadastrar_novo_usuario(nome, email, senha, tipo)
                else:
                    st.warning("Preencha todos os campos.")