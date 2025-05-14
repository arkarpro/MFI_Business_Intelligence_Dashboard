# Import necessary libraries
import pandas as pd  # For data manipulation and CSV export
import numpy as np  # For numerical operations
from faker import Faker  # For generating fake data
import random  # For randomization
from datetime import datetime, timedelta  # For date handling

# Initialize Faker with US context (English names)
fake = Faker('en_US')

# Set random seeds for reproducibility
np.random.seed(42)  # For numpy operations
random.seed(42)  # For Python's random module

# ======================
# 1. GEOGRAPHIC STRUCTURE
# ======================

# Myanmar's three main zones
zones = ['Lower', 'Upper', 'Central']  # Lower Myanmar has more economic activity

# Myanmar's states and regions
regions_states = [
    'Yangon', 'Mandalay', 'Ayeyarwady', 
    'Mon', 'Kayin', 'Shan', 
    'Sagaing', 'Bago', 'Magway', 
    'Tanintharyi'
]

# Real township names from different regions (50 total)
townships = [
    # Yangon Region townships
    'Hlaing', 'Insein', 'Kamayut', 'Bahan', 'Pazundaung',
    # Mandalay Region townships  
    'Chanayethazan', 'Mahar Aung Mye', 'Amarapura',
    # Ayeyarwady Region townships
    'Pathein', 'Myaungmya', 'Kyonpyaw',
    # Mon State townships
    'Mawlamyine', 'Chaungzon', 'Kyaikmaraw',
    # Kayin State townships
    'Hpa-an', 'Myawaddy', 'Kawkareik',
    # Shan State townships
    'Taunggyi', 'Lashio', 'Kengtung',
    # Sagaing Region townships
    'Monywa', 'Sagaing', 'Shwebo',
    # Bago Region townships
    'Bago', 'Pyay', 'Taungoo',
    # Magway Region townships
    'Magway', 'Pakokku', 'Gangaw',
    # Tanintharyi Region townships
    'Dawei', 'Myeik', 'Kawthaung'
] * 2  # Duplicate to get 50 townships

# =================
# 2. BRANCHES DATA
# =================
branches = []  # Empty list to store branch data

for i in range(1, 51):  # Generate 50 branches
    # Weight zones - Lower Myanmar has higher probability (45%)
    zone = random.choices(zones, weights=[0.45, 0.35, 0.2])[0]  
    
    # Randomly select a region/state
    region_state = random.choice(regions_states)
    
    # Create branch dictionary with all details
    branches.append({
        'branch_id': f'BR{i:03d}',  # Format as BR001, BR002 etc.
        'branch_name': f'{townships[i-1]} Branch',  # Township name + Branch
        'township': townships[i-1],  # Township name
        'region_state': region_state,  # State/Region
        'zone': zone,  # Lower/Upper/Central
        'opening_date': fake.date_between(start_date='-5y', end_date='-1y'),  # Opened 1-5 years ago
        'staff_count': random.randint(8, 25)  # Staff between 8-25
    })

# Convert branches list to pandas DataFrame
branch_df = pd.DataFrame(branches)

# =================
# 3. CLIENTS DATA
# =================
client_data = []  # Empty list for client data

for i in range(1, 110001):  # Generate 110,000 clients
    # Select a random branch for this client
    branch = random.choice(branches)
    
    # Random gender (50/50 distribution)
    gender = random.choice(['Male', 'Female'])
    
    # Generate gender-appropriate first name
    first_name = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
    last_name = fake.last_name()  # Random last name
    
    # Create client dictionary
    client_data.append({
        'client_id': f'CL{i:06d}',  # Format as CL000001, CL000002 etc.
        'branch_id': branch['branch_id'],  # Link to branch
        'name': f"{first_name} {last_name}",  # Full name
        'gender': gender,  # Male/Female
        'age': random.randint(21, 70),  # Age between 21-70
        # Occupation with weights (40% farmers)
        'occupation': random.choices(
            ['Farmer', 'Trader', 'Service', 'Manufacturing', 'Fishery'], 
            weights=[0.4, 0.3, 0.15, 0.1, 0.05]
        )[0],  
        # Loan count (most have 1-2 loans)
        'loan_count': min(np.random.poisson(1.5), 5),  
        # First loan date (within last 3 years)
        'first_loan_date': fake.date_between(start_date='-3y', end_date='today')
    })

# Convert to DataFrame
client_df = pd.DataFrame(client_data)

# ================
# 4. LOANS DATA
# ================
loan_products = ['Agri-Loan', 'SME', 'Microfinance', 'Digital-Loan']
loan_data = []  # Empty list for loan data

for _ in range(245000):  # Generate 245,000 loans
    # Select random client
    client = random.choice(client_data)
    
    # Find client's branch
    branch = next(b for b in branches if b['branch_id'] == client['branch_id'])
    
    # Select loan product (50% agriculture loans)
    product = random.choices(
        loan_products,
        weights=[0.5, 0.2, 0.25, 0.05]  # Weighted probabilities
    )[0]
    
    # Generate loan amount (100,000 - 5,000,000 MMK)
    amount = round(np.random.lognormal(12.5, 0.3), -3)
    
    # Loan status (~18% PAR)
    status = random.choices(
        ['Current', 'PAR30', 'PAR60', 'PAR90', 'Written-off'],
        weights=[0.82, 0.1, 0.05, 0.02, 0.01]
    )[0]
    
    # Create loan dictionary
    loan_data.append({
        'loan_id': f'LN{fake.unique.random_number(digits=8)}',  # 8-digit loan ID
        'client_id': client['client_id'],  # Link to client
        'branch_id': branch['branch_id'],  # Link to branch
        'product_type': product,  # Loan product
        'disbursement_date': fake.date_between(
            start_date=client['first_loan_date'], 
            end_date='today'
        ),  # Disbursed after client's first loan date
        'loan_amount': amount,  # Original loan amount
        # Outstanding balance (reduced if not current)
        'outstanding_balance': amount * random.uniform(0.1, 0.9) if status != 'Current' else amount * 0.95,
        'par_status': status,  # Loan status
        # Collateral value (only for Agri-Loan and SME)
        'collateral_value': amount * random.uniform(0.5, 2) if product in ['Agri-Loan', 'SME'] else 0
    })

# Convert to DataFrame
loan_df = pd.DataFrame(loan_data)

# =====================
# 5. FINANCIAL METRICS
# =====================
dates = pd.date_range('2022-01-01', '2024-12-31', freq='M')  # Monthly for 3 years
financials = []  # Empty list for financial data

for date in dates:  # For each month
    for branch in branches:  # For each branch
        base = branch['staff_count'] * 1500000  # Base metric scaled by staff
        
        # Create monthly financial record
        financials.append({
            'month': date.strftime('%Y-%m'),  # Format as YYYY-MM
            'branch_id': branch['branch_id'],  # Link to branch
            'disbursements': round(base * random.uniform(0.8, 1.5), -5),  # Disbursed amounts
            'collections': round(base * random.uniform(0.7, 1.3)),  # Collections
            'operating_expenses': round(base * 0.3 * random.uniform(0.9, 1.1)),  # Expenses
            'digital_transactions': random.randint(50, 300)  # Digital transactions
        })

# Convert to DataFrame
financial_df = pd.DataFrame(financials)

# ================
# 6. EXPORT DATA
# ================

# Export branches data
branch_df.to_csv('branches.csv', index=False)

# Export clients data (single file)
client_df.to_csv('clients.csv', index=False)

# Split and export large loan data (5 files)
for i, chunk in enumerate(np.array_split(loan_df, 5)):
    chunk.to_csv(f'loans_part_{i+1}.csv', index=False) 

# Split and export financial data (3 files)
for i, chunk in enumerate(np.array_split(financial_df, 3)):
    chunk.to_csv(f'financials_part_{i+1}.csv', index=False)

print("Data generation complete! Files saved to current directory.")