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
# 1. Exact Match
# -------------------------
result = df[df["Medicine_Name"].str.lower() == medicine]

# -------------------------
# 2. Partial Match
# -------------------------
if result.empty:
    result = df[df["Medicine_Name"].str.lower().str.contains(medicine, na=False)]

# -------------------------
# 3. Fuzzy Match
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
    print("\n❌ Medicine not found.")
print("\n========================================\n")   

#===================checking the inventory status ===
stock = int(row["Stock"])
reorder_level = int(row["Reorder_Level"])
price = float(row["Price_NPR"])
if stock==0:
    print("\n⚠️  The medicine is out of stock.")
elif stock<=reorder_level:
    print("\n⚠️  The medicine stock is low. Consider reordering.")      
else:
    print("\n✅ The medicine is in stock.")
print("\n========================================\n")   
#expiry date check
expiry_date = pd.to_datetime(row["Expiry_Date"])
today = pd.Timestamp.today()

days_left = (expiry_date - today).days


