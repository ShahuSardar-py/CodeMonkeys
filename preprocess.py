import pandas as pd

def load_and_combine_files(uploaded_files):
    combined_df = pd.DataFrame()
    
    for file in uploaded_files:
        df = pd.read_excel(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    return combined_df

def drop_unnecessary_columns(df):
    columns_to_drop = ['Unproctored programming exam score out of 25', 'DOB', 'College Roll Number']
    df = df.drop(columns=columns_to_drop, errors='ignore')
    return df

def segregate_data(df):
    faculty_df = df[df['Role'] == 'Faculty']
    student_df = df[df['Role'] == 'Student']
    return faculty_df, student_df

def calculate_presence(df):
    present_count = df['Attendance'].value_counts().get('Present', 0)
    absent_count = df['Attendance'].value_counts().get('Absent', 0)
    return present_count, absent_count

def preprocess_data(uploaded_files):
    combined_df = load_and_combine_files(uploaded_files)
    cleaned_df = drop_unnecessary_columns(combined_df)
    faculty_df, student_df = segregate_data(cleaned_df)
    faculty_present, faculty_absent = calculate_presence(faculty_df)
    student_present, student_absent = calculate_presence(student_df)
    
    return cleaned_df, faculty_df, student_df, faculty_present, faculty_absent, student_present, student_absent
