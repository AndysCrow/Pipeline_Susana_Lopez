import streamlit as st
import os


def mostrar_resultados() -> None:

    if "console_output" in st.session_state:
        st.subheader("Registro de ejecución")
        st.code(st.session_state["console_output"], language="text")

    if "cleaned_df" in st.session_state:
        st.subheader("Vista previa del DataFrame limpio")
        st.dataframe(
            st.session_state["cleaned_df"].head(),
            use_container_width=True,
            hide_index=True
        )
        st.caption(f"Total de registros limpios: {len(st.session_state['cleaned_df'])}")

    if "trace_df" in st.session_state:
        st.subheader("Vista previa de trazabilidad")
        st.dataframe(
            st.session_state["trace_df"].head(),
            use_container_width=True,
            hide_index=True
        )
        st.caption(f"Total de registros en trazabilidad: {len(st.session_state['trace_df'])}")

    # ── Validaciones ──────────────────────────────────────────────────────────
    if "validation_df" in st.session_state and st.session_state["validation_df"] is not None:
        st.subheader("✅ Validación del proceso")

        aprobadas = (st.session_state["validation_df"]["estado"].str.contains("APROBADO")).sum()
        total     = len(st.session_state["validation_df"])
        todo_ok   = st.session_state.get("validation_ok", False)

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Validaciones aprobadas", aprobadas)
        col_b.metric("Validaciones fallidas",  total - aprobadas)
        col_c.metric("Total ejecutadas",        total)

        if todo_ok:
            st.success("Todas las validaciones aprobadas. Los datos son confiables para análisis epidemiológico.")
        else:
            st.warning("Una o más validaciones fallaron. Revisa la tabla para identificar los problemas.")

        # Colorear filas según estado
        def colorear_fila(row):
            color = "#D1FAE5" if "APROBADO" in row["estado"] else "#FEE2E2"
            return [f"background-color: {color}"] * len(row)

        st.dataframe(
            st.session_state["validation_df"].style.apply(colorear_fila, axis=1),
            use_container_width=True,
            hide_index=True
        )

    # ── Descargas ──────────────────────────────────────────────────────────────
    if "generated_files" in st.session_state:
        st.subheader("Archivos generados")

        archivos: dict[str, bytes] = st.session_state["generated_files"]

        if not archivos:
            st.info("No se detectaron archivos generados.")
            return

        for nombre, contenido in archivos.items():
            st.download_button(
                label=f"⬇ Descargar {nombre}",
                data=contenido,
                file_name=nombre,
                mime="text/csv",
                key=nombre,
            )