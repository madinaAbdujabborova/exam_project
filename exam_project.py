import pandas as pd
import seaborn as sns
import streamlit as st

st.write("# This data about *Courses*")

df = pd.read_csv("10.csv")

# Initialize session state for the toggle
if 'show_dataframe' not in st.session_state:
    st.session_state.show_dataframe = False

# Function to toggle the display of the DataFrame
def toggle_dataframe():
    st.session_state.show_dataframe = not st.session_state.show_dataframe

# Button to toggle DataFrame display
st.button("Data Frame", on_click=toggle_dataframe)

# Display the DataFrame based on the toggle state
if st.session_state.show_dataframe:
    st.write(df)

# Course_nameni nanlarini to'ldirish

course_id = df["Course_Name"].to_list()
for i in range(len(course_id)):
    if course_id[i] != str:
        course_id[i] = f'Course_{i+1}'

df['Course_Name_full'] = course_id
df.head(20)

