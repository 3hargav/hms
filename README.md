### Steps to reproduce locally   
  
**Technologies Used for Hospital Management System**  
  
- **Flask:** Python web framework for API development  
- **MySQL:** Relational database for data storage  
- **Docker Compose:** Tool for defining and running multi-container applications  
  
### Setup and Installation  
  
1. Clone the repository:  
    ```bash  
	  git clone https://github.com/3hargav/hms.git  
	 ```  

2. Navigate to the project directory:  
    ```bash  
	  cd hms  
	 ```  

2. Build the Docker Images:  
	```bash  
	  docker compose build --no-cache  
	 ```  
3. Start the Docker Containers:  
    ```bash  
	  docker compose up  
	 ```  
The server will start running on `http://localhost:5000/`.  
  
### API Endpoints  
  
### Doctors  
  
- **GET /doctors**: Get all doctors.  
- **GET /doctors/<doctor_id>**: Get a doctor by ID.  
- **POST /doctors**: Create a new doctor.  
  - Required JSON parameters:  
      - name (string): Name of the doctor.  
      - specialization (string): Specialization of the doctor.  
      - contact_info (string): Contact information of the doctor.  
      - department_id (integer, optional): ID of the department the doctor belongs to.  
- **PUT /doctors/<doctor_id>**: Update a doctor.  
  - JSON parameters (optional):  
      - name (string): Name of the doctor.  
      - specialization (string): Specialization of the doctor.  
      - contact_info (string): Contact information of the doctor.  
      - department_id (integer): ID of the department the doctor belongs to.  
- **GET /doctors/<doctor_id>/availability**: Get availability schedule of a doctor.  
- **POST /doctors/<doctor_id>/availability**: Add availability schedule for a doctor.  
  - Required JSON parameters:  
      - day_of_week (string): Day of the week (e.g., Monday).  
      - start_time (string): Start time of availability (format: HH:MM).  
      - end_time (string): End time of availability (format: HH:MM).  
  
- **GET /doctors/<doctor_id>/appointments**: Get appointments for a doctor.  
  - Required query parameters:  
      - start_time (string): Start time of the appointments range (format: YYYY-MM-DD HH:MM:SS).  
      - end_time (string): End time of the appointments range (format: YYYY-MM-DD HH:MM:SS).  
  - Returns a list of appointments for the specified doctor within the given time range.  
  
### Patients  
  
- **GET /patients/pagination**: Get all patients with pagination.  
  - Optional query parameters:  
      - page (integer): Page number (default: 1).  
      - per_page (integer): Number of patients per page (default: 10).  
- **GET /patients/<patient_id>**: Get a patient by ID.  
- **POST /patients**: Create a new patient.  
  - Required JSON parameters:  
      - name (string): Name of the patient.  
      - age (integer): Age of the patient.  
      - gender (string): Gender of the patient.  
      - contact_info (string): Contact information of the patient.  
- **GET /patients/<patient_id>/medical_history**: Get Medical History for a patient.  
  - Returns a list of medical histories for the specified patient.  
- **POST /patients/medical_history**: Create a new medical history.  
  - Required JSON parameters:  
      - patient_id (integer).  
      - previous_diagnoses (string):.  
      - allergies (string).  
      - medications (string).  
- **GET /patients/<patient_id>/appointments**: Get appointments for a patient.  
  - Returns a list of appointments for the specified patient.  
  
### Departments  
  
- **GET /departments**: Get all departments.  
- **GET /departments/<department_id>**: Get a department by ID.  
- **POST /departments**: Create a new department.  
  - Required JSON parameters:  
      - name (string): Name of the department.  
      - services_offered (string): services.  
  
### Appointments  
  
- **GET /appointments**: Get all appointments.  
- **GET /appointments/<appointment_id>**: Get an appointment by ID.  
- **POST /appointments**: Create a new appointment.  
  - Required JSON parameters:  
      - patient_id (integer): ID of the patient.  
      - doctor_id (integer): ID of the doctor.  
      - start_time (string): Start time of the appointment (format: YYYY-MM-DD HH:MM:SS).  
      - end_time (string): End time of the appointment (format: YYYY-MM-DD HH:MM:SS).  
  
### Search and Filtering    
-  **GET /search**:   
    - Search for Patients, Doctors, and Departments by some attribute.   
    - Required query parameters:   
       - type (string): Type of entity to search (patient, doctor, or department).   
       - query (string): Search query.   
-  **GET /filter**:   
    - Filtering Options (e.g., Availability and Specialization). -   
    - Required query parameters:   
       - type (string): Type of filter (availability or specialization).   
       - value (string): Filter value.
