# Import necessary libraries
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker with US context
fake = Faker('en_US')

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

# ======================
# 1. GEOGRAPHIC STRUCTURE
# ======================

zones = ['Lower', 'Upper', 'Central']
regions_states = ['Yangon', 'Mandalay', 'Ayeyarwady', 'Mon', 'Kayin', 'Shan', 
                 'Sagaing', 'Bago', 'Magway', 'Tanintharyi']

townships = [
    'Hlaing', 'Insein', 'Kamayut', 'Bahan', 'Pazundaung',
    'Chanayethazan', 'Mahar Aung Mye', 'Amarapura',
    'Pathein', 'Myaungmya', 'Kyonpyaw',
    'Mawlamyine', 'Chaungzon', 'Kyaikmaraw',
    'Hpa-an', 'Myawaddy', 'Kawkareik',
    'Taunggyi', 'Lashio', 'Kengtung',
    'Monywa', 'Sagaing', 'Shwebo',
    'Bago', 'Pyay', 'Taungoo',
    'Magway', 'Pakokku', 'Gangaw',
    'Dawei', 'Myeik', 'Kawthaung'
] * 2

# =================
# 2. BRANCHES DATA
# =================
branches = []

for i in range(1, 51):
    zone = random.choices(zones, weights=[0.45, 0.35, 0.2])[0]
    region_state = random.choice(regions_states)
    branches.append({
        'branch_id': f'BR{i:03d}',
        'branch_name': f'{townships[i-1]} Branch',
        'township': townships[i-1],
        'region_state': region_state,
        'zone': zone,
        'opening_date': fake.date_between(start_date='-5y', end_date='-1y'),
        'staff_count': random.randint(8, 25)
    })

branch_df = pd.DataFrame(branches)

# =================
# 2. STAFF DATA (with Myanmar names)
# =================
staff_data = []

myanmar_first_names_male = [
    "Aung", "Min", "Kyaw", "Zaw", "Htun", "Win", "Myo", "Ko", "Thura", "Naing",
    "Soe", "Than", "Hla", "Moe", "Thein", "Yan", "Lin", "Zin", "Phyo", "Ye"
]

myanmar_first_names_female = [
    "Su", "Hla", "Khin", "Nwe", "Thida", "Myint", "Aye", "May", "Sandar", "Cho",
    "Thandar", "Yu", "Nu", "Khaing", "Phyu", "Thuzar", "Wai", "Hnin", "Yin", "Thet"
]

myanmar_last_names = [
    "Hlaing", "Aung", "Win", "Kyaw", "Zaw", "Htun", "Myint", "Thein", "Soe", "Moe",
    "Than", "Naing", "Yan", "Lin", "Zin", "Phyo", "Ye", "Oo", "Htet", "Khaing"
]

for branch in branches:
    # Generate branch manager
    gender = random.choice(['Male', 'Female'])
    if gender == 'Male':
        first_name = random.choice(myanmar_first_names_male)
    else:
        first_name = random.choice(myanmar_first_names_female)
    last_name = random.choice(myanmar_last_names)
    
    staff_data.append({
        'staff_id': f"ST{branch['branch_id'][2:]}001",
        'branch_id': branch['branch_id'],
        'name': f"{first_name} {last_name}",
        'gender': gender,
        'position': 'Branch Manager',
        'join_date': fake.date_between(start_date='-8y', end_date=branch['opening_date']),
        'salary': random.randint(800000, 1200000),
        'contact_number': f"09{random.randint(20000000, 99999999)}"  # Myanmar phone format
    })
    
    # Generate other staff members
    for i in range(2, branch['staff_count'] + 1):
        gender = random.choice(['Male', 'Female'])
        if gender == 'Male':
            first_name = random.choice(myanmar_first_names_male)
        else:
            first_name = random.choice(myanmar_first_names_female)
        last_name = random.choice(myanmar_last_names)
        
        staff_data.append({
            'staff_id': f"ST{branch['branch_id'][2:]}{i:03d}",
            'branch_id': branch['branch_id'],
            'name': f"{first_name} {last_name}",
            'gender': gender,
            'position': random.choice(['Loan Officer', 'Cashier', 'Accountant', 'Field Officer']),
            'join_date': fake.date_between(start_date=branch['opening_date'], end_date='today'),
            'salary': random.randint(400000, 800000),
            'contact_number': f"09{random.randint(20000000, 99999999)}"
        })

# Convert to DataFrame
staff_df = pd.DataFrame(staff_data)


# =================
# 4. CLIENTS DATA
# =================
client_data = []

for i in range(1, 110001):
    branch = random.choice(branches)
    gender = random.choice(['Male', 'Female'])
    first_name = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
    
    client_data.append({
        'client_id': f'CL{i:06d}',
        'branch_id': branch['branch_id'],
        'name': f"{first_name} {fake.last_name()}",
        'gender': gender,
        'age': random.randint(21, 70),
        'occupation': random.choices(
            ['Farmer', 'Trader', 'Service', 'Manufacturing', 'Fishery'], 
            weights=[0.4, 0.3, 0.15, 0.1, 0.05]
        )[0],
        'loan_count': min(np.random.poisson(1.5), 5),
        'first_loan_date': fake.date_between(start_date='-3y', end_date='today')
    })

client_df = pd.DataFrame(client_data)

# ================
# 5. LOANS DATA
# ================
loan_products = ['Agri-Loan', 'SME', 'Microfinance', 'Digital-Loan']
loan_data = []

for _ in range(245000):
    client = random.choice(client_data)
    branch = next(b for b in branches if b['branch_id'] == client['branch_id'])
    
    product = random.choices(
        loan_products,
        weights=[0.5, 0.2, 0.25, 0.05]
    )[0]
    
    amount = round(np.random.lognormal(12.5, 0.3), -3)
    
    status = random.choices(
        ['Current', 'PAR30', 'PAR60', 'PAR90', 'Written-off'],
        weights=[0.82, 0.1, 0.05, 0.02, 0.01]
    )[0]
    
    loan_data.append({
        'loan_id': f'LN{fake.unique.random_number(digits=8)}',
        'client_id': client['client_id'],
        'branch_id': branch['branch_id'],
        'product_type': product,
        'disbursement_date': fake.date_between(
            start_date=client['first_loan_date'], 
            end_date='today'
        ),
        'loan_amount': amount,
        'outstanding_balance': amount * random.uniform(0.1, 0.9) if status != 'Current' else amount * 0.95,
        'par_status': status,
        'collateral_value': amount * random.uniform(0.5, 2) if product in ['Agri-Loan', 'SME'] else 0
    })

loan_df = pd.DataFrame(loan_data)

# ==============================
# 6. LOAN REPAYMENT SCHEDULE DATA
# ==============================
repayment_data = []

for loan in loan_data:
    num_installments = min(36, max(12, int(loan['loan_amount'] / 500000) * 6))
    disbursement_date = pd.to_datetime(loan['disbursement_date'])
    installment_amount = loan['loan_amount'] / num_installments
    
    for i in range(1, num_installments + 1):
        due_date = disbursement_date + pd.DateOffset(months=i)
        is_paid = random.random() < 0.85 if i <= (num_installments * 0.8) else random.random() < 0.65
        payment_date = due_date + pd.DateOffset(days=random.randint(0, 30)) if is_paid else None
        
        repayment_data.append({
            'schedule_id': f"RS{loan['loan_id'][2:]}{i:03d}",
            'loan_id': loan['loan_id'],
            'client_id': loan['client_id'],
            'branch_id': loan['branch_id'],
            'installment_number': i,
            'due_date': due_date.strftime('%Y-%m-%d'),
            'principal_amount': round(installment_amount * 0.7, 2),
            'interest_amount': round(installment_amount * 0.3, 2),
            'total_due': round(installment_amount, 2),
            'paid_date': payment_date.strftime('%Y-%m-%d') if payment_date else None,
            'paid_amount': round(installment_amount * random.uniform(0.9, 1.1), 2) if is_paid else 0,
            'late_days': random.randint(1, 90) if is_paid and (payment_date - due_date).days > 0 else 0
        })

repayment_df = pd.DataFrame(repayment_data)

# =========================
# 7. CLIENT TRANSACTIONS DATA
# =========================
transaction_data = []
transaction_types = ['Deposit', 'Withdrawal', 'Loan Payment', 'Transfer']

for client in client_data[:30000]:  # First 30,000 clients only
    num_transactions = random.randint(1, 20)
    
    for _ in range(num_transactions):
        trans_type = random.choices(
            transaction_types,
            weights=[0.3, 0.3, 0.3, 0.1]
        )[0]
        
        if trans_type in ['Deposit', 'Withdrawal']:
            amount = round(random.uniform(10000, 500000), -3)
        elif trans_type == 'Loan Payment':
            amount = round(random.uniform(50000, 300000), -3)
        else:
            amount = round(random.uniform(100000, 1000000), -3)
        
        transaction_data.append({
            'transaction_id': f"TR{fake.unique.random_number(digits=8)}",
            'client_id': client['client_id'],
            'branch_id': client['branch_id'],
            'transaction_type': trans_type,
            'amount': amount,
            'transaction_date': fake.date_between(start_date=client['first_loan_date'], end_date='today'),
            'channel': random.choice(['Branch', 'Mobile App', 'Agent']),
            'related_loan': random.choice(loan_data)['loan_id'] if trans_type == 'Loan Payment' else None
        })

transaction_df = pd.DataFrame(transaction_data)

# ====================
# 8. BRANCH ASSETS DATA
# ====================
asset_data = []

for branch in branches:
    num_assets = random.randint(3, 8)
    
    for i in range(1, num_assets + 1):
        asset_type = random.choice(['Computer', 'Printer', 'Vehicle', 'Furniture', 'Safe', 'ATM'])
        purchase_date = fake.date_between(
            start_date=pd.to_datetime(branch['opening_date']) - pd.DateOffset(months=3),
            end_date='today'
        )
        
        asset_data.append({
            'asset_id': f"AS{branch['branch_id'][2:]}{i:03d}",
            'branch_id': branch['branch_id'],
            'asset_type': asset_type,
            'purchase_date': purchase_date,
            'purchase_value': round(random.uniform(500000, 5000000), -3),
            'current_value': round(random.uniform(100000, 3000000), -3),
            'condition': random.choice(['Excellent', 'Good', 'Fair', 'Poor']),
            'last_maintenance': fake.date_between(start_date=purchase_date, end_date='today')
        })

asset_df = pd.DataFrame(asset_data)

# =====================
# 9. FINANCIAL METRICS
# =====================
dates = pd.date_range('2022-01-01', '2024-12-31', freq='M')
financials = []

# Initialize portfolio tracker
portfolio_tracker = {}
for branch in branches:
    base_portfolio = branch['staff_count'] * 15000000
    portfolio_tracker[branch['branch_id']] = round(base_portfolio * random.uniform(0.8, 1.2))

for date in dates:
    for branch in branches:
        branch_id = branch['branch_id']
        staff_factor = branch['staff_count'] / 15
        
        disbursements = round(staff_factor * random.uniform(8, 15) * 1000000, -5)
        collections = round(portfolio_tracker[branch_id] * 0.1 * random.uniform(0.9, 1.1))
        
        portfolio_change = disbursements - collections
        portfolio_tracker[branch_id] = max(1000000, portfolio_tracker[branch_id] + portfolio_change)
        
        financials.append({
            'month': date.strftime('%Y-%m'),
            'branch_id': branch_id,
            'disbursements': disbursements,
            'collections': collections,
            'portfolio': round(portfolio_tracker[branch_id]),
            'operating_expenses': round(staff_factor * random.uniform(1.2, 1.8) * 1000000),
            'digital_transactions': random.randint(50, 300),
            'portfolio_growth': portfolio_change,
            'collection_rate': collections / (portfolio_tracker[branch_id] * 0.1)
        })

financial_df = pd.DataFrame(financials)

# ================
# 10. EXPORT DATA
# ================

# Export all tables
branch_df.to_csv('branches.csv', index=False)
staff_df.to_csv('staff.csv', index=False)
client_df.to_csv('clients.csv', index=False)

# Split large tables
for i, chunk in enumerate(np.array_split(loan_df, 5)):
    chunk.to_csv(f'loans_part_{i+1}.csv', index=False)

for i, chunk in enumerate(np.array_split(repayment_df, 5)):
    chunk.to_csv(f'repayments_part_{i+1}.csv', index=False)

for i, chunk in enumerate(np.array_split(transaction_df, 3)):
    chunk.to_csv(f'transactions_part_{i+1}.csv', index=False)

asset_df.to_csv('branch_assets.csv', index=False)

for i, chunk in enumerate(np.array_split(financial_df, 3)):
    chunk.to_csv(f'financials_part_{i+1}.csv', index=False)

print("All data generation complete! Files saved to current directory.")