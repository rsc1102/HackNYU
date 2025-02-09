import streamlit as st
import requests
import pandas as pd
import altair as alt
import json
import random
import string

def generate_random_alphanumeric_string(length):
  """Generates a random alphanumeric string of specified length."""
  characters = string.ascii_letters + string.digits
  return ''.join(random.choice(characters) for i in range(length))


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
        st.title("Promos")
        
        streak = 0
        for i in range(len(monthly_spend)-1,0,-1):
            if monthly_spend['Total Spend'][i] > monthly_spend['Total Spend'][i-1]:
                break
            streak += 1
        
        with open('Promos.json', 'r') as file:
            dictionary_list = json.load(file)
        
        cols = st.columns(6,border=True)
        
        for i,item in enumerate(random.sample(dictionary_list,6)):
            applied_streak = min(item['Max Streak'],streak)
            if applied_streak != 0:
                promo = {
                    "Partner":item['Partner'],
                    "Item":item['Item Name'],
                    "Price":item['Price'],
                    "Discount Applied":f"""{item[f"Streak {applied_streak} Discount"]}%""",
                    "New Price": item['Price'] - (item['Price']*item[f"Streak {applied_streak} Discount"]/100),
                    "Promo Code": generate_random_alphanumeric_string(6)
                }
                with cols[i]:
                    st.write(promo)
            
            
    with st.container(border=True):
        st.title("Your Spending Habits:")      
        col1, col2, col3 = st.columns([0.2,0.4,0.4],border=True)
        
        with col1:
            st.title("Streak 🔥")
            
                
            st.html(
                f"""
                <div style="display: flex; justify-content: center">
                    <span style='font-size: 84px; font-weight: bold;'>{streak}</span>
                </div>
                """
            )

        with col2:
            st.header("Monthly Trend")
            st.bar_chart(monthly_spend,x="Month",y="Total Spend")

        with col3:
            st.header("Spend Breakdown")
            chart = alt.Chart(latest_moth_spend).mark_arc().encode(
            theta="amount",
            color="category",
            tooltip=["category", "amount"]
        )

            # Display in Streamlit
            st.altair_chart(chart, use_container_width=True)
            