import streamlit as st

class AdminSalasUI:
    @staticmethod
    def render(controller):
        st.header("Gerenciar Salas (Admin)")
        
        tab_visualizar, tab_criar, tab_atualizar, tab_excluir = st.tabs([
            "Visualizar", 
            "Criar", 
            "Atualizar", 
            "Excluir"
        ])

        df = controller.obter_salas_df()
        salas_objs = controller.obter_salas()
        
       
        opcoes_salas = {sala.get_id_sala(): f"{sala.get_nome()} (Cap: {sala.get_capacidade()})" for sala in salas_objs}

        with tab_visualizar:
            st.subheader("Visualizar Salas")
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhuma sala cadastrada.")

        with tab_criar:
            st.subheader("Nova Sala")
            with st.form("form_nova_sala", clear_on_submit=True):
                nome = st.text_input("Nome da Sala")
                cap = st.number_input("Capacidade", min_value=1, step=1)
                desc = st.text_area("Descrição")
                
                submitted = st.form_submit_button("Salvar Sala")
                if submitted:
                    controller.criar_sala(nome, cap, desc)

        with tab_atualizar:
            st.subheader("Atualizar Sala")
            
            if not salas_objs:
                st.warning("Nenhuma sala para atualizar.")
            else:
                id_sel_upd = st.selectbox(
                    "Selecione a Sala:", 
                    options=opcoes_salas.keys(), 
                    format_func=lambda x: opcoes_salas[x],
                    key="sb_atualizar"
                )
                
                
                sala_atual = next((s for s in salas_objs if s.get_id_sala() == id_sel_upd), None)
                
                if sala_atual:
                    with st.form("form_atualizar_sala"):
                        
                        novo_nome = st.text_input("Novo Nome", value=sala_atual.get_nome())
                        nova_cap = st.number_input("Nova Capacidade", min_value=1, value=sala_atual.get_capacidade())
                        nova_desc = st.text_area("Nova Descrição", value=sala_atual.get_descricao())
                        
                        if st.form_submit_button("Confirmar Alterações"):
                            controller.atualizar_sala(id_sel_upd, novo_nome, nova_cap, nova_desc)

        with tab_excluir:
            st.subheader("Excluir Sala")
            st.caption("Atenção: Apenas salas sem reservas podem ser excluídas.")
            
            if not salas_objs:
                st.info("Nenhuma sala disponível para exclusão.")
            else:
                id_sel_del = st.selectbox(
                    "Selecione a Sala para Excluir:", 
                    options=opcoes_salas.keys(), 
                    format_func=lambda x: opcoes_salas[x],
                    index=None,
                    placeholder="Selecione...",
                    key="sb_excluir"
                )
                
                if id_sel_del:
                    st.markdown(f"Tem certeza que deseja excluir **{opcoes_salas[id_sel_del]}**?")
                    if st.button("Confirmar Exclusão", type="primary"):
                        controller.excluir_sala(id_sel_del)