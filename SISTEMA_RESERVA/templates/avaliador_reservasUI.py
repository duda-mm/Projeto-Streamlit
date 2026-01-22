import streamlit as st
import time

class AvaliadorReservasUI:
    @staticmethod
    def render_pendentes(controller):
        st.header("Análise de Reservas (Pendentes)")
        df = controller.obter_reservas_pendentes()
        
        if df.empty:
            st.success("Nenhuma pendência!")
            return

        for index, row in df.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.markdown(f"**{row['Sala']}** | Solicitante: {row['Usuario']}")
                    st.caption(f"De: {row['Início']} | Até: {row['Fim']}")
                with c2:
                    if st.button("✅ Aprovar", key=f"ok_{row['ID']}"):
                        sucesso, msg = controller.mudar_status_reserva(row['ID'], "Confirmada")
                        if sucesso:
                            st.success(msg)
                            time.sleep(1.2)
                            st.rerun()
                        else:
                            st.error(msg)
                with c3:
                    if st.button("❌ Negar", key=f"no_{row['ID']}"):
                        sucesso, msg = controller.mudar_status_reserva(row['ID'], "Negada")
                        if sucesso:
                            st.success(msg)
                            time.sleep(1.2)
                            st.rerun()
                        else:
                            st.error(msg)

    @staticmethod
    def render_historico(controller):
        st.header("Histórico de Avaliações")
        df = controller.obter_reservas_avaliadas()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhuma avaliação feita.")