
import sys
from datetime import datetime

# ==========================================
# Data Containers
# ==========================================
ROOM_TYPES = ("ICU", "Private", "Shared", "Emergency")

DISEASES_SET = {"Flu", "Diabetes", "Heart Disease", "Cancer"}

departments = {
    "Emergency": [],
    "ICU": [],
    "Cardiology": [],
    "Neurology": [],
    "Pediatrics": [],
    "Orthopedic": []
}

# ==========================================
# Validations
# ==========================================
def validate_age(age):
    try:
        val = int(age)
        return val > 0
    except ValueError:
        return False

def validate_phone(phone):
    return phone.isdigit()

def validate_salary(salary):
    try:
        val = float(salary)
        return val >= 0
    except ValueError:
        return False

def validate_date_not_past(date_str):
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return input_date >= datetime.now().date()
    except ValueError:
        return False

# ==========================================
# Required Classes
# ==========================================
class Person:
    def __init__(self, person_id, name, age, gender, phone):
        self.id = person_id
        self.name = name
        self.age = int(age)
        self.gender = gender
        self.phone = phone

    def display_info(self):
        print(f"ID: {self.id} | Name: {self.name} | Age: {self.age} | Gender: {self.gender} | Phone: {self.phone}")

    def update_info(self, name=None, age=None, gender=None, phone=None):
        if name: self.name = name
        if age and validate_age(age): self.age = int(age)
        if gender: self.gender = gender
        if phone and validate_phone(phone): self.phone = phone


class Doctor(Person):
    def __init__(self, doctor_id, name, age, gender, phone, specialization, salary, available_days):
        super().__init__(doctor_id, name, age, gender, phone)
        self.doctor_id = doctor_id
        self.specialization = specialization
        self.salary = float(salary)
        self.available_days = available_days
        self.assigned_patients = []

    def assign_patient(self, patient_id):
        if patient_id not in self.assigned_patients:
            self.assigned_patients.append(patient_id)

    def show_patients(self):
        print(f"Doctor {self.name}'s Patients: {', '.join(self.assigned_patients) if self.assigned_patients else 'None'}")

    def display_info(self):
        super().display_info()
        print(f"Spec: {self.specialization} | Salary: ${self.salary:.2f} | Days: {self.available_days} | Patients: {len(self.assigned_patients)}")


class Nurse(Person):
    def __init__(self, nurse_id, name, age, gender, phone, department, shift, salary):
        super().__init__(nurse_id, name, age, gender, phone)
        self.department = department
        self.shift = shift
        self.salary = float(salary)
        self.assigned_room = None

    def assign_room(self, room_number):
        self.assigned_room = room_number

    def display_info(self):
        super().display_info()
        print(f"Department: {self.department} | Shift: {self.shift} | Salary: ${self.salary:.2f} | Assigned Room: {self.assigned_room}")


class Receptionist(Person):
    def __init__(self, rec_id, name, age, gender, phone, shift, salary):
        super().__init__(rec_id, name, age, gender, phone)
        self.shift = shift
        self.salary = float(salary)

    def register_patient(self, hospital_obj, patient_obj):
        hospital_obj.add_entity(hospital_obj.patients, patient_obj, 'id')

    def schedule_appointment(self, hospital_obj, appointment_obj):
        hospital_obj.add_entity(hospital_obj.appointments, appointment_obj, 'appointment_id')


class Pharmacist(Person):
    def __init__(self, pharm_id, name, age, gender, phone, salary, pharmacy_name):
        super().__init__(pharm_id, name, age, gender, phone)
        self.salary = float(salary)
        self.pharmacy_name = pharmacy_name

    def issue_medicine(self, patient_name, medicine):
        print(f"Medicine '{medicine}' issued to {patient_name} by Pharmacy {self.pharmacy_name}.")

    def view_prescriptions(self):
        print("Displaying all patient prescriptions...")


class LabTechnician(Person):
    def __init__(self, tech_id, name, age, gender, phone, laboratory_name, salary):
        super().__init__(tech_id, name, age, gender, phone)
        self.laboratory_name = laboratory_name
        self.salary = float(salary)
        self.results = {}

    def add_test_result(self, patient_id, result):
        self.results[patient_id] = result

    def view_results(self):
        for pid, res in self.results.items():
            print(f"Patient ID {pid}: {res}")


class Staff(Person):
    def __init__(self, staff_id, name, age, gender, phone, job_title, salary, shift):
        super().__init__(staff_id, name, age, gender, phone)
        self.job_title = job_title
        self.salary = float(salary)
        self.shift = shift

    def display_info(self):
        super().display_info()
        print(f"Job Title: {self.job_title} | Shift: {self.shift} | Salary: ${self.salary:.2f}")


class Patient(Person):
    def __init__(self, patient_id, name, age, gender, phone, disease, blood_group, admission_date):
        super().__init__(patient_id, name, age, gender, phone)
        self.patient_id = patient_id
        self.disease = disease
        DISEASES_SET.add(disease)
        self.blood_group = blood_group
        self.doctor = None
        self.room_number = None
        self.admission_date = admission_date
        self.status = "Admitted"

    def assign_doctor(self, doctor_name):
        self.doctor = doctor_name

    def assign_room(self, room_obj):
        if room_obj.add_patient(self.patient_id):
            self.room_number = room_obj.room_number
            return True
        return False

    def discharge(self):
        self.status = "Discharged"

    def display_info(self):
        super().display_info()
        print(f"Disease: {self.disease} | Blood: {self.blood_group} | Doctor: {self.doctor} | Room: {self.room_number} | Status: {self.status}")


class Room:
    def __init__(self, room_number, room_type, capacity):
        self.room_number = room_number
        self.room_type = room_type if room_type in ROOM_TYPES else "Shared"
        self.capacity = int(capacity)
        self.current_patients = []

    def add_patient(self, patient_id):
        if len(self.current_patients) < self.capacity:
            self.current_patients.append(patient_id)
            return True
        return False

    def remove_patient(self, patient_id):
        if patient_id in self.current_patients:
            self.current_patients.remove(patient_id)

    def room_status(self):
        print(f"Room Number: {self.room_number} | Type: {self.room_type} | Capacity: {self.capacity} | Patients: {len(self.current_patients)}/{self.capacity}")


class Appointment:
    def __init__(self, appointment_id, patient_id, doctor_id, date, time):
        self.appointment_id = appointment_id
        self.patient = patient_id
        self.doctor = doctor_id
        self.date = date
        self.time = time

    def create(self):
        print(f"Appointment {self.appointment_id} scheduled for Patient {self.patient} with Doctor {self.doctor}.")

    def cancel(self):
        print(f"Appointment {self.appointment_id} cancelled.")

    def display(self):
        print(f"App ID: {self.appointment_id} | Patient: {self.patient} | Doctor: {self.doctor} | Date: {self.date} | Time: {self.time}")


class Bill:
    def __init__(self, bill_id, patient_id, consultation_fee, medicine_cost, room_cost):
        self.bill_id = bill_id
        self.patient = patient_id
        self.consultation_fee = max(0.0, float(consultation_fee))
        self.medicine_cost = max(0.0, float(medicine_cost))
        self.room_cost = max(0.0, float(room_cost))
        self.total_cost = self.calculate_total()

    def calculate_total(self):
        return self.consultation_fee + self.medicine_cost + self.room_cost

    def print_bill(self):
        print("\n" + "="*30)
        print(f"BILL ID: {self.bill_id}")
        print(f"Patient ID: {self.patient}")
        print(f"Consultation Fee: ${self.consultation_fee:.2f}")
        print(f"Medicine Cost:     ${self.medicine_cost:.2f}")
        print(f"Room Cost:         ${self.room_cost:.2f}")
        print(f"TOTAL AMOUNT:      ${self.total_cost:.2f}")
        print("="*30 + "\n")


# ==========================================
# Main Hospital Class
# ==========================================
class Hospital:
    def __init__(self):
        self.doctors = []
        self.nurses = []
        self.patients = []
        self.receptionists = []
        self.pharmacists = []
        self.lab_technicians = []
        self.staff = []
        self.rooms = []
        self.appointments = []
        self.bills = []

    def add_entity(self, target_list, entity_obj, id_attr):
        entity_id = getattr(entity_obj, id_attr)
        if self.search_entity(target_list, id_attr, entity_id):
            print("Error: ID must be unique!")
            return False
        target_list.append(entity_obj)
        print("Added successfully.")
        return True

    def view_all(self, target_list):
        if not target_list:
            print("No records found.")
            return
        for item in target_list:
            if hasattr(item, 'display_info'): item.display_info()
            elif hasattr(item, 'room_status'): item.room_status()
            elif hasattr(item, 'display'): item.display()
            elif hasattr(item, 'print_bill'): item.print_bill()

    def search_entity(self, target_list, id_attr, value):
        for item in target_list:
            if str(getattr(item, id_attr)) == str(value):
                return item
        return None

    def update_entity(self, target_list, id_attr, value):
        item = self.search_entity(target_list, id_attr, value)
        if item:
            new_name = input("Enter new Name (press Enter to skip): ")
            new_phone = input("Enter new Phone (press Enter to skip): ")
            if hasattr(item, 'update_info'):
                item.update_info(name=new_name if new_name else None, phone=new_phone if new_phone else None)
            print("Updated successfully.")
        else:
            print("Record not found.")

    def delete_entity(self, target_list, id_attr, value):
        item = self.search_entity(target_list, id_attr, value)
        if item:
            target_list.remove(item)
            print("Deleted successfully.")
            return True
        print("Record not found.")
        return False


h_sys = Hospital()

# ==========================================
# Helper Menu & System Functions
# ==========================================
def login():
    print("=== HOSPITAL SYSTEM LOGIN ===")
    user = input("Username: ")
    pwd = input("Password: ")
    print(f"Welcome, {user}!\n")
    return True

def exit_program():
    print("Exiting System. Goodbye!")
    sys.exit()

def generic_sub_menu(title, target_list, id_attr, create_func):
    while True:
        print(f"\n--- {title} Management ---")
        print("1. Add")
        print("2. View All")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Back")
        
        choice = input("Select choice (1-6): ")
        if choice == '1':
            obj = create_func()
            if obj: h_sys.add_entity(target_list, obj, id_attr)
        elif choice == '2':
            h_sys.view_all(target_list)
        elif choice == '3':
            val = input(f"Enter {id_attr}: ")
            res = h_sys.search_entity(target_list, id_attr, val)
            if res:
                if hasattr(res, 'display_info'): res.display_info()
                elif hasattr(res, 'room_status'): res.room_status()
                elif hasattr(res, 'display'): res.display()
                elif hasattr(res, 'print_bill'): res.print_bill()
            else: print("Not found.")
        elif choice == '4':
            val = input(f"Enter {id_attr}: ")
            h_sys.update_entity(target_list, id_attr, val)
        elif choice == '5':
            val = input(f"Enter {id_attr}: ")
            h_sys.delete_entity(target_list, id_attr, val)
        elif choice == '6':
            break

def create_doctor():
    d_id = input("Doctor ID: ")
    name = input("Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    phone = input("Phone: ")
    spec = input("Specialization: ")
    salary = input("Salary: ")
    days = input("Available Days: ")
    
    if validate_age(age) and validate_phone(phone) and validate_salary(salary):
        return Doctor(d_id, name, age, gender, phone, spec, salary, days)
    print("Invalid Input Data!")
    return None

def create_patient():
    p_id = input("Patient ID: ")
    name = input("Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    phone = input("Phone: ")
    disease = input("Disease: ")
    blood = input("Blood Group: ")
    adm_date = datetime.now().strftime("%Y-%m-%d")
    
    if validate_age(age) and validate_phone(phone):
        return Patient(p_id, name, age, gender, phone, disease, blood, adm_date)
    print("Invalid Input Data!")
    return None

def create_nurse():
    n_id = input("Nurse ID: ")
    name = input("Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    phone = input("Phone: ")
    dept = input("Department: ")
    shift = input("Shift (Day/Night): ")
    salary = input("Salary: ")
    if validate_age(age) and validate_phone(phone) and validate_salary(salary):
        return Nurse(n_id, name, age, gender, phone, dept, shift, salary)
    return None

def create_receptionist():
    r_id = input("Receptionist ID: ")
    name = input("Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    phone = input("Phone: ")
    shift = input("Shift: ")
    salary = input("Salary: ")
    if validate_age(age) and validate_phone(phone) and validate_salary(salary):
        return Receptionist(r_id, name, age, gender, phone, shift, salary)
    return None

def create_pharmacist():
    ph_id = input("Pharmacist ID: ")
    name = input("Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    phone = input("Phone: ")
    salary = input("Salary: ")
    ph_name = input("Pharmacy Name: ")
    if validate_age(age) and validate_phone(phone) and validate_salary(salary):
        return Pharmacist(ph_id, name, age, gender, phone, salary, ph_name)
    return None

def create_lab_tech():
    lt_id = input("Lab Tech ID: ")
    name = input("Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    phone = input("Phone: ")
    salary = input("Salary: ")
    lab_name = input("Laboratory Name: ")
    if validate_age(age) and validate_phone(phone) and validate_salary(salary):
        return LabTechnician(lt_id, name, age, gender, phone, lab_name, salary)
    return None

def create_staff():
    s_id = input("Staff ID: ")
    name = input("Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    phone = input("Phone: ")
    job = input("Job Title (Cleaner/Security/Maintenance): ")
    salary = input("Salary: ")
    shift = input("Shift: ")
    if validate_age(age) and validate_phone(phone) and validate_salary(salary):
        return Staff(s_id, name, age, gender, phone, job, salary, shift)
    return None

def create_room():
    r_num = input("Room Number: ")
    print(f"Available Types: {ROOM_TYPES}")
    r_type = input("Room Type: ")
    cap = input("Capacity: ")
    return Room(r_num, r_type, cap)

def create_appointment():
    app_id = input("Appointment ID: ")
    p_id = input("Patient ID: ")
    d_id = input("Doctor ID: ")
    date_str = input("Date (YYYY-MM-DD): ")
    time_str = input("Time (e.g. 10:00 AM): ")
    
    if validate_date_not_past(date_str):
        return Appointment(app_id, p_id, d_id, date_str, time_str)
    print("Error: Appointment date cannot be in the past!")
    return None

def create_bill():
    b_id = input("Bill ID: ")
    p_id = input("Patient ID: ")
    c_fee = float(input("Consultation Fee: "))
    m_cost = float(input("Medicine Cost: "))
    r_cost = float(input("Room Cost: "))
    if c_fee >= 0 and m_cost >= 0 and r_cost >= 0:
        return Bill(b_id, p_id, c_fee, m_cost, r_cost)
    print("Error: Bills cannot contain negative values!")
    return None

# ==========================================
# Reports Display Function
# ==========================================
def show_reports():
    print("\n" + "="*15 + " REPORTS " + "="*15)
    print(f"Total Doctors: {len(h_sys.doctors)}")
    print(f"Total Nurses: {len(h_sys.nurses)}")
    print(f"Total Patients: {len(h_sys.patients)}")
    print(f"Total Rooms: {len(h_sys.rooms)}")
    
    occupied = sum(1 for r in h_sys.rooms if len(r.current_patients) > 0)
    print(f"Occupied Rooms: {occupied}")
    print(f"Empty Rooms: {len(h_sys.rooms) - occupied}")
    
    total_income = sum(b.total_cost for b in h_sys.bills)
    print(f"Total Income: ${total_income:.2f}")
    
    if h_sys.patients:
        avg_age = sum(p.age for p in h_sys.patients) / len(h_sys.patients)
        print(f"Average Patient Age: {avg_age:.1f}")
        
        diseases = [p.disease for p in h_sys.patients]
        most_common = max(set(diseases), key=diseases.count)
        print(f"Most Common Disease: {most_common}")
    else:
        print("Average Patient Age: N/A")
        print("Most Common Disease: N/A")
    print("="*39 + "\n")

# ==========================================
# Main Menu Driver
# ==========================================
def show_main_menu():
    while True:
        print("\n Hospital Management System ")
        print("1. Doctors Management")
        print("2. Patients Management")
        print("3. Nurses Management")
        print("4. Receptionists Management")
        print("5. Pharmacists Management")
        print("6. Lab Technicians Management")
        print("7. Staff Management")
        print("8. Rooms Management")
        print("9. Appointments")
        print("10. Billing")
        print("11. Reports")
        print("12. Exit")
        
        choice = input("Select Option (1-12): ")
        
        if choice == '1': generic_sub_menu("Doctor", h_sys.doctors, 'doctor_id', create_doctor)
        elif choice == '2': generic_sub_menu("Patient", h_sys.patients, 'patient_id', create_patient)
        elif choice == '3': generic_sub_menu("Nurse", h_sys.nurses, 'id', create_nurse)
        elif choice == '4': generic_sub_menu("Receptionist", h_sys.receptionists, 'id', create_receptionist)
        elif choice == '5': generic_sub_menu("Pharmacist", h_sys.pharmacists, 'id', create_pharmacist)
        elif choice == '6': generic_sub_menu("Lab Technician", h_sys.lab_technicians, 'id', create_lab_tech)
        elif choice == '7': generic_sub_menu("Staff", h_sys.staff, 'id', create_staff)
        elif choice == '8': generic_sub_menu("Room", h_sys.rooms, 'room_number', create_room)
        elif choice == '9': generic_sub_menu("Appointment", h_sys.appointments, 'appointment_id', create_appointment)
        elif choice == '10': generic_sub_menu("Billing", h_sys.bills, 'bill_id', create_bill)
        elif choice == '11': show_reports()
        elif choice == '12': exit_program()
        else: print("Invalid Choice!")

if __name__ == "__main__":
    login()
    show_main_menu()