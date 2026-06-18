from db_connection import get_connection
import generate_data as gd

engine = get_connection()

# Generate data
patients = gd.generate_patients(10000)
therapists = gd.generate_therapists()
clinics = gd.generate_clinics()
insurance = gd.generate_insurance()
diagnosis = gd.generate_diagnosis()
visits = gd.generate_visits(patients, therapists, clinics, insurance, diagnosis, 5000)

# Load into MySQL
patients.to_sql("dim_patient", engine, if_exists="append", index=False)
therapists.to_sql("dim_therapist", engine, if_exists="append", index=False)
clinics.to_sql("dim_clinic", engine, if_exists="append", index=False)
insurance.to_sql("dim_insurance", engine, if_exists="append", index=False)
diagnosis.to_sql("dim_diagnosis", engine, if_exists="append", index=False)
visits.to_sql("fact_visits", engine, if_exists="append", index=False)

print("DATA LOADED SUCCESSFULLY 🚀")