import mysql.connector
import os

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="your_username",  # Replace with your MySQL username
    password="your_password",  # Replace with your MySQL password
    database="HospitalDB"
)
cursor = db.cursor()

# Initialize the database and tables if they don't exist
def initialize_database():
    cursor.execute("CREATE DATABASE IF NOT EXISTS HospitalDB")
    cursor.execute("USE HospitalDB")
    
    # Create Patients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Patients (
        PatientID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(50),
        Age INT,
        Gender ENUM('Male', 'Female', 'Other'),
        Diagnosis TEXT,
        AdmissionDate DATE
    )
    """)
    
    # Create Doctors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Doctors (
        DoctorID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(50),
        Specialty VARCHAR(50),
        Phone VARCHAR(15)
    )
    """)
    
    # Create Appointments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Appointments (
        AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
        PatientID INT,
        DoctorID INT,
        AppointmentDate DATE,
        Remarks TEXT,
        FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
        FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
    )
    """)

# Add a new patient
def add_patient():
    name = input("Enter patient's name: ")
    age = int(input("Enter patient's age: "))
    gender = input("Enter patient's gender (Male/Female/Other): ")
    diagnosis = input("Enter diagnosis: ")
    admission_date = input("Enter admission date (YYYY-MM-DD): ")

    query = "INSERT INTO Patients (Name, Age, Gender, Diagnosis, AdmissionDate) VALUES (%s, %s, %s, %s, %s)"
    values = (name, age, gender, diagnosis, admission_date)
    cursor.execute(query, values)
    db.commit()
    print("Patient added successfully!")

# View all patients
def view_patients():
    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()

    print("\nPatient List:")
    print("ID | Name       | Age | Gender | Diagnosis      | Admission Date")
    print("-" * 60)
    for patient in patients:
        print(f"{patient[0]} | {patient[1]} | {patient[2]} | {patient[3]} | {patient[4]} | {patient[5]}")
    print("\n")

# Add a new doctor
def add_doctor():
    name = input("Enter doctor's name: ")
    specialty = input("Enter doctor's specialty: ")
    phone = input("Enter doctor's phone number: ")

    query = "INSERT INTO Doctors (Name, Specialty, Phone) VALUES (%s, %s, %s)"
    values = (name, specialty, phone)
    cursor.execute(query, values)
    db.commit()
    print("Doctor added successfully!")

# View all doctors
def view_doctors():
    cursor.execute("SELECT * FROM Doctors")
    doctors = cursor.fetchall()

    print("\nDoctor List:")
    print("ID | Name       | Specialty      | Phone")
    print("-" * 40)
    for doctor in doctors:
        print(f"{doctor[0]} | {doctor[1]} | {doctor[2]} | {doctor[3]}")
    print("\n")

# Schedule an appointment
def schedule_appointment():
    patient_id = int(input("Enter Patient ID: "))
    doctor_id = int(input("Enter Doctor ID: "))
    appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
    remarks = input("Enter any remarks: ")

    query = "INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate, Remarks) VALUES (%s, %s, %s, %s)"
    values = (patient_id, doctor_id, appointment_date, remarks)
    cursor.execute(query, values)
    db.commit()
    print("Appointment scheduled successfully!")

# View all appointments
def view_appointments():
    cursor.execute("""
    SELECT a.AppointmentID, p.Name AS PatientName, d.Name AS DoctorName, a.AppointmentDate, a.Remarks
    FROM Appointments a
    JOIN Patients p ON a.PatientID = p.PatientID
    JOIN Doctors d ON a.DoctorID = d.DoctorID
    """)
    appointments = cursor.fetchall()

    print("\nAppointment List:")
    print("ID | Patient Name | Doctor Name  | Date       | Remarks")
    print("-" * 60)
    for appointment in appointments:
        print(f"{appointment[0]} | {appointment[1]} | {appointment[2]} | {appointment[3]} | {appointment[4]}")
    print("\n")

# Main menu
def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Hospital Management System")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Add Doctor")
        print("4. View Doctors")
        print("5. Schedule Appointment")
        print("6. View Appointments")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_patient()
        elif choice == '2':
            view_patients()
        elif choice == '3':
            add_doctor()
        elif choice == '4':
            view_doctors()
        elif choice == '5':
            schedule_appointment()
        elif choice == '6':
            view_appointments()
        elif choice == '7':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")
        input("\nPress Enter to continue...")

# Initialize database and run the system
initialize_database()
main_menu()

# Close the database connection
cursor.close()
db.close()