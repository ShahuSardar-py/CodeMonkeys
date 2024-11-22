import streamlit as st
st.set_page_config(
    page_title="InsightZ | NPTEL Report Generator",
    page_icon="📈",
)

st.write("# InsightZ | NPTEL Report Generator")

st.sidebar.success("Select App")

st.markdown(
    """
    Your one-stop app for turning raw NPTEL results into beautiful, insightful reports. Upload, analyze, and visualize all your academic data in just a few clicks!

    How to Use This App:

    ◻ Upload Your Files
    Head to the sidebar and upload your NPTEL result files in .xlsx or .xls format.

    ◻ View the Main Data
    After the files are successfully uploaded, expand the "Main Data" section to see the cleaned and combined data.

    ◻ Generate Your Report
    Click the "Generate Report" button to automatically create visual report.



    ◻ Export Your Report
    (Coming Soon!) You’ll be able to export the entire dashboard, including graphs, as a PDF.
"""
)

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: white;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #00010d;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed for Deptartment of Data Science & Cyber Security By  <a style='display: block; text-align: center;' href="https://github.com/ShahuSardar-py/" target="_blank">NekoDevs</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
