import pandas as pd

#concats the input file
def combiner(uploaded_files):
    combined_df = pd.DataFrame()
    for file in uploaded_files:
        df = pd.read_excel(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df

#drops unwanted columns
def drop_unnecessary_columns(df):
    columns_to_drop = ['College Roll no','Unproctored programming exam score out of 25', 'DOB', 'Email Id']
    df = df.drop(columns=columns_to_drop, errors='ignore')
    return df

#present and absent data
def present_absent_data(df):
    present_df = df[df['Present/Absent'] == 'Present']
    absent_df = df[df['Present/Absent'] == 'Absent']
    return present_df, absent_df

def segregate_data(df):
    faculty_df = df[df['Role'] == 'faculty']
    student_df = df[df['Role'] == 'student']
    return faculty_df, student_df


def filter_present(df):
    return df[df['Present/Absent'] == 'Present']

#main function 
def preprocess_data(uploaded_files):
    combined_df = combiner(uploaded_files)
    cleaned_df = drop_unnecessary_columns(combined_df)
    main_df= filter_present(cleaned_df)
    absent_df = present_absent_data(cleaned_df)
    faculty_df, student_df = segregate_data(main_df)
    return combined_df, cleaned_df, main_df, absent_df, faculty_df, student_df
