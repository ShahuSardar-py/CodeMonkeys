import streamlit as st
import pandas as pd
import plotly.express as px
from preprocessor import preprocess_data

# Functions

# Counts values
def value_counter(df: pd.DataFrame, column: str, value: str) -> int:
    return df[column].value_counts().get(value, 0)

# Course counter
def course_info(df, column):
    return df[column].value_counts()

# APP UI

st.set_page_config(page_title="Report Automator",
                   page_icon="📈",
                   layout="wide")

# CUSTOM CSS for KPI boxes
st.markdown(
    """
    <style>
    .kpi-box {
        background-color: #4a4e69;
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
        color: #dedede;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("InsightZ - NPTEL Report Generator")
st.write("V 1.2.2")

# SIDEBAR
# File uploader. (2 ideal)
uploaded_files = st.sidebar.file_uploader(
    "Upload the result files",
    accept_multiple_files=True,
    type=["xlsx", "xls"]
)

# For successful upload
if uploaded_files:

    st.sidebar.success("File Upload Successful!")

    # Preprocessed data loaded
    combined_df, cleaned_df, main_df, absent_df, faculty_df, student_df = preprocess_data(uploaded_files)

    # MAIN DATAFRAME
    with st.expander("Loaded Data"):
        st.write(main_df)

    # Button to generate analysis
    if st.button("Generate Report"):

        # Variables for count
        st.write("# Analysis Report")
        st.divider()

        # COLUMN LAYOUT
        col1, col2, col3 = st.columns([1, 2, 1])

        # Column 1 - KPI for counts
        with col1:
            total_enrolled = cleaned_df.shape[0]
            total_present = value_counter(main_df, 'Role', 'faculty') + value_counter(main_df, 'Role', 'student')
            faculty_count = value_counter(main_df, 'Role', 'faculty')
            student_count = value_counter(main_df, 'Role', 'student')

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

        # Column 2 - Graphs
        with col2:
            # HISTOGRAM
            fig_histogram = px.histogram(main_df, x="Department", title='Department wise enrollment')
            st.plotly_chart(fig_histogram, use_container_width=True)

            st.divider()

            # PIE CHART
            course_counts = course_info(main_df, 'Course Name')
            top_3_courses = course_counts.head(3)
            other_courses = course_counts.iloc[3:].sum()
            pie_data = top_3_courses._append(pd.Series({'Other': other_courses}))

            pie_chart = px.pie(pie_data, values=pie_data.values, names=pie_data.index, title='Top Courses')
            st.plotly_chart(pie_chart, use_container_width=True)

            with st.expander('About', expanded=True):
                st.caption('''
                    InsightZ- NPTEL report generator. 
                    V 1.2.6
                    A robust data analyser and report generator for NPTEL data
                    ♥
                        
        ''')
                st.markdown('<a href="https://github.com/ShahuSardar-py/CodeMonkeys" target="_blank">GitHub</a>', unsafe_allow_html=True)

        # Column 3 - Certification KPIs
        with col3:
            st.caption('Certification')

            elite_faculty = (faculty_df['Certificate Type'] == 'Elite').sum()
            st.markdown(f"""
            <div class="kpi-box">
                <h2>Elite (Faculty)</h2>
                <h1>{elite_faculty}</h1>
            </div>
            """, unsafe_allow_html=True)

            elite_student = (student_df['Certificate Type'] == 'Elite').sum()
            st.markdown(f"""
            <div class="kpi-box">
                <h2>Elite (Student)</h2>
                <h1>{elite_student}</h1>
            </div>
            """, unsafe_allow_html=True)

            ES_faculty = (faculty_df['Certificate Type'] == 'Elite+Silver').sum()
            ES_student = (student_df['Certificate Type'] == 'Elite+Silver').sum()
            st.markdown(f"""
            <div class="kpi-box">
                <h2>Elite+Silver (Faculty)</h2>
                <h1>{ES_faculty}</h1>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="kpi-box">
                <h2>Elite+Silver (Student)</h2>
                <h1>{ES_student}</h1>
            </div>
            """, unsafe_allow_html=True)

else:
    st.write("Please upload the files")
