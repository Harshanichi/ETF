import streamlit as st
import mysql.connector as sql
from mysql.connector import Error
import pandas as pd
from datetime import date as dt
import plotly.express as px
from graph import plot_Graph_details,plot_Graph_summary


def connect_to_db():
    try:
        mydb = sql.connect(
            host="192.168.1.92",
            user="remotehost",
            password="Remote@123"
        )
        return mydb
    except Error as e:
        st.error(f"Error connecting to the database: {e}")
        return None


def fetch_etf_codes(cursor, formatted_date):
    query = 'SELECT etf_code FROM tsepcfsummary WHERE dt=%s'
    cursor.execute(query, (formatted_date,))
    etf_codes = cursor.fetchall()
    return [code[0] for code in etf_codes]


def fetch_etf_details(cursor, selected_code):
    query = 'SELECT * FROM tsepcfdetail WHERE etf_code=%s'
    cursor.execute(query, (selected_code,))
    details = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    if details:
        df = pd.DataFrame(details, columns=headers)
        df['dt'] = df['dt'].astype(str)
        df = df.drop(['etf_code', 'update_source', 'update_time'], axis=1)
        return df
    else:
        return None


def fetch_etf_summary(cursor, selected_code):
    query = 'SELECT * FROM tsepcfsummary WHERE etf_code=%s'
    cursor.execute(query, (selected_code,))
    summary = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    if summary:
        df_summary = pd.DataFrame(summary, columns=headers)
        df_summary['dt'] = df_summary['dt'].astype(str)
        df_summary = df_summary.drop(['update_source', 'update_time'], axis=1)
        return df_summary
    else:
        return None


# def display_etf_data(mydb, formatted_date):
#     cursor = mydb.cursor()
#     cursor.execute('USE jpx;')

#     etf_codes = fetch_etf_codes(cursor, formatted_date)
#     selected_code = st.selectbox('Select a code', etf_codes, None)
    
#     load = st.button("Load", type="primary")
#     tab1, tab2, graph = st.tabs(['Summary', 'Details', 'Graph'])
#     details_df = None
#     if load:
#         with st.spinner('Loading data...'):
#             # Fetch and display details
#             with tab2:
#                 details_df = fetch_etf_details(cursor, selected_code)
#                 if details_df is not None:
#                     st.title(f'Details for {selected_code}:')
#                     st.dataframe(details_df, hide_index=True)
#                 else:
#                     st.write('No data found for the selected ETF code and date.')
            
#             # Fetch and display summary
#             with tab1:
#                 summary_df = fetch_etf_summary(cursor, selected_code)
#                 if summary_df is not None:
#                     st.title(f'Summary for {selected_code}:')
#                     st.dataframe(summary_df, hide_index=True)
#                 else:
#                     st.write('No data found for the selected ETF code and date.')

#             # Display graph
#             with graph:
#                 details_df = fetch_etf_details(cursor, selected_code)
#                 if details_df is not None:
#                     plot_Graph(details_df)


def display_etf_data(mydb, formatted_date):
    cursor = mydb.cursor()
    cursor.execute('USE jpx;')

    etf_codes = fetch_etf_codes(cursor, formatted_date)
    selected_code = st.selectbox('Select a code', etf_codes, None)
    
    load = st.button("Load", type="primary")

    if 'details_df' not in st.session_state:
        st.session_state.details_df = None
    if 'summary_df' not in st.session_state:
        st.session_state.summary_df = None

    if load:
        with st.spinner('Loading data...'):
            st.session_state.details_df = fetch_etf_details(cursor, selected_code)
            st.session_state.summary_df = fetch_etf_summary(cursor, selected_code)

    tab1, tab2, graph = st.tabs(['Summary', 'Details', 'Graph'])

    with tab2:
        if st.session_state.details_df is not None:
            st.title(f'Details for {selected_code}:')
            st.dataframe(st.session_state.details_df, hide_index=True)
        else:
            st.write('No data found for the selected ETF code and date.')

    with tab1:
        if st.session_state.summary_df is not None:
            st.title(f'Summary for {selected_code}:')
            st.dataframe(st.session_state.summary_df, hide_index=True)
        else:
            st.write('No data found for the selected ETF code and date.')

    with graph:
        if st.session_state.details_df is not None:
            plot_Graph_details(st.session_state.details_df)
        if st.session_state.summary_df is not None:
            plot_Graph_summary(st.session_state.summary_df,selected_code)
            



def main():
    st.title('ETF')

    # Connect to the database
    mydb = connect_to_db()
    if not mydb:
        return

    date = st.date_input('Please select Date', value=None)
    today = dt.today()

    if date and date <= today:
        formatted_date = int(date.strftime('%Y%m%d'))
        display_etf_data(mydb, formatted_date)
    else:
        st.write('Please select a valid date in the past.')


if __name__ == "__main__":
    main()
