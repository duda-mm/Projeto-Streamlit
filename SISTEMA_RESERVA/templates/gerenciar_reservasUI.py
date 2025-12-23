import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta

class GerenciarReservasUI:
    @staticmethod
    def render(controller):
        st.header("⚙️ Gerenciar Reservas")
        st.info("Aqui você pode alterar ou cancelar reservas futuras (mínimo de 7 dias de antecedência).")

        usuario = st.session_state['usuario_logado']
        df_raw = controller.obter_minhas_reservas_raw(usuario.get_id_usuario())

        if df_raw.empty:
            st.warning("Você não possui reservas para gerenciar.")
            return

        df_raw['data_inicio'] = pd.to_datetime(df_raw['data_inicio'])
        agora = datetime.datetime.now()
        df_futuras = df_raw[df_raw['data_inicio'] >= agora].copy()

        if df_futuras.empty:
            st.warning("Nenhuma reserva futura encontrada.")
        else:
            opcoes_reservas = {}
            for idx, row in df_futuras.iterrows():
                fmt_data = row['data_inicio'].strftime('%d/%m/%Y %H:%M')
                label = f"{row['Sala']} | {fmt_data} ({row['status']})"
                opcoes_reservas[row['ID']] = label

            id_selecionado = st.selectbox(
                "Selecione a reserva:", 
                options=opcoes_reservas.keys(),
                format_func=lambda x: opcoes_reservas[x],
                placeholder="Selecione para ver opções...",
                index=None
            )

            if id_selecionado:
                reserva_sel = df_futuras[df_futuras['ID'] == id_selecionado].iloc[0]
                data_inicio_reserva = reserva_sel['data_inicio']
                
                data_limite_acao = agora + timedelta(days=7)
                pode_mexer = data_inicio_reserva >= data_limite_acao

                st.divider()

                if not pode_mexer:
                    dias_restantes = (data_inicio_reserva - agora).days
                    st.error("**Ação Bloqueada**")
                    st.write(f"Esta reserva é para daqui a **{dias_restantes} dias**.")
                    st.warning("Regra: Alterações apenas com 7 dias de antecedência.")
                else:
                    tab_edit, tab_del = st.tabs(["✏️ Editar", "🗑️ Cancelar"])

                    with tab_edit:
                        with st.form("form_editar_reserva"):
                            st.write("Novo Horário:")
                            nova_data = st.date_input("Nova Data", value=data_inicio_reserva.date())
                            c1, c2 = st.columns(2)
                            with c1:
                                novo_ini = st.time_input("Novo Início", value=data_inicio_reserva.time())
                            with c2:
                                novo_fim = st.time_input("Novo Fim", value=pd.to_datetime(reserva_sel['data_fim']).time())
                            
                            if st.form_submit_button("Salvar Alteração"):
                                controller.atualizar_reserva(
                                    id_selecionado, 
                                    reserva_sel['id_sala'], 
                                    nova_data, 
                                    novo_ini, 
                                    novo_fim,
                                    data_inicio_reserva
                                )

                    with tab_del:
                        st.write(f"Deseja cancelar: **{opcoes_reservas[id_selecionado]}**?")
                        if st.button("Confirmar Cancelamento", type="primary"):
                            controller.excluir_reserva(id_selecionado, data_inicio_reserva)