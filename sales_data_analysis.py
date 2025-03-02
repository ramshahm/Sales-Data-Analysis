import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os
file_path = "sales_data.csv"

if not os.path.exists(file_path):
    print(f"Error: '{file_path}' not found. Please place the file in the same directory.")
    exit()

df = pd.read_csv(file_path)
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

df['Date'] = pd.to_datetime(df['Date'])

df['Total_Sales'] = df['Sales'] * df['Quantity']
df['Profit_Margin'] = (df['Profit'] / df['Total_Sales']) * 100

conn = sqlite3.connect("sales_data.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

query1 = "SELECT Region, SUM(Sales) as TotalSales FROM sales GROUP BY Region ORDER BY TotalSales DESC"
query2 = "SELECT Category, SUM(Profit) as TotalProfit FROM sales GROUP BY Category ORDER BY TotalProfit DESC"

sales_by_region = pd.read_sql(query1, conn)
profit_by_category = pd.read_sql(query2, conn)

conn.close()

plt.figure(figsize=(10, 5))
sns.barplot(x="Region", y="TotalSales", data=sales_by_region, palette="viridis")
plt.title("Total Sales by Region")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(x="Category", y="TotalProfit", data=profit_by_category, palette="magma")
plt.title("Total Profit by Category")
plt.xticks(rotation=45)
plt.show()

output_file = "Sales_Report.xlsx"
df.to_excel(output_file, sheet_name="Sales Data", index=False)

print(f"✅ Project Completed! Final report saved as '{output_file}'")
