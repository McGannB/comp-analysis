import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # for enhanced visualizations

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('rows.csv')

# Display the first few rows
print(df.head())

# Get information about the columns and data types
print(df.info())

# Summary statistics
print(df.describe())

# Change Column Names
df.columns = df.columns.str.lower()  # Convert to lowercase
df.columns = df.columns.str.replace(' ', '_')  # Replace spaces with underscores
df.columns = df.columns.str.replace('?', '')  # Remove question marks

df = df.rename(columns={'consumer_complaint_narrative': 'consumer_complaint', 'company_public_response': 'public_response', 'consumer_consent_provided': 'consumer_consent', 'company_response_to_consumer': 'response_to_consumer', 'date_sent_to_company': 'date_sent'})  # Rename long column names for easier access


# Check for missing values
print(df.isnull().sum())

# Handle missing values (fill with 'Unknown')
cols_to_fill = ['sub-product', 'sub-issue', 'consumer_complaint', 'public_response', 'zip_code', 'tags', 'consumer_consent', 'response_to_consumer', 'consumer_disputed']
for col in cols_to_fill:
    if col in df.columns: # Check if the column exists
        df.fillna({col: 'Unknown'}, inplace=True)

# Convert 'Date received' and 'Date sent to company' to datetime objects
date_cols = ['date_received', 'date_sent']
for col in date_cols:
    if col in df.columns: # Check if the column exists
        df[col] = pd.to_datetime(df[col], errors='coerce') # Use errors='coerce' to handle potential errors

# Convert 'Complaint ID' to string
if 'complaint_id' in df.columns: # Check if the column exists
    df['complaint_id'] = df['complaint_id'].astype(str)

# Example: Convert text columns to lowercase
text_cols = ['product', 'sub-product', 'issue', 'sub-issue', 'consumer_complaint', 'public_response', 'company', 'state', 'zip_code', 'tags', 'consumer_consent', 'submitted_via', 'response_to_consumer', 'timely_response', 'consumer_disputed']
for col in text_cols:
    if col in df.columns: # Check if the column exists
        df[col] = df[col].astype(str).str.lower()

# Analyze complaint volume by product
if 'product' in df.columns: # Check if the column exists
    product_counts = df['product'].value_counts().head(10)  # Top 10 products
    print("\nComplaint Volume by Product:\n", product_counts)

    # Visualize complaint volume by product
    plt.figure(1, figsize=(10, 6))
    product_counts.plot(kind='bar')
    plt.title('Complaint Volume by Product')
    plt.xlabel('Product')
    plt.ylabel('Number of Complaints')
    #plt.show()

# Analyze complaint volume by company
if 'company' in df.columns: # Check if the column exists
    company_counts = df['company'].value_counts().head(10)  # Top 10 companies
    print("\nComplaint Volume by Company:\n", company_counts)

    # Visualize complaint volume by company
    plt.figure(2, figsize=(10, 6))
    company_counts.plot(kind='bar')
    plt.title('Complaint Volume by Company')
    plt.xlabel('Company')
    plt.ylabel('Number of Complaints')
    #plt.show()

# Analyze complaint trends over time
if 'date_received' in df.columns: # Check if the column exists
    # Resample by month
    complaints_by_month = df.set_index('date_received').resample('M').size()
    print("\nComplaint Trends Over Time:\n", complaints_by_month.head())

    # Visualize complaint trends
    plt.figure(3, figsize=(10, 6))
    complaints_by_month.plot()
    plt.title('Complaint Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Complaints')
    #plt.show()

# Analyze how complaints are being resolved
if 'response_to_consumer' in df.columns: # Check if the column exists
    resolution_counts = df['response_to_consumer'].value_counts()
    print("\nComplaint Resolution Analysis:\n", resolution_counts)

    # Visualize complaint resolution
    plt.figure(4, figsize=(8, 8))
    resolution_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Complaint Resolution')
    plt.ylabel('')  # Remove the default 'ylabel'

#plt.show()

def generate_complaint_report(df, top_n=5):
    """
    Generates a simple complaint report.

    Args:
        df: Pandas DataFrame containing complaint data.
        top_n: Number of top products/companies to include in the report.
    """

    report = f"Complaint Report\n\n"

    # Top products
    if 'product' in df.columns: # Check if the column exists
        top_products = df['product'].value_counts().head(top_n)
        report += f"\nTop {top_n} Products with Most Complaints:\n"
        report += top_products.to_string() + "\n"
    # Top companies
    if 'company' in df.columns: # Check if the column exists
        top_companies = df['company'].value_counts().head(top_n)
        report += f"\nTop {top_n} Companies with Most Complaints:\n"
        report += top_companies.to_string() + "\n"
    # Complaint trends (simple example)
    if 'date_received' in df.columns: # Check if the column exists
        report += "\nComplaint Trends (Last 3 Months):\n"
        if 'date_received' in df.columns:
            recent_complaints = df.set_index('date_received').resample('M').size().tail(3)
            report += recent_complaints.to_string() + "\n"

    return report

# Generate and print the report
complaint_report = generate_complaint_report(df)
print(complaint_report)

# To save the report to a file:
# with open("complaint_report.txt", "w") as file:
#     file.write(complaint_report)