# Genetic Disorder Management System - Streamlit UI

A comprehensive database management system with a Streamlit UI for managing genetic disorder information, patients, doctors, clinics, and appointments.

## 🚀 Features

### CRUD Operations

- ✅ **Clinics** - Create, Read, Update, Delete
- ✅ **Doctors** - Create, Read, Update, Delete
- ✅ **Patients** - Create, Read, Update, Delete
- ✅ **Appointments** - Create, Read, Update, Delete
- ✅ **Genetic Disorders** - Create, Read, Update, Delete

### Database Features Implemented

- 📊 **Stored Procedure**: `sp_GetPatientFullReport` - Generates comprehensive patient reports
- 🎂 **Function**: `fn_GetPatientAge` - Calculates patient age from date of birth
- 🔔 **Trigger**: `trg_PatientAudit` - Automatically logs changes to patient contact numbers

## 📋 Prerequisites

1. Python 3.7 or higher
2. MySQL or MariaDB server running
3. Database created from `DBMSProject.sql`

## 🛠️ Installation Steps

### Step 1: Install Required Python Packages

```powershell
pip install streamlit mysql-connector-python pandas
```

### Step 2: Set Up the Database

1. Start your MySQL/MariaDB server
2. Create the database by running the SQL file:
   ```sql
   mysql -u root -p < DBMSProject.sql
   ```
   Or import it using MySQL Workbench or phpMyAdmin

### Step 3: Configure Database Connection

Edit the `DB_CONFIG` dictionary in `app.py` (lines 8-13):

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_username',    # Change this
    'password': 'your_mysql_password', # Change this
    'database': 'genetic_disorder_db'
}
```

### Step 4: Run the Application

```powershell
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### Main Menu Sections

1. **Home** - Dashboard with quick statistics
2. **Clinics** - Manage clinic information
3. **Doctors** - Manage doctor profiles and assignments
4. **Patients** - Manage patient records
5. **Appointments** - Schedule and manage appointments
6. **Genetic Disorders** - Manage genetic disorder database
7. **Special Features** - Access stored procedures and functions
8. **Audit Log** - View trigger-generated audit logs

### Testing the Database Features

#### Testing the Stored Procedure

1. Go to **Special Features** → **Patient Full Report**
2. Select a patient from the dropdown
3. Click "Generate Full Report"
4. View the three result sets:
   - Patient personal details
   - Diagnosed disorders
   - Family history of disorders

#### Testing the Function

1. Go to **Special Features** → **Patient Age**
2. Select a patient from the dropdown
3. Click "Calculate Age"
4. View the calculated age

#### Testing the Trigger

1. Go to **Patients** → **Update** tab
2. Select a patient
3. Change the Contact Number field
4. Click "Update Patient"
5. Go to **Audit Log** to see the logged change

## 🎯 Example Workflow

1. **Add a new patient**

   - Go to Patients → Create
   - Fill in patient details
   - Submit

2. **Schedule an appointment**

   - Go to Appointments → Create
   - Select patient and doctor
   - Set date and time
   - Submit

3. **Generate patient report**

   - Go to Special Features → Patient Full Report
   - Select the patient
   - View comprehensive report

4. **Test the trigger**
   - Update a patient's contact number
   - Check the Audit Log to see the automatic logging

## 🔧 Troubleshooting

### Connection Error

- Verify MySQL is running
- Check username and password in `app.py`
- Ensure database `genetic_disorder_db` exists

### Import Error

- Run: `pip install streamlit mysql-connector-python pandas`

### Port Already in Use

- Run: `streamlit run app.py --server.port 8502` (use different port)

## 📊 Database Schema

The system manages the following entities:

- Clinic
- Doctor
- Patient
- Appointment
- GeneticDisorder
- FamilyHistory
- DiagnosedWith
- FamilyDisorder
- GeneVariant
- Genetic_Test
- Test
- Patient_Audit_Log

## 👨‍💻 Development

To extend the application:

- Add new CRUD functions following the existing pattern
- Create new tabs in the Streamlit UI
- Implement additional stored procedures/functions as needed

## 📝 License

This is an educational project for DBMS coursework.
