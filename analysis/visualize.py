import os
import pandas as pd
import matplotlib.pyplot as plt

# Ensure output directory exists
os.makedirs('visualizations', exist_ok=True)

# Reload and prepare data using identical logic
orders_df = pd.read_csv('data/orders.csv')
customers_df = pd.read_csv('data/customers.csv')
products_df = pd.read_csv('data/products.csv')

orders_df['payment_method'] = orders_df['payment_method'].astype(str).str.strip().str.upper()
natural_key_cols = ['customer_id', 'product_id', 'order_date', 'quantity', 'discount_pct', 'payment_method', 'rating', 'returned']
orders_clean = orders_df.drop_duplicates(subset=natural_key_cols, keep='first').copy()

orders_clean['discount_pct'] = pd.to_numeric(orders_clean['discount_pct'], errors='coerce').fillna(0)
orders_clean['rating'] = pd.to_numeric(orders_clean['rating'], errors='coerce').fillna(orders_clean['rating'].median())
orders_clean['quantity'] = pd.to_numeric(orders_clean['quantity'], errors='coerce')

merged_df = orders_clean.merge(products_df, on='product_id').merge(customers_df, on='customer_id')
merged_df['order_value'] = merged_df['quantity'] * merged_df['price'] * (1 - merged_df['discount_pct'] / 100.0)

# IQR Outliers
Q1, Q3 = merged_df['quantity'].quantile(0.25), merged_df['quantity'].quantile(0.75)
IQR = Q3 - Q1
merged_df['is_outlier'] = (merged_df['quantity'] < (Q1 - 1.5 * IQR)) | (merged_df['quantity'] > (Q3 + 1.5 * IQR))

# 1. Chart 1: return_rate_by_payment.png
plt.figure(figsize=(8, 5))
return_rates = (merged_df.groupby('payment_method')['returned'].mean() * 100).sort_values(ascending=False)
bars = plt.bar(return_rates.index, return_rates.values, color=['#e74c3c', '#3498db', '#2ecc71'])
plt.title('COD Returns at 44.4% — ~3x Card', fontsize=12, fontweight='bold')
plt.xlabel('Payment Method')
plt.ylabel('Return Rate (%)')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f"{yval:.1f}%", ha='center', va='bottom')
plt.savefig('visualizations/return_rate_by_payment.png', bbox_inches='tight')
plt.close()

# 2. Chart 2: monthly_revenue_trend.png
plt.figure(figsize=(10, 5))
merged_df['order_date'] = pd.to_datetime(merged_df['order_date'])
merged_df['year_month'] = merged_df['order_date'].dt.to_period('M')
ts_clean = merged_df[~merged_df['is_outlier']].groupby('year_month')['order_value'].sum()

months_str = [str(m) for m in ts_clean.index]
plt.plot(months_str, ts_clean.values, marker='o', color='#2c3e50', linewidth=2)
plt.title('Outlier-Corrected Monthly Revenue Trend (Peak: March 2026)', fontsize=12, fontweight='bold')
plt.xlabel('Year-Month')
plt.ylabel('Revenue (₹)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('visualizations/monthly_revenue_trend.png', bbox_inches='tight')
plt.close()

print("Visualizations successfully saved to visualizations/ folder.")