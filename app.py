import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime, date

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': 'Ishan@123',  # Change this to your MySQL password
    'database': 'genetic_disorder_db'
}

# Database Connection Function
def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# ==================== CLINIC CRUD ====================
def create_clinic(name, address):
    """Create a new clinic"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Clinic (ClinicName, Address) VALUES (%s, %s)"
            cursor.execute(query, (name, address))
            conn.commit()
            st.success("Clinic created successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def read_clinics():
    """Read all clinics"""
    conn = get_db_connection()
    if conn:
        try:
            query = "SELECT * FROM Clinic"
            df = pd.read_sql(query, conn)
            return df
        except Error as e:
            st.error(f"Error: {e}")
            return pd.DataFrame()
        finally:
            conn.close()

def update_clinic(clinic_id, name, address):
    """Update a clinic"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE Clinic SET ClinicName = %s, Address = %s WHERE ClinicID = %s"
            cursor.execute(query, (name, address, clinic_id))
            conn.commit()
            st.success("Clinic updated successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def delete_clinic(clinic_id):
    """Delete a clinic"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM Clinic WHERE ClinicID = %s"
            cursor.execute(query, (clinic_id,))
            conn.commit()
            st.success("Clinic deleted successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# ==================== DOCTOR CRUD ====================
def create_doctor(first_name, last_name, specialization, clinic_id):
    """Create a new doctor"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Doctor (FirstName, LastName, Specialization, ClinicID) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (first_name, last_name, specialization, clinic_id))
            conn.commit()
            st.success("Doctor created successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def read_doctors():
    """Read all doctors"""
    conn = get_db_connection()
    if conn:
        try:
            query = """
                SELECT d.DoctorID, d.FirstName, d.LastName, d.Specialization, 
                       d.ClinicID, c.ClinicName
                FROM Doctor d
                LEFT JOIN Clinic c ON d.ClinicID = c.ClinicID
            """
            df = pd.read_sql(query, conn)
            return df
        except Error as e:
            st.error(f"Error: {e}")
            return pd.DataFrame()
        finally:
            conn.close()

def update_doctor(doctor_id, first_name, last_name, specialization, clinic_id):
    """Update a doctor"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE Doctor SET FirstName = %s, LastName = %s, Specialization = %s, ClinicID = %s WHERE DoctorID = %s"
            cursor.execute(query, (first_name, last_name, specialization, clinic_id, doctor_id))
            conn.commit()
            st.success("Doctor updated successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def delete_doctor(doctor_id):
    """Delete a doctor"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM Doctor WHERE DoctorID = %s"
            cursor.execute(query, (doctor_id,))
            conn.commit()
            st.success("Doctor deleted successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# ==================== PATIENT CRUD ====================
def create_patient(first_name, last_name, dob, gender, contact, address):
    """Create a new patient"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Patient (FirstName, LastName, DateOfBirth, Gender, ContactNo, Address) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (first_name, last_name, dob, gender, contact, address))
            conn.commit()
            st.success("Patient created successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def read_patients():
    """Read all patients"""
    conn = get_db_connection()
    if conn:
        try:
            query = "SELECT * FROM Patient"
            df = pd.read_sql(query, conn)
            return df
        except Error as e:
            st.error(f"Error: {e}")
            return pd.DataFrame()
        finally:
            conn.close()

def update_patient(patient_id, first_name, last_name, dob, gender, contact, address):
    """Update a patient - This will trigger the audit log for ContactNo changes"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """UPDATE Patient 
                      SET FirstName = %s, LastName = %s, DateOfBirth = %s, 
                          Gender = %s, ContactNo = %s, Address = %s 
                      WHERE PatientID = %s"""
            cursor.execute(query, (first_name, last_name, dob, gender, contact, address, patient_id))
            conn.commit()
            st.success("Patient updated successfully! (Trigger fired if ContactNo changed)")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def delete_patient(patient_id):
    """Delete a patient"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM Patient WHERE PatientID = %s"
            cursor.execute(query, (patient_id,))
            conn.commit()
            st.success("Patient deleted successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# ==================== APPOINTMENT CRUD ====================
def create_appointment(appt_date, appt_time, patient_id, doctor_id):
    """Create a new appointment"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Appointment (AppointmentDate, AppointmentTime, PatientID, DoctorID) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (appt_date, appt_time, patient_id, doctor_id))
            conn.commit()
            st.success("Appointment created successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def read_appointments():
    """Read all appointments"""
    conn = get_db_connection()
    if conn:
        try:
            query = """
                SELECT a.AppointmentID, a.AppointmentDate, a.AppointmentTime,
                       a.PatientID, CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
                       a.DoctorID, CONCAT(d.FirstName, ' ', d.LastName) AS DoctorName
                FROM Appointment a
                LEFT JOIN Patient p ON a.PatientID = p.PatientID
                LEFT JOIN Doctor d ON a.DoctorID = d.DoctorID
            """
            df = pd.read_sql(query, conn)
            return df
        except Error as e:
            st.error(f"Error: {e}")
            return pd.DataFrame()
        finally:
            conn.close()

def update_appointment(appt_id, appt_date, appt_time, patient_id, doctor_id):
    """Update an appointment"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """UPDATE Appointment 
                      SET AppointmentDate = %s, AppointmentTime = %s, 
                          PatientID = %s, DoctorID = %s 
                      WHERE AppointmentID = %s"""
            cursor.execute(query, (appt_date, appt_time, patient_id, doctor_id, appt_id))
            conn.commit()
            st.success("Appointment updated successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def delete_appointment(appt_id):
    """Delete an appointment"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM Appointment WHERE AppointmentID = %s"
            cursor.execute(query, (appt_id,))
            conn.commit()
            st.success("Appointment deleted successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# ==================== GENETIC DISORDER CRUD ====================
def create_genetic_disorder(name, gene_symbol, omim_id):
    """Create a new genetic disorder"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO GeneticDisorder (DisorderName, GeneSymbol, OMIM_ID) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, gene_symbol, omim_id))
            conn.commit()
            st.success("Genetic Disorder created successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def read_genetic_disorders():
    """Read all genetic disorders"""
    conn = get_db_connection()
    if conn:
        try:
            query = "SELECT * FROM GeneticDisorder"
            df = pd.read_sql(query, conn)
            return df
        except Error as e:
            st.error(f"Error: {e}")
            return pd.DataFrame()
        finally:
            conn.close()

def update_genetic_disorder(disorder_id, name, gene_symbol, omim_id):
    """Update a genetic disorder"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE GeneticDisorder SET DisorderName = %s, GeneSymbol = %s, OMIM_ID = %s WHERE DisorderID = %s"
            cursor.execute(query, (name, gene_symbol, omim_id, disorder_id))
            conn.commit()
            st.success("Genetic Disorder updated successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def delete_genetic_disorder(disorder_id):
    """Delete a genetic disorder"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM GeneticDisorder WHERE DisorderID = %s"
            cursor.execute(query, (disorder_id,))
            conn.commit()
            st.success("Genetic Disorder deleted successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# ==================== SPECIAL FEATURES ====================

def call_patient_full_report(patient_id):
    """Call the stored procedure sp_GetPatientFullReport"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc('sp_GetPatientFullReport', [patient_id])
            
            results = []
            for result in cursor.stored_results():
                df = pd.DataFrame(result.fetchall(), columns=[desc[0] for desc in result.description])
                results.append(df)
            
            return results
        except Error as e:
            st.error(f"Error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

def get_patient_age(patient_id):
    """Call the function fn_GetPatientAge"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT fn_GetPatientAge(%s) AS Age"
            cursor.execute(query, (patient_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            st.error(f"Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

def view_audit_log():
    """View the Patient_Audit_Log table (populated by trigger)"""
    conn = get_db_connection()
    if conn:
        try:
            query = "SELECT * FROM Patient_Audit_Log ORDER BY ChangedAt DESC"
            df = pd.read_sql(query, conn)
            return df
        except Error as e:
            st.error(f"Error: {e}")
            return pd.DataFrame()
        finally:
            conn.close()

# ==================== STREAMLIT UI ====================

def main():
    st.set_page_config(page_title="Genetic Disorder Management System", layout="wide")
    
    st.title("🧬 Genetic Disorder Management System")
    st.markdown("---")
    
    # Sidebar Navigation
    menu = st.sidebar.selectbox(
        "Select Module",
        ["Home", "Clinics", "Doctors", "Patients", "Appointments", 
         "Genetic Disorders", "Special Features", "Audit Log"]
    )
    
    # ==================== HOME ====================
    if menu == "Home":
        st.header("Welcome to the Genetic Disorder Management System")
        st.write("""
        This system helps manage:
        - 🏥 Clinics and Doctors
        - 👥 Patients and their genetic information
        - 📅 Appointments
        - 🧬 Genetic Disorders and Test Results
        - 📊 Special Reports and Analytics
        
        **Features:**
        - Full CRUD operations on all entities
        - Stored Procedure: Patient Full Report
        - Function: Calculate Patient Age
        - Trigger: Audit log for patient contact changes
        """)
        
        # Quick Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            df = read_patients()
            st.metric("Total Patients", len(df))
        with col2:
            df = read_doctors()
            st.metric("Total Doctors", len(df))
        with col3:
            df = read_clinics()
            st.metric("Total Clinics", len(df))
        with col4:
            df = read_appointments()
            st.metric("Total Appointments", len(df))
    
    # ==================== CLINICS ====================
    elif menu == "Clinics":
        st.header("🏥 Clinic Management")
        
        tab1, tab2, tab3, tab4 = st.tabs(["View All", "Create", "Update", "Delete"])
        
        with tab1:
            st.subheader("All Clinics")
            df = read_clinics()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No clinics found.")
        
        with tab2:
            st.subheader("Create New Clinic")
            with st.form("create_clinic_form"):
                name = st.text_input("Clinic Name")
                address = st.text_area("Address")
                submitted = st.form_submit_button("Create Clinic")
                if submitted:
                    if name:
                        create_clinic(name, address)
                        st.rerun()
                    else:
                        st.warning("Please enter clinic name.")
        
        with tab3:
            st.subheader("Update Clinic")
            df = read_clinics()
            if not df.empty:
                clinic_id = st.selectbox("Select Clinic", df['ClinicID'].tolist())
                selected_clinic = df[df['ClinicID'] == clinic_id].iloc[0]
                
                with st.form("update_clinic_form"):
                    name = st.text_input("Clinic Name", value=selected_clinic['ClinicName'])
                    address = st.text_area("Address", value=selected_clinic['Address'] if pd.notna(selected_clinic['Address']) else "")
                    submitted = st.form_submit_button("Update Clinic")
                    if submitted:
                        update_clinic(clinic_id, name, address)
                        st.rerun()
            else:
                st.info("No clinics to update.")
        
        with tab4:
            st.subheader("Delete Clinic")
            df = read_clinics()
            if not df.empty:
                clinic_id = st.selectbox("Select Clinic to Delete", df['ClinicID'].tolist())
                selected_clinic = df[df['ClinicID'] == clinic_id].iloc[0]
                st.write(f"**{selected_clinic['ClinicName']}**")
                if st.button("Delete Clinic", type="primary"):
                    delete_clinic(clinic_id)
                    st.rerun()
            else:
                st.info("No clinics to delete.")
    
    # ==================== DOCTORS ====================
    elif menu == "Doctors":
        st.header("👨‍⚕️ Doctor Management")
        
        tab1, tab2, tab3, tab4 = st.tabs(["View All", "Create", "Update", "Delete"])
        
        with tab1:
            st.subheader("All Doctors")
            df = read_doctors()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No doctors found.")
        
        with tab2:
            st.subheader("Create New Doctor")
            clinics_df = read_clinics()
            with st.form("create_doctor_form"):
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                specialization = st.text_input("Specialization")
                clinic_id = st.selectbox("Clinic", clinics_df['ClinicID'].tolist() if not clinics_df.empty else [])
                submitted = st.form_submit_button("Create Doctor")
                if submitted:
                    if first_name and last_name:
                        create_doctor(first_name, last_name, specialization, clinic_id)
                        st.rerun()
                    else:
                        st.warning("Please enter required fields.")
        
        with tab3:
            st.subheader("Update Doctor")
            df = read_doctors()
            clinics_df = read_clinics()
            if not df.empty:
                doctor_id = st.selectbox("Select Doctor", df['DoctorID'].tolist())
                selected_doctor = df[df['DoctorID'] == doctor_id].iloc[0]
                
                with st.form("update_doctor_form"):
                    first_name = st.text_input("First Name", value=selected_doctor['FirstName'])
                    last_name = st.text_input("Last Name", value=selected_doctor['LastName'])
                    specialization = st.text_input("Specialization", value=selected_doctor['Specialization'] if pd.notna(selected_doctor['Specialization']) else "")
                    clinic_id = st.selectbox("Clinic", clinics_df['ClinicID'].tolist() if not clinics_df.empty else [], 
                                            index=clinics_df['ClinicID'].tolist().index(selected_doctor['ClinicID']) if pd.notna(selected_doctor['ClinicID']) and selected_doctor['ClinicID'] in clinics_df['ClinicID'].tolist() else 0)
                    submitted = st.form_submit_button("Update Doctor")
                    if submitted:
                        update_doctor(doctor_id, first_name, last_name, specialization, clinic_id)
                        st.rerun()
            else:
                st.info("No doctors to update.")
        
        with tab4:
            st.subheader("Delete Doctor")
            df = read_doctors()
            if not df.empty:
                doctor_id = st.selectbox("Select Doctor to Delete", df['DoctorID'].tolist())
                selected_doctor = df[df['DoctorID'] == doctor_id].iloc[0]
                st.write(f"**Dr. {selected_doctor['FirstName']} {selected_doctor['LastName']}**")
                if st.button("Delete Doctor", type="primary"):
                    delete_doctor(doctor_id)
                    st.rerun()
            else:
                st.info("No doctors to delete.")
    
    # ==================== PATIENTS ====================
    elif menu == "Patients":
        st.header("👥 Patient Management")
        
        tab1, tab2, tab3, tab4 = st.tabs(["View All", "Create", "Update", "Delete"])
        
        with tab1:
            st.subheader("All Patients")
            df = read_patients()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No patients found.")
        
        with tab2:
            st.subheader("Create New Patient")
            with st.form("create_patient_form"):
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    dob = st.date_input("Date of Birth", value=date(2000, 1, 1))
                with col2:
                    gender = st.selectbox("Gender", ["M", "F", "Other"])
                    contact = st.text_input("Contact Number")
                    address = st.text_area("Address")
                submitted = st.form_submit_button("Create Patient")
                if submitted:
                    if first_name and last_name:
                        create_patient(first_name, last_name, dob, gender, contact, address)
                        st.rerun()
                    else:
                        st.warning("Please enter required fields.")
        
        with tab3:
            st.subheader("Update Patient (Trigger will fire on ContactNo change)")
            df = read_patients()
            if not df.empty:
                patient_id = st.selectbox("Select Patient", df['PatientID'].tolist())
                selected_patient = df[df['PatientID'] == patient_id].iloc[0]
                
                with st.form("update_patient_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        first_name = st.text_input("First Name", value=selected_patient['FirstName'])
                        last_name = st.text_input("Last Name", value=selected_patient['LastName'])
                        dob = st.date_input("Date of Birth", value=pd.to_datetime(selected_patient['DateOfBirth']).date() if pd.notna(selected_patient['DateOfBirth']) else date(2000, 1, 1))
                    with col2:
                        gender = st.selectbox("Gender", ["M", "F", "Other"], 
                                            index=["M", "F", "Other"].index(selected_patient['Gender']) if selected_patient['Gender'] in ["M", "F", "Other"] else 0)
                        contact = st.text_input("Contact Number", value=selected_patient['ContactNo'] if pd.notna(selected_patient['ContactNo']) else "")
                        address = st.text_area("Address", value=selected_patient['Address'] if pd.notna(selected_patient['Address']) else "")
                    
                    st.info("⚠️ Changing the Contact Number will trigger the audit log!")
                    submitted = st.form_submit_button("Update Patient")
                    if submitted:
                        update_patient(patient_id, first_name, last_name, dob, gender, contact, address)
                        st.rerun()
            else:
                st.info("No patients to update.")
        
        with tab4:
            st.subheader("Delete Patient")
            df = read_patients()
            if not df.empty:
                patient_id = st.selectbox("Select Patient to Delete", df['PatientID'].tolist())
                selected_patient = df[df['PatientID'] == patient_id].iloc[0]
                st.write(f"**{selected_patient['FirstName']} {selected_patient['LastName']}**")
                if st.button("Delete Patient", type="primary"):
                    delete_patient(patient_id)
                    st.rerun()
            else:
                st.info("No patients to delete.")
    
    # ==================== APPOINTMENTS ====================
    elif menu == "Appointments":
        st.header("📅 Appointment Management")
        
        tab1, tab2, tab3, tab4 = st.tabs(["View All", "Create", "Update", "Delete"])
        
        with tab1:
            st.subheader("All Appointments")
            df = read_appointments()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No appointments found.")
        
        with tab2:
            st.subheader("Create New Appointment")
            patients_df = read_patients()
            doctors_df = read_doctors()
            
            with st.form("create_appointment_form"):
                col1, col2 = st.columns(2)
                with col1:
                    appt_date = st.date_input("Appointment Date", value=date.today())
                    appt_time = st.time_input("Appointment Time")
                with col2:
                    patient_id = st.selectbox("Patient", patients_df['PatientID'].tolist() if not patients_df.empty else [])
                    doctor_id = st.selectbox("Doctor", doctors_df['DoctorID'].tolist() if not doctors_df.empty else [])
                
                submitted = st.form_submit_button("Create Appointment")
                if submitted:
                    create_appointment(appt_date, appt_time, patient_id, doctor_id)
                    st.rerun()
        
        with tab3:
            st.subheader("Update Appointment")
            df = read_appointments()
            patients_df = read_patients()
            doctors_df = read_doctors()
            
            if not df.empty:
                appt_id = st.selectbox("Select Appointment", df['AppointmentID'].tolist())
                selected_appt = df[df['AppointmentID'] == appt_id].iloc[0]
                
                with st.form("update_appointment_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        appt_date = st.date_input("Appointment Date", value=pd.to_datetime(selected_appt['AppointmentDate']).date() if pd.notna(selected_appt['AppointmentDate']) else date.today())
                        appt_time = st.time_input("Appointment Time", value=selected_appt['AppointmentTime'] if pd.notna(selected_appt['AppointmentTime']) else datetime.now().time())
                    with col2:
                        patient_id = st.selectbox("Patient", patients_df['PatientID'].tolist() if not patients_df.empty else [],
                                                index=patients_df['PatientID'].tolist().index(selected_appt['PatientID']) if pd.notna(selected_appt['PatientID']) and selected_appt['PatientID'] in patients_df['PatientID'].tolist() else 0)
                        doctor_id = st.selectbox("Doctor", doctors_df['DoctorID'].tolist() if not doctors_df.empty else [],
                                                index=doctors_df['DoctorID'].tolist().index(selected_appt['DoctorID']) if pd.notna(selected_appt['DoctorID']) and selected_appt['DoctorID'] in doctors_df['DoctorID'].tolist() else 0)
                    
                    submitted = st.form_submit_button("Update Appointment")
                    if submitted:
                        update_appointment(appt_id, appt_date, appt_time, patient_id, doctor_id)
                        st.rerun()
            else:
                st.info("No appointments to update.")
        
        with tab4:
            st.subheader("Delete Appointment")
            df = read_appointments()
            if not df.empty:
                appt_id = st.selectbox("Select Appointment to Delete", df['AppointmentID'].tolist())
                selected_appt = df[df['AppointmentID'] == appt_id].iloc[0]
                st.write(f"**Appointment on {selected_appt['AppointmentDate']} at {selected_appt['AppointmentTime']}**")
                st.write(f"Patient: {selected_appt['PatientName']}")
                st.write(f"Doctor: {selected_appt['DoctorName']}")
                if st.button("Delete Appointment", type="primary"):
                    delete_appointment(appt_id)
                    st.rerun()
            else:
                st.info("No appointments to delete.")
    
    # ==================== GENETIC DISORDERS ====================
    elif menu == "Genetic Disorders":
        st.header("🧬 Genetic Disorder Management")
        
        tab1, tab2, tab3, tab4 = st.tabs(["View All", "Create", "Update", "Delete"])
        
        with tab1:
            st.subheader("All Genetic Disorders")
            df = read_genetic_disorders()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No genetic disorders found.")
        
        with tab2:
            st.subheader("Create New Genetic Disorder")
            with st.form("create_disorder_form"):
                name = st.text_input("Disorder Name")
                gene_symbol = st.text_input("Gene Symbol")
                omim_id = st.text_input("OMIM ID")
                submitted = st.form_submit_button("Create Disorder")
                if submitted:
                    if name:
                        create_genetic_disorder(name, gene_symbol, omim_id)
                        st.rerun()
                    else:
                        st.warning("Please enter disorder name.")
        
        with tab3:
            st.subheader("Update Genetic Disorder")
            df = read_genetic_disorders()
            if not df.empty:
                disorder_id = st.selectbox("Select Disorder", df['DisorderID'].tolist())
                selected_disorder = df[df['DisorderID'] == disorder_id].iloc[0]
                
                with st.form("update_disorder_form"):
                    name = st.text_input("Disorder Name", value=selected_disorder['DisorderName'])
                    gene_symbol = st.text_input("Gene Symbol", value=selected_disorder['GeneSymbol'] if pd.notna(selected_disorder['GeneSymbol']) else "")
                    omim_id = st.text_input("OMIM ID", value=selected_disorder['OMIM_ID'] if pd.notna(selected_disorder['OMIM_ID']) else "")
                    submitted = st.form_submit_button("Update Disorder")
                    if submitted:
                        update_genetic_disorder(disorder_id, name, gene_symbol, omim_id)
                        st.rerun()
            else:
                st.info("No disorders to update.")
        
        with tab4:
            st.subheader("Delete Genetic Disorder")
            df = read_genetic_disorders()
            if not df.empty:
                disorder_id = st.selectbox("Select Disorder to Delete", df['DisorderID'].tolist())
                selected_disorder = df[df['DisorderID'] == disorder_id].iloc[0]
                st.write(f"**{selected_disorder['DisorderName']}**")
                if st.button("Delete Disorder", type="primary"):
                    delete_genetic_disorder(disorder_id)
                    st.rerun()
            else:
                st.info("No disorders to delete.")
    
    # ==================== SPECIAL FEATURES ====================
    elif menu == "Special Features":
        st.header("🔧 Special Features - Procedure & Function")
        
        tab1, tab2 = st.tabs(["📊 Patient Full Report (Procedure)", "🎂 Patient Age (Function)"])
        
        with tab1:
            st.subheader("Get Patient Full Report")
            st.write("This uses the stored procedure `sp_GetPatientFullReport`")
            
            patients_df = read_patients()
            if not patients_df.empty:
                patient_id = st.selectbox("Select Patient", patients_df['PatientID'].tolist())
                
                if st.button("Generate Full Report"):
                    results = call_patient_full_report(patient_id)
                    
                    if results:
                        st.success("Report generated successfully!")
                        
                        if len(results) > 0 and not results[0].empty:
                            st.subheader("1️⃣ Patient Personal Details")
                            st.dataframe(results[0], use_container_width=True)
                        
                        if len(results) > 1 and not results[1].empty:
                            st.subheader("2️⃣ Diagnosed Disorders")
                            st.dataframe(results[1], use_container_width=True)
                        
                        if len(results) > 2 and not results[2].empty:
                            st.subheader("3️⃣ Family History of Disorders")
                            st.dataframe(results[2], use_container_width=True)
                    else:
                        st.info("No data returned from procedure.")
            else:
                st.info("No patients available.")
        
        with tab2:
            st.subheader("Calculate Patient Age")
            st.write("This uses the function `fn_GetPatientAge`")
            
            patients_df = read_patients()
            if not patients_df.empty:
                patient_id = st.selectbox("Select Patient ", patients_df['PatientID'].tolist())
                
                if st.button("Calculate Age"):
                    age = get_patient_age(patient_id)
                    if age is not None:
                        selected_patient = patients_df[patients_df['PatientID'] == patient_id].iloc[0]
                        st.success(f"**{selected_patient['FirstName']} {selected_patient['LastName']}** is **{age} years old**")
                    else:
                        st.error("Could not calculate age.")
            else:
                st.info("No patients available.")
    
    # ==================== AUDIT LOG ====================
    elif menu == "Audit Log":
        st.header("📝 Patient Audit Log (Trigger)")
        st.write("This table is populated by the trigger `trg_PatientAudit` when ContactNo is updated")
        
        df = view_audit_log()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No audit logs found. Update a patient's contact number to see the trigger in action!")

if __name__ == "__main__":
    main()
