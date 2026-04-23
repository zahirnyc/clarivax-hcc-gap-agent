import pandas as pd
import numpy as np
import os

np.random.seed(42)

HCC_CONDITIONS = [
    {"hcc": 19,  "name": "Diabetes without Complication",
     "icd10": ["E11.9","E10.9","E13.9"]},
    {"hcc": 18,  "name": "Diabetes with Chronic Complication",
     "icd10": ["E11.40","E11.41","E10.40"]},
    {"hcc": 85,  "name": "Congestive Heart Failure",
     "icd10": ["I50.9","I50.1","I50.20"]},
    {"hcc": 96,  "name": "Atrial Fibrillation",
     "icd10": ["I48.0","I48.11","I48.19"]},
    {"hcc": 111, "name": "COPD",
     "icd10": ["J44.0","J44.1","J44.9"]},
    {"hcc": 136, "name": "Chronic Kidney Disease Stage 5",
     "icd10": ["N18.5","N18.6"]},
    {"hcc": 22,  "name": "Morbid Obesity",
     "icd10": ["E66.01","E66.09"]},
    {"hcc": 59,  "name": "Major Depressive Disorder",
     "icd10": ["F32.0","F32.1","F32.2"]},
    {"hcc": 108, "name": "Vascular Disease",
     "icd10": ["I70.201","I70.0","I73.9"]},
    {"hcc": 137, "name": "Chronic Kidney Disease Stage 4",
     "icd10": ["N18.4"]},
]

RAF_WEIGHTS = {
    19: 0.118, 18: 0.302, 85: 0.323,
    96: 0.168, 111: 0.335, 136: 0.538,
    22: 0.272, 59: 0.243, 108: 0.288, 137: 0.289
}

n_members = 500
member_ids = [f"MBR{str(i).zfill(5)}" for i in range(1, n_members+1)]

records = []
for member_id in member_ids:
    age = np.random.randint(65, 90)
    gender = np.random.choice(["M", "F"])
    n_conditions = np.random.randint(1, 5)
    conditions = np.random.choice(HCC_CONDITIONS, n_conditions, replace=False)
    for condition in conditions:
        icd10 = np.random.choice(condition["icd10"])
        year = np.random.choice([2022, 2023])
        records.append({
            "MEMBER_ID":      member_id,
            "AGE":            age,
            "GENDER":         gender,
            "YEAR":           year,
            "HCC_CODE":       condition["hcc"],
            "HCC_NAME":       condition["name"],
            "ICD10_CODE":     icd10,
            "RAF_WEIGHT":     RAF_WEIGHTS[condition["hcc"]],
        })

df = pd.DataFrame(records)
os.makedirs("data", exist_ok=True)
df.to_csv("data/member_conditions.csv", index=False)
print(f"Generated {len(df)} records for {n_members} members")
print(df.head(10).to_string())
print(f"\nHCC distribution:\n{df['HCC_NAME'].value_counts()}")