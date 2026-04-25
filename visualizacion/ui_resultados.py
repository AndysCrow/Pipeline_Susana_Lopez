import streamlit as st
import os


def mostrar_resultados() -> None:

    if "console_output" in st.session_state:
        st.subheader("Registro de ejecución")

        st.code(
            st.session_state["console_output"],
            language="text"
        )

    if "cleaned_df" in st.session_state:
        st.subheader("Vista previa del DataFrame limpio")

        st.dataframe(
            st.session_state["cleaned_df"].head(),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total de registros limpios: {len(st.session_state['cleaned_df'])}"
        )

    if "trace_df" in st.session_state:
        st.subheader("Vista previa de trazabilidad")

        st.dataframe(
            st.session_state["trace_df"].head(),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total de registros en trazabilidad: {len(st.session_state['trace_df'])}"
        )

    if "generated_files" in st.session_state:
        st.subheader("Archivos generados")

        archivos = st.session_state["generated_files"]

        if not archivos:
            st.info("No se detectaron archivos generados.")
            return

        for archivo in archivos:
            st.write(f"`{archivo}`")