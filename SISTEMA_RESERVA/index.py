import streamlit as st
from views import SistemaController
from templates.loginUI import LoginUI
from templates.cadastroUI import CadastroUI
from templates.homeUI import HomeUI
from templates.reservarUI import ReservarUI
from templates.minhas_reservasUI import MinhasReservasUI
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
            tipo = usuario.get_tipo()
            
            if tipo == "Administrador":
                opcoes += ["Gerenciar Salas", "Todos Agendamentos", "Cadastrar Usuário"]
            elif tipo == "Avaliador":
                opcoes += ["Reservas Pendentes", "Reservas Avaliadas"]
            else: 
                opcoes += ["Nova Reserva", "Minhas Reservas"]

            escolha = st.selectbox("Selecione a tela:", options=opcoes)
            
            st.divider()
            if st.button("Sair", type="primary"): 
                controller.logout()

    
        if escolha == "Home": HomeUI.render(controller)
        elif escolha == "Nova Reserva": ReservarUI.render(controller)
        elif escolha == "Minhas Reservas": MinhasReservasUI.render(controller)
        elif escolha == "Gerenciar Salas": AdminSalasUI.render(controller)
        elif escolha == "Todos Agendamentos": AdminReservasUI.render(controller)
        elif escolha == "Cadastrar Usuário": CadastroUI.render(controller)
        elif escolha == "Reservas Pendentes": AvaliadorReservasUI.render_pendentes(controller)
        elif escolha == "Reservas Avaliadas": AvaliadorReservasUI.render_historico(controller)

if __name__ == "__main__":
    main()