import streamlit as st
import pandas as pd
import plotly.express as px
from preprocessor import preprocess_data

# Functions
def value_counter(df: pd.DataFrame, column: str, value: str) -> int:
    return df[column].value_counts().get(value, 0)

def course_info(df, column):
    return df[column].value_counts()

# Custom CSS for KPI boxes
st.set_page_config(page_title="NPTEL Report Automator", layout="wide")
st.title("NPTEL Report Generator")
st.write("V 1.2.0")
st.markdown("""
    <style>
    .kpi-box {
        background-color: #f1f3f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .kpi-box h1 {
        font-size: 2.5em;
        margin: 0;
    }
    .kpi-box h2 {
        font-size: 1.2em;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# APP UI 


# Sidebar - File Uploader
uploaded_files = st.sidebar.file_uploader(
    "Upload the result files",
    accept_multiple_files=True,
    type=["xlsx", "xls"]
)

# Processing the uploaded files
if uploaded_files:
    st.write("Upload successful!")
    
    # Preprocess the data
    combined_df, cleaned_df, main_df, absent_df, faculty_df, student_df = preprocess_data(uploaded_files)
    
    with st.expander("Main Data"):
        st.write(main_df)

    # Create layout with three columns
    col1, col2, col3 = st.columns([1, 2, 1])

    # First Column - KPIs
    with col1:
        total_count = value_counter(main_df, 'Role', 'faculty') + value_counter(main_df, 'Role', 'student')
        faculty_count = value_counter(main_df, 'Role', 'faculty')
        student_count = value_counter(main_df, 'Role', 'student')

        st.markdown(f"""
        <div class="kpi-box">
            <h2>Total Participants</h2>
            <h1>{total_count}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="kpi-box">
            <h2>Faculty</h1>
            <h1>{faculty_count}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="kpi-box">
            <h2>Students</h2>
            <h1>{student_count}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        elite_faculty = (faculty_df['Certificate Type'] == 'Elite').sum()
        elite_student = (student_df['Certificate Type'] == 'Elite').sum()
        
        st.markdown(f"""
        <div class="kpi-box">
            <h2>Elite (Faculty)</h2>
            <h1>{elite_faculty}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="kpi-box">
            <h2>Elite (Students)</h2>
            <h1>{elite_student}</h1>
        </div>
        """, unsafe_allow_html=True)

    # Second Column - Graphs
    with col2:
        fig_histogram = px.histogram(main_df, x="Department", title='Department Distribution')
        st.plotly_chart(fig_histogram, use_container_width=True)
        
        course_counts = course_info(main_df, 'Course Name')
        top_3_courses = course_counts.head(3)
        other_courses = course_counts.iloc[3:].sum()
        pie_data = top_3_courses._append(pd.Series({'Other': other_courses}))
        st.divider()
        pie_chart = px.pie(pie_data, values=pie_data.values, names=pie_data.index, title='Top Courses')
        st.plotly_chart(pie_chart, use_container_width=True)

    # Third Column - Certification KPIs
    with col3:
        ES_faculty = (faculty_df['Certificate Type'] == 'Elite+Silver').sum()
        ES_student = (student_df['Certificate Type'] == 'Elite+Silver').sum()

        st.markdown(f"""
        <div class="kpi-box">
            <h2>Elite + Silver (Faculty)</h2>
            <h1>{ES_faculty}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="kpi-box">
            <h2>Elite + Silver (Students)</h2>
            <h1>{ES_student}</h1>
        </div>
        """, unsafe_allow_html=True)

        fdp_eligible = (faculty_df['FDP Eligible'] == 'Yes').sum()
        
        st.markdown(f"""
        <div class="kpi-box">
            <h2>FDP Eligible Faculty</h2>
            <h1>{fdp_eligible}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        toppers = (main_df['Topper'] == 'Yes').sum()
        
        st.markdown(f"""
        <div class="kpi-box">
            <h2>Top Performers</h2>
            <h1>{toppers}</h1>
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("Please upload the files")
