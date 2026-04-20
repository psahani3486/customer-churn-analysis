"""
Generate synthetic telecom customer churn dataset.
Run this script once to create data/churn.csv
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)

N = 1500  # Reduced size to prevent Gunicorn timeout on Render Free Tier

# --- Customer Demographics ---
customer_ids = [f"CUST-{str(i).zfill(5)}" for i in range(1, N + 1)]
genders = np.random.choice(["Male", "Female"], N)
senior_citizen = np.random.choice([0, 1], N, p=[0.84, 0.16])
partner = np.random.choice(["Yes", "No"], N, p=[0.48, 0.52])
dependents = np.random.choice(["Yes", "No"], N, p=[0.30, 0.70])

# --- Account Info ---
tenure = np.random.exponential(scale=32, size=N).astype(int)
tenure = np.clip(tenure, 1, 72)

# --- Phone Services ---
phone_service = np.random.choice(["Yes", "No"], N, p=[0.90, 0.10])
multiple_lines = []
for ps in phone_service:
    if ps == "No":
        multiple_lines.append("No phone service")
    else:
        multiple_lines.append(np.random.choice(["Yes", "No"], p=[0.42, 0.58]))

# --- Internet Services ---
internet_service = np.random.choice(
    ["DSL", "Fiber optic", "No"], N, p=[0.34, 0.44, 0.22]
)

internet_dependent_services = [
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies"
]

services_data = {}
for svc in internet_dependent_services:
    vals = []
    for inet in internet_service:
        if inet == "No":
            vals.append("No internet service")
        else:
            vals.append(np.random.choice(["Yes", "No"], p=[0.40, 0.60]))
    services_data[svc] = vals

# --- Contract & Billing ---
contract = np.random.choice(
    ["Month-to-month", "One year", "Two year"], N, p=[0.55, 0.21, 0.24]
)
paperless_billing = np.random.choice(["Yes", "No"], N, p=[0.59, 0.41])
payment_method = np.random.choice(
    ["Electronic check", "Mailed check", "Bank transfer (automatic)",
     "Credit card (automatic)"],
    N, p=[0.34, 0.23, 0.22, 0.21]
)

# --- Charges ---
monthly_charges = np.round(np.random.uniform(18.25, 118.75, N), 2)
total_charges = np.round(monthly_charges * tenure * np.random.uniform(0.85, 1.05, N), 2)

# --- Churn Label (correlated with features) ---
churn_prob = np.zeros(N)
# Higher churn for month-to-month
churn_prob += np.where(contract == "Month-to-month", 0.25, 0.0)
churn_prob += np.where(contract == "One year", 0.05, 0.0)
# Higher churn for fiber optic (higher cost, more competition)
churn_prob += np.where(internet_service == "Fiber optic", 0.15, 0.0)
# Higher churn for short tenure
churn_prob += np.where(tenure < 12, 0.15, 0.0)
churn_prob += np.where(tenure < 6, 0.10, 0.0)
# Higher churn for electronic check
churn_prob += np.where(payment_method == "Electronic check", 0.10, 0.0)
# Higher churn for no tech support
churn_prob += np.where(np.array(services_data["TechSupport"]) == "No", 0.05, 0.0)
# Higher churn for senior citizens
churn_prob += np.where(senior_citizen == 1, 0.08, 0.0)
# Higher churn for high monthly charges
churn_prob += np.where(monthly_charges > 80, 0.08, 0.0)
# No online security
churn_prob += np.where(np.array(services_data["OnlineSecurity"]) == "No", 0.05, 0.0)
# Paperless billing
churn_prob += np.where(paperless_billing == "Yes", 0.03, 0.0)

# Clip and add noise
churn_prob = np.clip(churn_prob + np.random.normal(0, 0.05, N), 0.02, 0.95)
churn = np.where(np.random.random(N) < churn_prob, "Yes", "No")

# --- Build DataFrame ---
df = pd.DataFrame({
    "customerID": customer_ids,
    "gender": genders,
    "SeniorCitizen": senior_citizen,
    "Partner": partner,
    "Dependents": dependents,
    "tenure": tenure,
    "PhoneService": phone_service,
    "MultipleLines": multiple_lines,
    "InternetService": internet_service,
    "OnlineSecurity": services_data["OnlineSecurity"],
    "OnlineBackup": services_data["OnlineBackup"],
    "DeviceProtection": services_data["DeviceProtection"],
    "TechSupport": services_data["TechSupport"],
    "StreamingTV": services_data["StreamingTV"],
    "StreamingMovies": services_data["StreamingMovies"],
    "Contract": contract,
    "PaperlessBilling": paperless_billing,
    "PaymentMethod": payment_method,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
    "Churn": churn
})

# Inject ~11 missing TotalCharges values (like the real dataset)
df["TotalCharges"] = df["TotalCharges"].astype(object)
missing_idx = np.random.choice(df.index, 11, replace=False)
df.loc[missing_idx, "TotalCharges"] = " "

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "churn.csv")
df.to_csv(output_path, index=False)
print(f"[OK] Generated churn.csv with {len(df)} rows at {output_path}")
print(f"   Churn rate: {(churn == 'Yes').mean():.1%}")
