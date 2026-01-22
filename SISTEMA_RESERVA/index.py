import streamlit as st
import time
from views import SistemaController
from templates.loginUI import LoginUI
from templates.cadastroUI import CadastroUI
from templates.homeUI import HomeUI
from templates.reservarUI import ReservarUI
from templates.minhas_reservasUI import MinhasReservasUI
from templates.gerenciar_reservasUI import GerenciarReservasUI 
from templates.admin_salasUI import AdminSalasUI
from templates.admin_reservasUI import AdminReservasUI
from templates.avaliador_reservasUI import AvaliadorReservasUI

st.set_page_config(page_title="Sistema de Reservas", layout="wide")

def main():
    if 'controller' not in st.session_state:
        st.session_state.controller = SistemaController()
    controller = st.session_state.controller

    if 'usuario_logado' not in st.session_state:
        st.session_state['usuario_logado'] = None
    usuario = st.session_state['usuario_logado']

    if usuario is None:
        tab1, tab2 = st.tabs(["Login", "Criar Conta"])
        with tab1: LoginUI.render(controller)
        with tab2: CadastroUI.render(controller)
    else:
        with st.sidebar:
            st.title("Menu Principal")
            st.markdown(f"**{usuario.get_nome()}**")
            st.caption(f"Cargo: {usuario.get_tipo()}")
            st.divider()
            
            opcoes = ["Home"]
            
            if usuario.get_tipo() == "Administrador":
                opcoes += ["Gerenciar Salas", "Todos Agendamentos", "Cadastrar Usuário"]
            elif usuario.get_tipo() == "Avaliador":
                opcoes += ["Reservas Pendentes", "Reservas Avaliadas"]
            else: 
              
                opcoes += ["Nova Reserva", "Minhas Reservas", "Gerenciar Reservas"]

            escolha = st.selectbox("Navegação:", options=opcoes)
            
            st.divider()
            if st.sidebar.button("Sair"):
                st.session_state['usuario_logado'] = None
                time.sleep(1)
                st.rerun()

        if escolha == "Home": HomeUI.render(controller)
        elif escolha == "Nova Reserva": ReservarUI.render(controller)
        elif escolha == "Minhas Reservas": MinhasReservasUI.render(controller)
        elif escolha == "Gerenciar Reservas": GerenciarReservasUI.render(controller)
        elif escolha == "Gerenciar Salas": AdminSalasUI.render(controller)
        elif escolha == "Todos Agendamentos": AdminReservasUI.render(controller)
        elif escolha == "Cadastrar Usuário": CadastroUI.render(controller)
        elif escolha == "Reservas Pendentes": AvaliadorReservasUI.render_pendentes(controller)
        elif escolha == "Reservas Avaliadas": AvaliadorReservasUI.render_historico(controller)

if __name__ == "__main__":
    main()