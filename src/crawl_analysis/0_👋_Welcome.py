import streamlit as st
import streamlit_mermaid as stm

st.set_page_config(page_title="Welcome!", page_icon="👋")

st.markdown("# 爬蟲分析工具箱")

st.markdown("## 系統要求")
st.markdown("""
- Python 3.11+
- LINE 的爬蟲是 macOS only
- 部分模型需要 GPU 或 NPU 才能運作
""")

st.markdown("## 流程")
stm.st_mermaid("""
graph TB
    A[爬蟲] --> B[放入 MongoDB]
    B --> C[取出資料 / 正規化]
    C --> D[語意分析]
    C --> E[文字雲]
""", height="500px")
