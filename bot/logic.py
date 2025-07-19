from bot.data_loader import load_employee_data

# Load data once when this file is imported
df = load_employee_data()

def search_employee(query):
    query = query.lower()
    # Simple search
    for _, row in df.iterrows():
        if row["Name"].lower() in query:
            return f"{row['Name']}'s email is {row['Email']}, phone number is {row['Phone']}."
    return None
