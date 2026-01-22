import streamlit as st
import time

class PerfilUI:
    @staticmethod
    def render(controller):
        st.header("👤 Meus Dados")
        
        # Pega os dados atuais da sessão
        usuario_atual = st.session_state['usuario_logado']
        
        with st.container(border=True):
            with st.form("form_perfil"):
                st.subheader("Editar Informações")
                
                # Preenche os campos com os valores atuais
                novo_nome = st.text_input("Nome Completo", value=usuario_atual.get_nome())
                novo_email = st.text_input("E-mail", value=usuario_atual.get_email())
                nova_senha = st.text_input("Senha", value=usuario_atual.get_senha(), type="password")
                
                c1, c2 = st.columns([1, 4])
                with c1:
                    submitted = st.form_submit_button("Salvar Alterações")
                
                if submitted:
                    if not novo_nome or not novo_email or not nova_senha:
                        st.warning("Todos os campos são obrigatórios.")
                    else:
                        sucesso, msg, user_obj = controller.atualizar_usuario(
                            usuario_atual.get_id_usuario(),
                            novo_nome, 
                            novo_email, 
                            nova_senha,
                            usuario_atual.get_tipo()
                        )
                        
                        if sucesso:
                            # ATUALIZA A SESSÃO IMEDIATAMENTE
                            st.session_state['usuario_logado'] = user_obj
                            st.success(msg)
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)