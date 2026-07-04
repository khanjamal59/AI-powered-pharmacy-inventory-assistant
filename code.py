# import pandas as pd 
# df=pd.read_excel(r"C:\Users\Jamal\Dropbox\pharmacy_inventory\project_again\dummy_medicine_inventory.xlsx")
# print(df.head(2))
# medicine_name=input("enter the name of the medicine:").strip()
# result=df[df['Medicine_Name'].str.lower()==medicine_name]

# if result.empty:
#     print("medicine is not found")
# else:
#     print(result)
# print("-"*20)
# print("Medicine_Name:", result['Medicine_Name'])
import pandas as pd


df=pd.read_excel(r"dummy_medicine_inventory.xlsx")

# Taking the  medicine name from the  user
medicine = input("Enter medicine name: ")

# Searching the name from the excel 
result = df[df["Medicine_Name"].str.lower() == medicine.lower()]

if not result.empty:
    result = result.iloc[0]  # Getting the first matching row

    print("Medicine Name :", result["Medicine_Name"])
    print("Category      :", result["Category"])
    print("Batch No      :", result["Batch_No"])
    print("Stock         :", result["Stock"])
    print("Unit          :", result["Unit"])
    print("Price (NPR)   :", result["Price_NPR"])
    print("Expiry Date   :", result["Expiry_Date"])
    print("Supplier      :", result["Supplier"])
    print("Reorder Level :", result["Reorder_Level"])
else:
    print("Medicine not found.")
