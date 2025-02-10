from data import *
from faker import Faker

# Initialize the Faker object
fake = Faker()



# Function to generate a fake person with address
def generate_fake_customers():
    first_name = fake.first_name()
    last_name = fake.last_name()
    address = fake.address().split('\n')
    street_address = address[0]
    city_state_zip = address[1].split(',')
    city = city_state_zip[0].strip()
    state_zip = city_state_zip[1].strip().split(' ')
    state = state_zip[0]
    zipcode = state_zip[1]

    customer = {
        'first_name': first_name,
        'last_name': last_name,
        'address': {
            'street_name': street_address,
            'sreet_number': street_address.split(' ')[0],
            'city': city,
            'state': state,
            'zipcode': zipcode
        }
    }
    print(customer)

    return create_customer(customer)


# generate_fake_customers()


# print(get_all_customers())