import streamlit as st
import pandas as pd
import os

# File to store data
FILE_NAME = "data.csv"

# Load data
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    else:
        return pd.DataFrame(columns=["Name", "Department", "Month", "Score"])

# Save data
def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# Initialize
df = load_data()

st.title("📊 Employee Performance Tracker")

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Add Employee", "View Data", "Analytics"])

# ➤ Add Employee Section
if menu == "Add Employee":
    st.subheader("Add Employee Performance")

    name = st.text_input("Employee Name")
    department = st.selectbox("Department", ["HR", "IT", "Sales", "Finance"])
    month = st.selectbox("Month", 
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    score = st.slider("Performance Score", 0, 100)

    if st.button("Add Record"):
        new_data = pd.DataFrame([[name, department, month, score]], 
                                columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success("✅ Record Added Successfully!")

# ➤ View Data Section
elif menu == "View Data":
    st.subheader("Employee Data")

    if df.empty:
        st.warning("No data available")
    else:
        st.dataframe(df)

# ➤ Analytics Section
elif menu == "Analytics":
    st.subheader("Performance Analysis")

    if df.empty:
        st.warning("No data available for analysis")
    else:
        # Average Score
        st.write("### 📌 Average Score by Department")
        dept_avg = df.groupby("Department")["Score"].mean()
        st.bar_chart(dept_avg)

        # Monthly Trend
        st.write("### 📌 Monthly Performance Trend")
        month_avg = df.groupby("Month")["Score"].mean()
        st.line_chart(month_avg)

        # Top Performer
        st.write("### 🏆 Top Performer")
        top = df.sort_values(by="Score", ascending=False).head(1)
        st.dataframe(top)