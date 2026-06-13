import pandas as pd

# Read Excel files
companies = pd.read_excel("data/raw/companies.xlsx")
analysis = pd.read_excel("data/raw/analysis.xlsx")
balancesheet = pd.read_excel("data/raw/balancesheet.xlsx")
cashflow = pd.read_excel("data/raw/cashflow.xlsx")
profitandloss = pd.read_excel("data/raw/profitandloss.xlsx")
prosandcons = pd.read_excel("data/raw/prosandcons.xlsx")
documents = pd.read_excel("data/raw/documents.xlsx")

# Print shapes
print("Companies:", companies.shape)
print("Analysis:", analysis.shape)
print("Balance Sheet:", balancesheet.shape)
print("Cashflow:", cashflow.shape)
print("Profit & Loss:", profitandloss.shape)
print("Pros & Cons:", prosandcons.shape)
print("Documents:", documents.shape)

# Save CSV versions
companies.to_csv("data/raw/companies.csv", index=False)
analysis.to_csv("data/raw/analysis.csv", index=False)
balancesheet.to_csv("data/raw/balancesheet.csv", index=False)
cashflow.to_csv("data/raw/cashflow.csv", index=False)
profitandloss.to_csv("data/raw/profitandloss.csv", index=False)
prosandcons.to_csv("data/raw/prosandcons.csv", index=False)
documents.to_csv("data/raw/documents.csv", index=False)

print("✅ All CSV files created successfully")