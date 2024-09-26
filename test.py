import streamlit as st
import pandas as pd
import mysql.connector as sql


mydb = sql.connect(
    host = "localhost",
    user = "root",
    password = "root"
)
cursor = mydb.cursor()
cursor.execute('use test;')
date = st.date_input('Please select Date')
if date:
    formatted_date = date.strftime('%Y-%m')
    # st.write(date)
    st.write(formatted_date)
    query = 'Insert into test1 (date) values(%s);'
    cursor.execute(query,(date,))
    # mydb.commit()
    mydb.commit()