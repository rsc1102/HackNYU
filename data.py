import requests
import random
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import json

# CREATE A CUSTOMER
def create_customer(customer_deets):

    ''' # Use address in this format
    address  =  {
        "street_number" : "Jay St" ,
        "street_name" : "Jay St" ,
        "city" : "Brooklyn" ,
        "state" : "NY" ,
        "zip": "11201"
    } 
    
    # Use customer_deets in this format
    customer_deets =  {
        "first_name" : "John",
        "last_name" : "Doe",
        "address": address,
    }
    '''

    create_cust_url = "http://api.nessieisreal.com/customers?key={}".format(API_KEY)
    response = requests.post(create_cust_url,
                             data=json.dumps(customer_deets),
        headers={'content-type':'application/json'},
        )

# GET ALL CUSTOMERS
def get_all_customers():
    get_cust_url =  "http://api.nessieisreal.com/customers?key={}".format(API_KEY)
    response = requests.get(get_cust_url)
    return response.json()

# GET A CUSTOMER
def get_customer(customer_id):
    get_cust_url = "http://api.nessieisreal.com/customers/{}?key={}".format(customer_id, API_KEY)
    response = requests.get(get_cust_url)
    return response.json()
    #To get customer ID, use response.json()['objectCreated']['_id']

# CREATE ACCOUNT USING CUSTOMER ID
def create_account(customer_id, body):
    # Use body in this format
    # body = {
    #     "type": "Savings",
    #     "nickname": "test",
    #     "rewards": 10000,
    #     "balance": 10000,
    # }
    create_acc_url = "http://api.nessieisreal.com/customers/{}/accounts?key={}".format(customer_id, API_KEY)
    response = requests.post(create_acc_url,
                                json=body,
                                )
    return response.json()
    #To get account ID, use response.json()['objectCreated']['_id']

def create_merchant(body):
    create_merchant_url = "http://api.nessieisreal.com/merchants?key={}".format(API_KEY)
    ''' Use body in this format
    body = {
        "name": "string",
        "category": "string",
        "address": {
            "street_number": "string",
            "street_name": "string",
            "city": "string",
            "state": "string",
            "zip": "string"
        },
        "geocode": {
            "lat": 0,
            "lng": 0
        }
    } 
    '''
    def get_lat_lon(body):
        address = body['address']
        geolocator = Nominatim(user_agent="hackNYU")  # Set a unique user-agent
        location = geolocator.geocode(address)

        if location:
            return location.latitude, location.longitude
        else:
            return None

    body['geocode']['lat'], body['geocode']['lng'] = get_lat_lon(body)
    response = requests.post(create_merchant_url,
                             json=body,
                             )
    return response.json()
    #To get merchant ID, use response.json()['objectCreated']['_id']

def make_purchase(account_id, merchant_id, amount):
    make_purchase_url = "http://api.nessieisreal.com/accounts/{}/purchases?key={}".format(account_id, API_KEY)
    body = {
        "merchant_id": merchant_id,
        "medium": "balance",
        "purchase_date": datetime.now().isoformat(),
        "amount": amount,
        "status": "pending",
        "description": "test" # necessary for categorization of purchase
    }
