# Repayments Table (tracking loan repayments)
repayments = []
repayment_id = 1
for i in range(100000):  # Assuming there are 100,000 repayment records
    loan = random.choice(loans)  # Randomly selecting a loan
    repayments.append({
        'RepaymentID': repayment_id,
        'LoanID': loan['LoanID'],
        'AmountPaid': random.randint(50000, loan['LoanAmount'] // 10),  # Random repayment amount (up to 10% of loan)
        'RepaymentDate': pd.Timestamp.now() - pd.DateOffset(days=random.randint(0, 1800)),  # Payment made between 0-5 years ago
    })
    repayment_id += 1

# Convert to DataFrame
repayments_df = pd.DataFrame(repayments)

# Reschedules Table (tracking loan reschedules)
reschedules = []
reschedule_id = 1
for i in range(50000):  # Assuming there are 50,000 reschedule records
    loan = random.choice(loans)  # Randomly selecting a loan
    reschedules.append({
        'RescheduleID': reschedule_id,
        'LoanID': loan['LoanID'],
        'NewDueDate': pd.Timestamp.now() + pd.DateOffset(days=random.randint(0, 365)),  # New due date within 1 year
        'RescheduleDate': pd.Timestamp.now() - pd.DateOffset(days=random.randint(0, 1800)),  # Rescheduled between 0-5 years ago
    })
    reschedule_id += 1

# Convert to DataFrame
reschedules_df = pd.DataFrame(reschedules)

# Write-Offs Table (tracking loan write-offs)
write_offs = []
write_off_id = 1
for i in range(20000):  # Assuming there are 20,000 write-off records
    loan = random.choice(loans)  # Randomly selecting a loan
    write_offs.append({
        'WriteOffID': write_off_id,
        'LoanID': loan['LoanID'],
        'WriteOffAmount': random.randint(loan['LoanAmount'] // 2, loan['LoanAmount']),  # Amount written off (between 50%-100% of loan)
        'WriteOffDate': pd.Timestamp.now() - pd.DateOffset(days=random.randint(0, 1800)),  # Write-off between 0-5 years ago
    })
    write_off_id += 1

# Convert to DataFrame
write_offs_df = pd.DataFrame(write_offs)

# Display the DataFrames for Repayments, Reschedules, and Write-Offs
print(repayments_df.head())
print(reschedules_df.head())
print(write_offs_df.head())