from faker import Faker
import pandas as pd
import random

fake = Faker()

# ---------------- PATIENTS ----------------
def generate_patients(n=10000):
    return pd.DataFrame([{
        "patient_id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "gender": random.choice(["Male", "Female"]),
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=85),
        "state": fake.state(),
        "referral_source": random.choice([
            "Orthopedic Surgeon",
            "Primary Care",
            "Self Referral",
            "Sports Medicine"
        ])
    } for i in range(1, n+1)])


# ---------------- THERAPISTS ----------------
def generate_therapists(n=200):
    specialties = ["Sports Rehab", "Neuro Rehab", "Ortho Rehab", "Pediatric"]
    return pd.DataFrame([{
        "therapist_id": i,
        "therapist_name": fake.name(),
        "specialty": random.choice(specialties),
        "years_experience": random.randint(1, 20)
    } for i in range(1, n+1)])


# ---------------- CLINICS ----------------
def generate_clinics(n=20):
    return pd.DataFrame([{
        "clinic_id": i,
        "clinic_name": f"{fake.last_name()} Physical Therapy",
        "city": fake.city(),
        "state": fake.state()
    } for i in range(1, n+1)])


# ---------------- INSURANCE ----------------
def generate_insurance():
    providers = ["Medicare", "Medicaid", "Aetna", "Blue Cross", "UnitedHealth"]
    return pd.DataFrame([{
        "insurance_id": i+1,
        "insurance_name": providers[i]
    } for i in range(len(providers))])


# ---------------- DIAGNOSIS ----------------
def generate_diagnosis():
    conditions = [
        "Back Pain",
        "ACL Tear",
        "Shoulder Injury",
        "Stroke Recovery",
        "Knee Replacement Rehab"
    ]
    return pd.DataFrame([{
        "diagnosis_id": i+1,
        "diagnosis_name": conditions[i]
    } for i in range(len(conditions))])


# ---------------- VISITS (FACT TABLE) ----------------
def generate_visits(patients, therapists, clinics, insurance, diagnosis, n=50000):
    data = []

    for i in range(1, n+1):
        data.append({
            "visit_id": i,
            "patient_id": random.randint(1, len(patients)),
            "therapist_id": random.randint(1, len(therapists)),
            "clinic_id": random.randint(1, len(clinics)),
            "insurance_id": random.randint(1, len(insurance)),
            "diagnosis_id": random.randint(1, len(diagnosis)),
            "visit_date": fake.date_between(start_date="-2y", end_date="today"),
            "duration_minutes": random.randint(20, 90),
            "revenue_amount": round(random.uniform(80, 250), 2),
            "outcome_score": random.randint(40, 100)
        })

    return pd.DataFrame(data)