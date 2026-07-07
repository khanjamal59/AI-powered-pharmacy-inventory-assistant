import pandas as pd
from rapidfuzz import process, fuzz
from datetime import datetime

# Load Excel file
df = pd.read_excel(
    r"C:\Users\Jamal\Dropbox\pharmacy_inventory\project_again\dummy_medicine_inventory.xlsx"
)

print(df.columns.tolist())
# Remove extra spaces
df["Medicine_Name"] = df["Medicine_Name"].astype(str).str.strip()

# User input
medicine = input("Enter medicine name: ").strip().lower()

# -------------------------

result = df[df["Medicine_Name"].str.lower() == medicine]

# -------------------------
# Partial Match
# -------------------------
if result.empty:
    result = df[df["Medicine_Name"].str.lower().str.contains(medicine, na=False)]

# -------------------------
# Fuzzy Match
# -------------------------
if result.empty:

    match = process.extractOne(
        medicine,
        df["Medicine_Name"],
        scorer=fuzz.partial_ratio
    )

    if match:
        matched_name = match[0]
        score = match[1]

        print(f"\nBest Match: {matched_name} ({score:.1f}% similarity)")

        if score >= 70:
            result = df[df["Medicine_Name"] == matched_name]

# -------------------------
# Display Result
# -------------------------
if not result.empty:

    row = result.iloc[0]

    print("\n========== Medicine Details ==========\n")
    print("Medicine Name :", row["Medicine_Name"])
    print("Category      :", row["Category"])
    print("Batch No      :", row["Batch_No"])
    print("Stock         :", row["Stock"])
    print("Unit          :", row["Unit"])
    print("Price (NPR)   :", row["Price_NPR"])
    print("Expiry Date   :", row["Expiry_Date"])
    print("Supplier      :", row["Supplier"])
    print("Reorder Level :", row["Reorder_Level"])
    print("Last Updated  :", row["Last_Updated"])

else:
    print("\n Medicine not found.")
print("\n========================================\n")   

#===================checking the inventory status ===
stock = int(row["Stock"])
reorder_level = int(row["Reorder_Level"])
price = float(row["Price_NPR"])
if stock==0:
    print("\n The medicine is out of stock.")
elif stock<=reorder_level:
    print("\n The medicine stock is low. Consider reordering.")      
else:
    print("\n The medicine is in stock.")
print("\n========================================\n")   

expiry_date = pd.to_datetime(row["Expiry_Date"])
today = pd.Timestamp.today()

days_left = (expiry_date - today).days

if days_left < 0:
    print(" Medicine has expired.")
elif days_left <= 30:
    print(f"⚠ Medicine will expire in {days_left} days.")
else:
    print(f" Expiry OK ({days_left} days remaining).")
print("\n========================================\n")   
#expiry date checking feature
if days_left<=0:
    print("\n The medicine has expired.")    
elif days_left<=30:
    print("\n The medicine is nearing its expiry date. Consider using it soon or reordering.")   
else:
    print("\n The medicine is within its expiry date.")
    
