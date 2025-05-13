# Portfolio Performance Metrics

# Total Repayments: Sum of all repayments made
total_repayments = repayments_df['AmountPaid'].sum()

# Total Write-Offs: Sum of all write-offs
total_write_offs = write_offs_df['WriteOffAmount'].sum()

# Rescheduled Loans: Count of loans that have been rescheduled
rescheduled_loans_count = reschedules_df['LoanID'].nunique()

# Non-Performing Loans (NPLs): Loans that are 90+ days overdue
# Assuming we consider loans that are 90 days overdue as NPLs
npl_loans = loans_df[loans_df['LoanID'].isin(repayments_df[repayments_df['RepaymentDate'] < (pd.Timestamp.now() - pd.DateOffset(days=90))]['LoanID'])]

# Calculating NPL ratio
npl_ratio = len(npl_loans) / len(loans_df) * 100

# Performance Report by Branch
branch_performance = loans_df.groupby('BranchID').agg(
    TotalLoans=('LoanID', 'count'),
    TotalAmount=('LoanAmount', 'sum'),
    TotalRepayments=('LoanID', lambda x: repayments_df[repayments_df['LoanID'].isin(x)]['AmountPaid'].sum()),
    TotalWriteOffs=('LoanID', lambda x: write_offs_df[write_offs_df['LoanID'].isin(x)]['WriteOffAmount'].sum())
).reset_index()

# Performance Report by Region
region_performance = loans_df.groupby('Region').agg(
    TotalLoans=('LoanID', 'count'),
    TotalAmount=('LoanAmount', 'sum'),
    TotalRepayments=('LoanID', lambda x: repayments_df[repayments_df['LoanID'].isin(x)]['AmountPaid'].sum()),
    TotalWriteOffs=('LoanID', lambda x: write_offs_df[write_offs_df['LoanID'].isin(x)]['WriteOffAmount'].sum())
).reset_index()

# Performance Report by Loan Product Type (assuming loan types are in the LoanProductType column)
loan_type_performance = loans_df.groupby('LoanProductType').agg(
    TotalLoans=('LoanID', 'count'),
    TotalAmount=('LoanAmount', 'sum'),
    TotalRepayments=('LoanID', lambda x: repayments_df[repayments_df['LoanID'].isin(x)]['AmountPaid'].sum()),
    TotalWriteOffs=('LoanID', lambda x: write_offs_df[write_offs_df['LoanID'].isin(x)]['WriteOffAmount'].sum())
).reset_index()

# Display Metrics and Reports
print(f"Total Repayments: {total_repayments}")
print(f"Total Write-Offs: {total_write_offs}")
print(f"Rescheduled Loans: {rescheduled_loans_count}")
print(f"NPL Ratio: {npl_ratio:.2f}%")

print("\nBranch Performance Report:")
print(branch_performance.head())

print("\nRegion Performance Report:")
print(region_performance.head())

print("\nLoan Product Type Performance Report:")
print(loan_type_performance.head())