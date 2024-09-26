import streamlit as st
import plotly.express as px
import pandas as pd

def plot_Graph_details(df):
    st.title(f'Graphs')

    df['dt'] = pd.to_datetime(df['dt'],format='%Y%m%d')

    # Initialize session state for selected_stock if it doesn't exist
    if 'selected_stock' not in st.session_state:
        st.session_state.selected_stock = df['name'].unique()[0]  

    selected_stock = st.selectbox('Select a stock', df['name'].unique())

    if selected_stock != st.session_state.selected_stock:
        st.session_state.selected_stock = selected_stock

    filtered_df = df.loc[df['name'] == st.session_state.selected_stock] 

  
    if not filtered_df.empty:
        plot_figure = px.bar(
            data_frame=filtered_df,
            x='dt',  
            y='stock_price',  
            labels={'dt': 'Date', 'stock_price': 'Stock Price'},
            title=f'Stock Price of {st.session_state.selected_stock} Over Time'
        )
        plot_figure.update_xaxes(
            title_text='Date',
            tickformat='%b %d',  
            tickmode='auto'
        )
        
        # date_range = pd.date_range(start=filtered_df['dt'].min(), end=filtered_df['dt'].max(), freq='7D')
        # plot_figure.update_xaxes(tickvals=date_range)


        st.plotly_chart(plot_figure)
    else:
        st.write(f'No data available for the selected stock: {st.session_state.selected_stock}')
        print(f'No data available for the selected stock: {st.session_state.selected_stock}')


def plot_Graph_summary(df, selected_code):
    if df is not None and not df.empty:
        if 'dt' in df.columns:
            df['dt'] = pd.to_datetime(df['dt'], format='%Y%m%d')

       
        filtered_summary_df = df[df['etf_code'] == selected_code]

        if not filtered_summary_df.empty:
            plot_figure = px.line(
                data_frame=filtered_summary_df,
                x='dt',
                y='outstanding',
                labels={'dt': 'Date', 'outstanding': 'Outstanding'},
                title=f'Outstanding for {selected_code}'
            )
            plot_figure.update_xaxes(
            title_text='Date',
            tickformat='%b %d',  
            tickmode='auto'
        )

            st.plotly_chart(plot_figure)
        else:
            st.write(f'No summary data found for {selected_code}.')
    else:
        st.write('No data available in the summary.')
    
