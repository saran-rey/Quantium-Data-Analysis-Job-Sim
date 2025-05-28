# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

# %%
# Suppress warnings
warnings.filterwarnings('ignore')

# %%
plt.style.use('seaborn-v0_8')  # Using a specific seaborn style version
sns.set_theme()  # Set seaborn theme


# %%
# Create output directory for visualizations
output_dir = Path("visualizations")
output_dir.mkdir(exist_ok=True)


# %%
print("Loading data...")
behav = pd.read_csv("QVI_purchase_behaviour.csv")
transac = pd.read_excel("QVI_transaction_data.xlsx")


# %%
# Basic data information
print("\n[[[[[[[[[[[[[[       Purchase Behavior Data Info        ]]]]]]]]]]]]]\n")
print(behav.info())
print("\n[[[[[[[[[[[[[[      First 10 rows of Purchase Behavior Data:      ]]]]]]]]]]]]]]")
behav.head(10)

# %%
# LYLTY_CARD_NBR will be used a unique identifier
behav.drop_duplicates("LYLTY_CARD_NBR")
behav.dropna(inplace=True)
behav.info()

# %%
# Create customer segment analysis
customer_segments = pd.crosstab(behav['LIFESTAGE'], behav['PREMIUM_CUSTOMER'])
print("\nCustomer Segments Analysis:")
customer_segments

# %%
# Customer Analysis
print("\n[[[[[[[[[[[[[[      Customer Analysis      ]]]]]]]]]]]]]]")
print("\nTotal number of customers:")
print(len(behav))
print("\n[[[[[[[[[[[[[[      Customer Lifestage Distribution:      ]]]]]]]]]]]]]]\n")
print(behav['LIFESTAGE'].value_counts())
print("\n[[[[[[[[[[[[[[      Customer Premium Status Distribution:      ]]]]]]]]]]]]]]\n")
premium_customers = behav['PREMIUM_CUSTOMER'].value_counts()
premium_customers

# %%
print("\n[[[[[[[[[[[[[[      Transaction Data Info      ]]]]]]]]]]]]]]\n")
print(transac.info())
print("\n[[[[[[[[[[[[[[      First 10 rows of Transaction Data:      ]]]]]]]]]]]]]]")
transac.head(10)

# %%
# Changing the date format
transac["DATE"] = pd.to_datetime(transac["DATE"], origin = '1899-12-30', unit ='D')


# %%
transac.head(10)

# %%
# Clean product names by removing special characters and digits
transac['PROD_NAME'] = transac['PROD_NAME'].str.replace('[^a-zA-Z0-9\s]', '', regex=True)
transac['PROD_NAME'] = transac['PROD_NAME'].str.replace(r'\d+', '', regex=True)
print("\nSample of cleaned product names:")
print(transac['PROD_NAME'].head())

# %%
# Remove 'g' from the end of product names
transac['PROD_NAME'] = transac['PROD_NAME'].str.replace(r'g$', '', regex=True)
print("\nSample of product names after removing trailing 'g':")
transac['PROD_NAME'].head()

# %%
# Filter transactions to only include products with 'chip' or 'chips'
chip_mask = transac['PROD_NAME'].str.contains('chip', case=False)
transac = transac[chip_mask]

print("\nDataset filtered to only include chip products")
print(f"Number of transactions remaining: {len(transac)}")
print("\nSample of chip products:")
print(transac['PROD_NAME'].head())


# %%
transac.info()

# %%
Sales_by_Period = transac.iloc[:, [0,7]].groupby("DATE").sum().sort_values("DATE", ascending=True).reset_index()

# %%
Sales_by_Period['DATE'] = pd.to_datetime(Sales_by_Period['DATE'])
Sales_by_Period['Year Month'] = Sales_by_Period['DATE'].dt.to_period('M').astype(str)
Sales_by_Period['Month'] = Sales_by_Period['DATE'].dt.strftime('%B')

# %%
Sales_by_Period.head(10)
Sales_by_Period.info()

# %%
# Create a complete date range from Jul 1 2018 to Jun 30 2019
date_range = pd.date_range(start='2018-07-01', end='2019-06-30', freq='D')

# Convert date_range to dataframe
date_df = pd.DataFrame({'DATE': date_range})

# Merge with Sales_by_Period to identify missing dates
complete_sales = pd.merge(date_df, Sales_by_Period, on='DATE', how='left')

# Fill missing values with 0
complete_sales = complete_sales.fillna(0)

# Find missing dates
missing_dates = complete_sales[complete_sales['TOT_SALES'] == 0]['DATE']

print("\nMissing dates in the dataset:")
print(missing_dates.dt.strftime('%Y-%m-%d').tolist())


# %%
# Create a complete date range from Jul 1 2018 to Jun 30 2019
date_range = pd.date_range(start='2018-07-01', end='2019-06-30', freq='D')

# Convert date_range to dataframe
date_df = pd.DataFrame({'DATE': date_range})

# Merge with Sales_by_Period to include all dates
Sales_by_Period = pd.merge(date_df, Sales_by_Period, on='DATE', how='left')

# Fill missing values with 0
Sales_by_Period = Sales_by_Period.fillna(0)

# Re-calculate Year Month and Month columns for any new rows
Sales_by_Period['Year Month'] = Sales_by_Period['DATE'].dt.to_period('M').astype(str)
Sales_by_Period['Month'] = Sales_by_Period['DATE'].dt.strftime('%B')


# %%
Sales_by_Period.info()

# %%
monthly_sales = Sales_by_Period.groupby(['Year Month', 'Month'])["TOT_SALES"].sum().reset_index()

# %%
monthly_sales.head(12)

# %%
# Join behavior and transaction data
combined_data = pd.merge(transac, behav, on='LYLTY_CARD_NBR', how='inner',validate = "m:1")

# %%
combined_data.info()

# %%
# Calculate total sales and percentages by customer segments
sales_by_segment = combined_data.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['TOT_SALES'].sum().reset_index()
total_sales = sales_by_segment['TOT_SALES'].sum()
sales_by_segment['Sales_Percentage'] = (sales_by_segment['TOT_SALES'] / total_sales * 100).round(2)

# Create pivot table with both total sales and percentages
sales_pivot = pd.pivot_table(sales_by_segment, 
                           values=['TOT_SALES', 'Sales_Percentage'],
                           index='LIFESTAGE',
                           columns='PREMIUM_CUSTOMER')

# Display combined results
print("\nCustomer Segment Analysis - Total Sales ($) and Percentage Contribution (%):")
print(sales_pivot)


# %%
# Check for unmatched transactions by comparing original transaction count with merged count
print("Original transaction count:", len(transac))
print("Merged transaction count:", len(combined_data))
print("Number of unmatched transactions:", len(transac) - len(combined_data))


# %% [markdown]
# ### General Visualizations

# %%
# Customer Lifestage Distribution
CustDist = plt.figure(figsize=(12, 6))
lifestages = CustDist.add_subplot(1,1,1)
behav['LIFESTAGE'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Distribution of Customer Lifestages', pad=20)
plt.xlabel('Lifestage')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / 'lifestage_distribution.png', dpi=300, bbox_inches='tight')
plt.show() # Add this to display the plot
plt.close()

# %%
# Premium Customer Distribution
plt.figure(figsize=(10, 6))
behav['PREMIUM_CUSTOMER'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightgreen', 'lightcoral'])
plt.title('Distribution of Customer Segments', pad=20)
plt.savefig(output_dir / 'premium_distribution.png', dpi=300, bbox_inches='tight')
plt.show() # Add this to display the plot
plt.close()


# %%
# Customer Segments Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(customer_segments, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': 'Number of Customers'})
plt.title('Customer Segments Analysis', pad=20)
plt.tight_layout()
plt.savefig(output_dir / 'customer_segments_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()



# %%
# Sales by Segment Heatmap
segment_sales = combined_data.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['TOT_SALES'].sum().unstack()

plt.figure(figsize=(12, 8))
sns.heatmap(segment_sales, annot=True, fmt='.0f', cmap='viridis', cbar_kws={'label': 'Total Sales ($)'})
plt.title('Total Sales by Customer Segment', pad=20)
plt.tight_layout()
plt.savefig(output_dir / 'sales_by_segment_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()


# %%
# Average Transaction Value by Customer Segment
merged_data = pd.merge(transac, behav, on='LYLTY_CARD_NBR', how='left')
avg_transaction = merged_data.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['TOT_SALES'].mean().unstack()

plt.figure(figsize=(12, 6))
avg_transaction.plot(kind='bar', colormap='viridis')
plt.title('Average Transaction Value by Customer Segment', pad=20)
plt.xlabel('Lifestage')
plt.ylabel('Average Transaction Value')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Customer Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(output_dir / 'avg_transaction_by_segment.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

# %%
# Monthly Sales Analysis
salesPlot = plt.figure(figsize = (12.5,5))
sales_in_months = salesPlot.add_subplot(1,1,1)
sales_in_months.plot(monthly_sales["Month"],monthly_sales["TOT_SALES"], 'b', alpha = 0.7, )
plt.title('Monthly Sales Trend', pad=20)
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(output_dir / 'monthly_sales.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()


# %%



