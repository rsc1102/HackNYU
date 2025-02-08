import streamlit as st
import requests
import pandas as pd
import numpy as np
import altair as alt

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

pie_data = pd.DataFrame({
    'Category': ['Category A', 'Category B', 'Category C'],
    'Values': [40, 35, 25]
})

st.set_page_config(
        page_title="Smart Spend", 
        page_icon="Smart.png",
        layout="wide",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About':None
    }) 

st.html(
    """
    <div style="display: flex; justify-content: center">
        <span style='font-size: 84px; font-weight: bold;'>Smart Spend</span>
    </div>
    """
)


with st.form("my_form"):
    customer_id = st.text_input("Customer ID:",max_chars=24,placeholder="Your 24 character customer is...")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted: 
        if len(customer_id)!= 24:
            st.error("Customer ID needs to be 24 characters.")
            submitted = False
        url = 'http://api.nessieisreal.com/customers/{}/accounts?key={}'.format(customer_id,st.secrets['apiKey'])
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"Request failed with status code {response.status_code}")
        else:
            account_list = response.json()
            account_ids = [x["_id"] for x in account_list]
        
  
if submitted:      
    with st.container(border=True):
        st.title("Your Spending Habits:")      
        col1, col2 = st.columns(2,border=True)

        with col1:
            st.header("A cat")
            st.line_chart(chart_data)

        with col2:
            st.header("A dog")
            chart = alt.Chart(pie_data).mark_arc().encode(
            theta="Values",
            color="Category",
            tooltip=["Category", "Values"]
        )

            # Display in Streamlit
            st.altair_chart(chart, use_container_width=True)

    with st.container(border=True):
        col1,col2 = st.columns([0.3,0.7],border=True)
        
        with col1:
            st.title("Your Streak 🔥")
            
        with col2:
            st.title("Promos")