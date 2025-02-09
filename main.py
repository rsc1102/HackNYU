import streamlit as st
import requests
import pandas as pd
import altair as alt

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
    account_id = st.text_input("Account number:",max_chars=24,placeholder="Your 24 account number is...")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted: 
        if len(account_id)!= 24:
            st.error("Account number needs to be 24 characters.")
            submitted = False
        else:
            transactions = []
            url = "http://api.nessieisreal.com/accounts/{}/purchases?key={}".format(account_id,st.secrets['apiKey'])
            response = requests.get(url)
            if response.status_code == 200:
                transactions.extend(response.json())
            
            amount = []
            category = []
            purchase_date = []
            for transaction in transactions:
                amount.append(transaction['amount'])
                category.append(transaction['description'])
                purchase_date.append(transaction['purchase_date'])
      
            df = pd.DataFrame({"amount":amount,"category":category,"purchase_date":purchase_date})
            df["purchase_date"] = pd.to_datetime(df['purchase_date'])
            
            # Extract year and month and group by it
            monthly_spend = df.groupby(df['purchase_date'].dt.to_period('M'))['amount'].sum().reset_index()

            # Rename columns
            monthly_spend.columns = ['Month', 'Total Spend']

            # Convert 'Month' back to string for better readability
            monthly_spend['Month'] = monthly_spend['Month'].astype(str)
            
            df['Month'] = df['purchase_date'].dt.to_period("M")
            latest_month_transactions = df[df['Month'] == df['Month'].max()]
            latest_moth_spend = latest_month_transactions.groupby(latest_month_transactions['category'])['amount'].sum().reset_index()
                  
        
  
if submitted:      
    with st.container(border=True):
        col1,col2 = st.columns([0.3,0.7],border=True)
        
        with col1:
            st.title("Streak 🔥")
            streak = 0
            for i in range(len(monthly_spend)-1,0,-1):
                if monthly_spend['Total Spend'][i] > monthly_spend['Total Spend'][i-1]:
                    break
                streak += 1
                
            st.html(
                f"""
                <div style="display: flex; justify-content: center">
                    <span style='font-size: 84px; font-weight: bold;'>{streak}</span>
                </div>
                """
            )
            
            
        with col2:
            st.title("Promos")
            
            
    with st.container(border=True):
        st.title("Your Spending Habits:")      
        col1, col2 = st.columns(2,border=True)

        with col1:
            st.header("Monthly Trend")
            st.bar_chart(monthly_spend,x="Month",y="Total Spend")

        with col2:
            st.header("Spend Breakdown")
            chart = alt.Chart(latest_moth_spend).mark_arc().encode(
            theta="amount",
            color="category",
            tooltip=["category", "amount"]
        )

            # Display in Streamlit
            st.altair_chart(chart, use_container_width=True)
            