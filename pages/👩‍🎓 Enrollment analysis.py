import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Enrollment Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("InsightZ Enrollment Data Analyser")
st.write("V 1.3.0")

uploaded_files = st.sidebar.file_uploader(
    "Upload the result files",
    accept_multiple_files=True,
    type=["xlsx", "xls"]
)
for file in uploaded_files:
        df = pd.read_excel(file)
st.write("We are still tweaking things a  bit. Come back later :)")
if uploaded_files:
    st.sidebar.success("Files uploaded")

    with st.expander("Loaded data"):
        st.write(df)
    
    caste_count= df['SC/ST status'].sum()
    males= df['Gender'].value_counts()['male']
    females= df['Gender'].value_counts()['female']

    st.markdown(f"""
            <div class="kpi-box">
                <h2>Total SC/ST</h2>
                <h1>{caste_count}</h1>
            </div>
            """, unsafe_allow_html=True)
    st.markdown(f"""
            <div class="kpi-box">
                <h2>Total SC/ST</h2>
                <h1>{males }</h1>
            </div>
            """, unsafe_allow_html=True)
            
    
