from faker import Faker
import csv
import random
from datetime import datetime
from pathlib import Path

fake = Faker()

def generate_data():

    today = datetime.now().strftime("%Y%m%d")

    output_path = Path(__file__).parent.parent.resolve().joinpath('data', 'output', f'data_{today}.csv')

    with open(output_path, 'w') as output:
        
        header = ['transactionId', 'userId', 'timestamp', 'amount', 'currency', 'city', 'country', 'merchantName', \
            'paymentMetod', 'ipAddress',]

        mywriter = csv.writer(output)

        mywriter.writerow(header)

        for r in range(1000):
            mywriter.writerow([fake.uuid4(), fake.user_name(), fake.date(), round(random.uniform(10, 1000), 2), \
                                random.choice(['USD', 'GBP']), fake.city(), fake.country(), fake.company(), \
                                    random.choice(['credit_card', 'debit_card', 'online_transfer']), fake.ipv4()])
            
    print(f'csv file created sucessfully at {output_path}')

    return str(output_path) #Returning filepath to Xcom
