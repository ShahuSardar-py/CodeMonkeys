import streamlit as st
import pandas as pd
import plotly.express as px
from modules.preprocessor import preprocess_data

# Functions

# Counts values based on column and condition
def value_counter(df: pd.DataFrame, column: str, value: str) -> int:
    return df[column].value_counts().get(value, 0)

# Course counter
def course_info(df, column):
    return df[column].value_counts()

# Certificate counts based on type
def certification_counter(df, certificate_type: str):
    return (df['Certificate Type'] == certificate_type).sum()

# APP UI

st.set_page_config(page_title="InsightZ - NPTEL Report Generator",
                   page_icon="📈",
                   layout="wide")

# CUSTOM CSS for KPI boxes
st.markdown(
    """
    <style>
    .kpi-box {
        background-color: #141424;
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
        color: #e6e6e6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("InsightZ - NPTEL Report Generator")
st.write("V 1.2.2")

# SIDEBAR
uploaded_files = st.sidebar.file_uploader(
    "Upload the result files", 
    accept_multiple_files=True, 
    type=["xlsx", "xls"]
)

if uploaded_files:
    st.sidebar.success("File Upload Successful!")

    # Preprocessed data loaded
    combined_df, cleaned_df, main_df, absent_df, faculty_df, student_df = preprocess_data(uploaded_files)

    # Sidebar for department selection
    if 'Department' in main_df.columns:
        departments = ["All Departments"] + list(main_df['Department'].unique())
        selected_department = st.sidebar.selectbox("Filter by Department", departments)

        if selected_department == "All Departments":
            # Show general loaded data inside an expander if "All Departments" is selected
            with st.expander("General Loaded Data"):
                st.write(main_df)

        # Filter data based on department selection (for KPIs and charts)
        filtered_df = main_df[main_df['Department'] == selected_department] if selected_department != "All Departments" else main_df

        # Generate the KPIs and charts based on filtered or general data
        total_enrolled = filtered_df.shape[0]
        total_present = value_counter(filtered_df, 'Role', 'faculty') + value_counter(filtered_df, 'Role', 'student')
        faculty_count = value_counter(filtered_df, 'Role', 'faculty')
        student_count = value_counter(filtered_df, 'Role', 'student')

        # Additional KPIs for Elite and Silver Certification
        elite_faculty = certification_counter(filtered_df[filtered_df['Role'] == 'faculty'], 'Elite')
        elite_student = certification_counter(filtered_df[filtered_df['Role'] == 'student'], 'Elite')
        elite_silver_faculty = certification_counter(filtered_df[filtered_df['Role'] == 'faculty'], 'Elite+Silver')
        elite_silver_student = certification_counter(filtered_df[filtered_df['Role'] == 'student'], 'Elite+Silver')

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            st.markdown(f"""
            <div class="kpi-box">
                <h2>Total Enrolled</h2>
                <h1>{total_enrolled}</h1>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="kpi-box">
                <h2>Total Participants</h2>
                <h1>{total_present}</h1>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="kpi-box">
                <h2>Faculty</h2>
                <h1>{faculty_count}</h1>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="kpi-box">
                <h2>Students</h2>
                <h1>{student_count}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            fig_histogram = px.histogram(filtered_df, x="Department", title='Department wise enrollment')
            st.plotly_chart(fig_histogram, use_container_width=True)

            course_counts = course_info(filtered_df, 'Course Name')
            top_3_courses = course_counts.head(3)
            other_courses = course_counts.iloc[3:].sum()
            pie_data = top_3_courses._append(pd.Series({'Other': other_courses}))

            pie_chart = px.pie(pie_data, values=pie_data.values, names=pie_data.index, title='Top Courses')
            st.plotly_chart(pie_chart, use_container_width=True)

        with col3:
            st.markdown(f"""
            <div class="kpi-box">
                <h2>Elite (Faculty)</h2>
                <h1>{elite_faculty}</h1>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="kpi-box">
                <h2>Elite (Student)</h2>
                <h1>{elite_student}</h1>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="kpi-box">
                <h2>Elite+Silver (Faculty)</h2>
                <h1>{elite_silver_faculty}</h1>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="kpi-box">
                <h2>Elite+Silver (Student)</h2>
                <h1>{elite_silver_student}</h1>
            </div>
            """, unsafe_allow_html=True)

else:
    st.write("Please upload the files")
