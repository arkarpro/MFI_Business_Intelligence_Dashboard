import pandas as pd
import random

# Seed for reproducibility
random.seed(42)

# List of Regions, States, and Townships for Myanmar
regions = ['Lower Myanmar', 'Central Myanmar', 'Upper Myanmar']
states = {
    'Lower Myanmar': ['Yangon', 'Mon', 'Bago'],
    'Central Myanmar': ['Mandalay', 'Magway', 'Sagaing'],
    'Upper Myanmar': ['Kachin', 'Shan', 'Chin']
}

townships = {
    'Yangon': ['Hlaing', 'Sanchaung', 'Bahan', 'Kyauktada'],
    'Mon': ['Mawlamyine', 'Thaton', 'Kyaikto'],
    'Bago': ['Bago', 'Nyaunglaybin', 'Thegon'],
    'Mandalay': ['Mandalay', 'Chanmyathazi', 'Amarapura'],
    'Magway': ['Magway', 'Pakokku', 'Chauk'],
    'Sagaing': ['Sagaing', 'Monywa', 'Kalewa'],
    'Kachin': ['Myitkyina', 'Bhamo', 'Mohnyin'],
    'Shan': ['Taunggyi', 'Lashio', 'Kengtung'],
    'Chin': ['Hakha', 'Falam', 'Tedim']
}

# Core Branch Data
branches = []
branch_id = 1
for region in regions:
    for state in states[region]:
        for township in townships[state]:
            branches.append({
                'BranchID': branch_id,
                'Region': region,
                'State': state,
                'Township': township,
            })
            branch_id += 1

# Convert to DataFrame
branches_df = pd.DataFrame(branches)

# Client Data (150,000 clients)
clients = []
client_id = 1
for i in range(150000):
    branch = random.choice(branches)
    clients.append({
        'ClientID': client_id,
        'ClientName': f'Client {client_id}',
        'BranchID': branch['BranchID'],
        'Region': branch['Region'],
        'State': branch['State'],
        'Township': branch['Township'],
        'Age': random.randint(18, 60),
        'Gender': random.choice(['Male', 'Female']),
    })
    client_id += 1

# Convert to DataFrame
clients_df = pd.DataFrame(clients)

# Loan Data (280,000 loans)
loans = []
loan_id = 1
for i in range(280000):
    client = random.choice(clients)
    branch = clients_df.loc[clients_df['ClientID'] == client['ClientID'], 'BranchID'].values[0]
    loans.append({
        'LoanID': loan_id,
        'ClientID': client['ClientID'],
        'BranchID': branch,
        'LoanAmount': random.randint(500000, 10000000),  # Loan amount between 500,000 to 10,000,000 MMK
        'InterestRate': random.uniform(5, 15),  # Interest rate between 5% to 15%
        'DisbursementDate': pd.Timestamp.now() - pd.DateOffset(days=random.randint(0, 1800)),  # Loan issued between 0-5 years ago
        'LoanType': random.choice(['Personal', 'Business', 'Mortgage']),
        'Status': random.choice(['Active', 'Repaid', 'Overdue'])
    })
    loan_id += 1

# Convert to DataFrame
loans_df = pd.DataFrame(loans)

# Display the DataFrames
print(branches_df.head())
print(clients_df.head())
print(loans_df.head())