from datetime import date

import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
from psycopg2.extras import DictCursor
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'static/Uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

########################################################################################################################
########################################################################################################################

def connect_db():
    conn = psycopg2.connect(
        dbname="Emergency_Room",
        user="Emergency_Room_owner",
        password="MnYato6AVF5r",
        host="ep-ancient-water-a2txwc34.eu-central-1.aws.neon.tech",
        port="5432"
    )
    return conn

########################################################################################################################
########################################################################################################################
# Route for the home page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

########################################################################################################################
########################################################################################################################

@app.route('/patientprofile')
def patientprofile():
    pid = request.args.get('pid')

    conn = connect_db()
    cursor = conn.cursor(cursor_factory=DictCursor)

    # Example query to fetch specific attributes
    cursor.execute("SELECT * FROM patient where pid=%(pid)s",{"pid": pid})
    conn.commit()
    patient = dict(cursor.fetchone())

    return render_template('PatientProfile.html',patient=patient)

########################################################################################################################
########################################################################################################################

# Route for the registration page
@app.route('/registration')
def registration():
    return render_template('registration.html')

########################################################################################################################
########################################################################################################################
@app.route('/submit_registration',methods=['GET', 'POST'])
def submit_registration():
    conn=connect_db()
    if request.method == 'GET':
         return render_template('registration.html')

    if request.method == 'POST':
        pssn=request.form.get('pssn')
        pid=request.form.get('pid')
        fname=request.form.get('fname')
        mname=request.form.get('mname')
        lname=request.form.get('lname')
        occupation=request.form.get('occupation')
        nationality=request.form.get('nationality')
        email=request.form.get('email')
        triage=request.form.get('triage')
        mobileNumber=request.form.get('mobileNumber')
        age=request.form.get('age')
        dateofbirth=request.form.get('dateofbirth')
        sex=request.form.get('sex')
        bloodtype=request.form.get('bloodtype')
        address=request.form.get('address')
        profilepicture=request.form.get('profilepicture')
        password=request.form.get('password')

        cur=conn.cursor()
        cur.execute('INSERT INTO patient(pssn,pid,fname,mname,lname,occupation,nationality,email,triage,mobilenumber,age,dateofbirth,sex,bloodtype,address,profilepicture,password) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (pssn,pid,fname,mname,lname,occupation,nationality,email,triage,mobileNumber,age,dateofbirth,sex,bloodtype,address,profilepicture,password))
        conn.commit()

        return redirect('/registration')

########################################################################################################################
########################################################################################################################

# Route for the login/signup page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        speciality = request.form.get('Speciality')
        key = request.form.get('id')
        password = request.form.get('password')

        conn = connect_db()
        cursor = conn.cursor(cursor_factory=DictCursor)

        if speciality == "doctor":
            cursor.execute("SELECT * FROM doctor WHERE did=%(did)s AND password=%(password)s", {"did": key, "password": password})
            conn.commit()
            result = cursor.fetchone()
            if result:
                return redirect(url_for('doctorprofile',did=key))
            else:
                return "Invalid credentials for doctor", 401

        elif speciality == "nurse":
            cursor.execute("SELECT * FROM nurse WHERE nid=%(nid)s AND password=%(password)s", {"nid": key, "password": password})
            conn.commit()
            result = cursor.fetchone()
            if result:
                return redirect(url_for('nurseprofile',nid=key))
            else:
                return "Invalid credentials for nurse", 401

        elif speciality == "patient":
            cursor.execute("SELECT * FROM patient WHERE pid=%(pid)s AND password=%(password)s", {"pid": key,"password": password})
            conn.commit()
            result = cursor.fetchone()
            if result:
                return redirect(url_for('patientprofile', pid=key))  # Redirect to the patient's profile page
            else:
                return "Invalid credentials for patient", 401

        elif speciality == "admin":
            cursor.execute("SELECT * FROM admin WHERE aid=%(aid)s AND password=%(password)s", {"aid": key, "password": password})
            conn.commit()
            result = cursor.fetchone()
            if result:
                return redirect(url_for('dashboard', aid=key))
            else:
                return "Invalid credentials for Admin", 401
        else:

            return "Invalid speciality", 400  # Handle case if no speciality is selected


########################################################################################################################
########################################################################################################################

@app.route('/doclist')
def doctorlist():
    conn = connect_db()
    cursor = conn.cursor()

    # Example query to fetch specific attributes
    cursor.execute("SELECT did, fname, lname,speciality FROM doctor")
    data = cursor.fetchall()

    conn.close()

    # Format data for HTML
    formatted_data = []
    for row in data:
        formatted_data.append({'did': row[0], 'fname': row[1], 'lname': row[2], 'speciality': row[3]})
    print(formatted_data)
    return render_template('doctor_list.html', data=formatted_data)


########################################################################################################################
########################################################################################################################

@app.route('/N_list')
def nur_list():
    conn = connect_db()
    cursor = conn.cursor()

    # Example query to fetch specific attributes
    cursor.execute("SELECT nid, fname, lname,department FROM nurse")
    datan = cursor.fetchall()

    conn.close()

    # Format data for HTML
    formatted_datan = []
    for row in datan:
        formatted_datan.append({'nid': row[0], 'fname': row[1], 'lname': row[2], 'department': row[3]})
    print(formatted_datan)
    return render_template('Nurse_list.html', data=formatted_datan)


########################################################################################################################
########################################################################################################################

@app.route('/P_list')
def pa_list():
    conn = connect_db()
    cursor = conn.cursor()

    # Example query to fetch specific attributes
    cursor.execute("SELECT pid, fname, lname,triage, bnumber FROM patient")
    datap = cursor.fetchall()

    conn.close()

    # Format data for HTML
    formatted_datap = []
    for row in datap:
        formatted_datap.append({'pid': row[0], 'fname': row[1], 'lname': row[2], 'triage': row[3],'bnumber': row[4]})
    print(formatted_datap)
    return render_template('Patient_List.html', data=formatted_datap)


########################################################################################################################
########################################################################################################################

@app.route('/R_list')
def reg_list():
    conn = connect_db()
    cursor = conn.cursor()

    # Example query to fetch specific attributes
    cursor.execute("SELECT rid, fname, lname FROM receptionist")
    datar = cursor.fetchall()

    conn.close()

    # Format data for HTML
    formatted_datar = []
    for row in datar:
        formatted_datar.append({'rid': row[0], 'fname': row[1], 'lname': row[2]})
    print(formatted_datar)
    return render_template('Register_list.html', data=formatted_datar)

########################################################################################################################
########################################################################################################################

@app.route('/contactus')
def contactus():
    return render_template('Contact.html')

########################################################################################################################
########################################################################################################################

@app.route('/data')
def get_data():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
          SELECT speciality, count(*)
          FROM doctor
          group by speciality
      """)
    data = cursor.fetchall()

    conn.close()
    data_list = [{"speciality": row[0], "count": row[1]} for row in data]

    return jsonify (data_list)

########################################################################################################################
########################################################################################################################

@app.route('/datap')
def get_data2():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""SELECT triage, count(*) AS count FROM patient
         group by triage""")
    datap = cursor.fetchall()

    conn.close()
    data_list1 = [{"triage": row[0], "count": row[1]} for row in datap]

    return jsonify(data_list1)

########################################################################################################################
########################################################################################################################

@app.route('/Analytics')
def ana():
    return render_template('Analytics.html')
@app.route('/home')
def home():
    return render_template('index.html')
########################################################################################################################
########################################################################################################################

@app.route('/doctorprofile')
def doctorprofile():
    did = request.args.get('did')

    # Safeguard connection handling with a try-except-finally block
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=DictCursor)

        # Fetch doctor information
        cursor.execute("SELECT * FROM doctor WHERE did=%(did)s", {"did": did})
        doctor = dict(cursor.fetchone())

        # Fetch patient information
        cursor.execute("SELECT pid, fname, lname, triage, bnumber FROM patient JOIN treat ON patient.PSSN=Treat.patientssn")
        datap = cursor.fetchall()

        # Format data for HTML
        formatted_datap = [
            {'pid': row['pid'], 'fname': row['fname'], 'lname': row['lname'], 'triage': row['triage'], 'bnumber': row['bnumber']}
            for row in datap
        ]

        cursor.execute("SELECT working_day FROM doctor_schedule WHERE did = did",)
        days = cursor.fetchall()

        # Format days for HTML
        working_days = [row['working_day'] for row in days]


    except Exception as e:
        # Log or handle the exception appropriately
        print(f"Error: {e}")
        return "An error occurred while processing the request.", 500

    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

    return render_template('DoctorProfile.html', doctor=doctor, patients=formatted_datap, working_days=working_days)



# @app.route('/doctorprofile')
# def doctorprofile():
#     did = request.args.get('did')
#
#     conn = connect_db()
#     cursor = conn.cursor(cursor_factory=DictCursor)
#
#     # Example query to fetch specific attributes
#     cursor.execute("SELECT * FROM doctor WHERE did=%(did)s", {"did": did})
#     conn.commit()
#     doctor = dict(cursor.fetchone())
#
#     # Example query to fetch specific attributes
#     cursor.execute("SELECT pid, fname, lname,triage, bnumber FROM patient")
#     datap = cursor.fetchall()
#
#     conn.close()
#
#     # Format data for HTML
#     formatted_datap = []
#     for row in datap:
#         formatted_datap.append({'pid': row[0], 'fname': row[1], 'lname': row[2], 'triage': row[3], 'bnumber': row[4]})
#
#     return render_template('DoctorProfile.html', doctor=doctor, patient= formatted_datap)

##################################################################################################
##################################################################################################

@app.route('/submit_patient_record', methods=['POST'])
def submit_patient_record():
    try:
        # Get form data
        patient_id = request.form['patient_id']
        doctor_id = request.form['did']  # Fetch the current doctor's ID
        PSSN = request.form['PSSN']
        DSSN = request.form['DSSN']
        condition = request.form['condition']
        triage = request.form['triage']
        treatment = request.form['treatment']
        recommendation = request.form['recommendation']

        current_date = date.today()

        print("patient_id id3:-", patient_id)


        # Handle file upload
        scan_file = request.files['scan']
        if scan_file and allowed_file(scan_file.filename):
            filename = secure_filename(scan_file.filename)
            scan_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            scan_file.save(scan_path)
        else:
            return "Invalid file type.", 400

        print("Form Data:", request.form.to_dict())

        # Insert into database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""  
            INSERT INTO Patient_Record (
                patient_id, PSSN, DSSN, date, condition, triage, treatment, recommendation, scans
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (patient_id, PSSN, DSSN, current_date, condition, triage, treatment, recommendation, scan_path))
        conn.commit()

        # cursor = conn.cursor()
        # cursor.execute("""
        #        SELECT doctor.did
        #        FROM doctor
        #        WHERE doctor.DSSN=%(DSSN)s
        #    """, (doctor_id,))

        print("doctor_id id3:-", doctor_id)

        return redirect(url_for('doctorprofile', did=doctor_id))

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred.", 500

    finally:
        if conn:
            conn.close()

##################################################################################################
##################################################################################################

@app.route('/add_patient_record')
def add_patient_record():
    # Fetch query parameters from the request
    patient_id = request.args.get('pid')
    #doctor_id = request.args.get('did')  # Fetch the current doctor's ID

    print("patient_id id1:-", patient_id)

    # Retrieve PSSN and DSSN from the database (example query)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT patient.pssn, treat.doctorssn
        FROM patient
        JOIN treat ON patient.pssn = treat.patientssn
        WHERE patient.pid = %s
    """, (patient_id,))

    record = cursor.fetchone()
    conn.close()

    if record:
        PSSN, DSSN = record
    else:
        PSSN, DSSN = None, None  # Handle missing data

    print("patient_id id2:-", patient_id)

    return render_template('AddPatientRecord.html', patient_id=patient_id, PSSN=PSSN, DSSN=DSSN)


#
# @app.route('/add_patient_record')
# def add_patient_record():
#     patient_id = request.args.get('pid')
#     doctor_id = request.args.get('did')  # Fetch the current doctor's ID
#     return render_template('AddPatientRecord.html', patient_id=patient_id, doctor_id=doctor_id)

##################################################################################################
##################################################################################################

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        # Handle form submission and save the data
        did = request.form.get('did')
        department = request.form.get('department')
        specialisation = request.form.get('specialisation')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        email = request.form.get('email')
        # Add logic to save the updated data to the database
        return redirect(url_for('profile', doctor_id=did))

    # Render the edit profile form
    return render_template('edit_profile.html')  # Make sure this template exists


########################################################################################################################
########################################################################################################################

@app.route('/nurseprofile')
def nurseprofile():
    nid = request.args.get('nid')

    conn = connect_db()
    cursor = conn.cursor(cursor_factory=DictCursor)

    # Example query to fetch specific attributes
    cursor.execute("SELECT * FROM nurse WHERE nid=%(nid)s", {"nid": nid})
    conn.commit()
    nurse = dict(cursor.fetchone())

    return render_template('NurseProfile.html', nurse=nurse)

########################################################################################################################
########################################################################################################################

@app.route('/dashboard')
def dashboard():
    return render_template('dashtest.html')

########################################################################################################################
########################################################################################################################

@app.route('/dataN')
def get_data3():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""SELECT department, count(*) AS count FROM nurse
        group by department""")
    dataN= cursor.fetchall()

    conn.close()
    data_list2 = [{"department": row[0], "count": row[1]} for row in dataN]

    return jsonify(data_list2)

########################################################################################################################
########################################################################################################################

@app.route('/P_list')
def get_patient():
    return render_template('Patient_list.html')

########################################################################################################################
########################################################################################################################

@app.route('/N_list')
def get_nurse():
    return render_template('Nurse_list.html')

########################################################################################################################
########################################################################################################################

@app.route('/reception')
def reception():
    return render_template('Register_list.html')

########################################################################################################################
########################################################################################################################

@app.route('/dropd',methods=['POST'])
def delete_doctor():
    try:
        doctor_id = request.form.get('doctor_id')
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM doctor WHERE did = %s", (doctor_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('doctorlist'))  # Correct usage of url_for
    except Exception as e:
        print(f"Error deleting doctor: {e}")
        return "Error deleting doctor.", 500

########################################################################################################################
########################################################################################################################

@app.route('/dropnn',methods=['POST'])
def delete_nurse():
    try:
        nurse_id = request.form.get('nurse_id')
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM nurse WHERE nid = %s", (nurse_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('nur_list'))  # Correct usage of url_for
    except Exception as e:
        print(f"Error deleting doctor: {e}")
        return "Error deleting doctor.", 500

########################################################################################################################
########################################################################################################################

@app.route('/droprr',methods=['POST'])
def delete_reception():
    try:
        reception_id = request.form.get('reception_id')
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM receptionist WHERE rid = %s", (reception_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('reg_list'))  # Correct usage of url_for
    except Exception as e:
        print(f"Error deleting doctor: {e}")
        return "Error deleting doctor.", 500

########################################################################################################################
########################################################################################################################

@app.route('/submit_doctor_reg', methods=['GET', 'POST'])
def submit_doctor_reg():
    conn = connect_db()
    if request.method == 'GET':
        return render_template('Reg_doctor.html', data=conn)

    if request.method == 'POST':
        dssn = request.form.get('dssn')
        did = request.form.get('did')
        fname = request.form.get('fname')
        mname = request.form.get('mname')
        lname = request.form.get('lname')
        dateofbirth = request.form.get('dateofbirth')
        sex = request.form.get('sex')
        address = request.form.get('address')
        mobileNumber = request.form.get('mobileNumber')
        age = request.form.get('age')
        department = request.form.get('department')
        speciality = request.form.get('speciality')
        email = request.form.get('email')
        profilepicture = request.form.get('profilepicture')
        password = request.form.get('password')

        try:

            cur = conn.cursor()
            cur.execute(
                'INSERT INTO doctor(dssn, did, fname, mname, lname, dateofbirth, sex, address, mobileNumber, age, department, speciality, email, profilepicture, password) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (
                    dssn, did, fname, mname, lname, dateofbirth, sex, address, mobileNumber, age, department, speciality, email,
                    profilepicture, password
                )
            )
            conn.commit()
            return render_template('Reg_doctor.html', message="Doctor registered successfully!")  # Success message
        except psycopg2.errors.CheckViolation as e:
            print(f"Error: {e}")
            return render_template('Reg_doctor.html', error_message="Check Violation: Please review the entered data for any constraints.")
        except Exception as e:
            print(f"Error registering doctor: {e}")
            return render_template('Reg_doctor.html', error_message="An error occurred while registering the doctor.")
        finally:
            conn.close()

########################################################################################################################
########################################################################################################################

@app.route('/submit_nurse_reg', methods=['GET', 'POST'])
def submit_nurse_reg():
    conn = connect_db()
    if request.method == 'GET':
        return render_template('Reg_nurse.html', data=conn)

    if request.method == 'POST':
        nssn = request.form.get('nssn')
        nid = request.form.get('nid')
        fname = request.form.get('fname')
        mname = request.form.get('mname')
        lname = request.form.get('lname')
        dateofbirth = request.form.get('dateofbirth')
        sex = request.form.get('sex')
        address = request.form.get('address')
        mobileNumber = request.form.get('mobileNumber')
        age = request.form.get('age')
        department = request.form.get('department')
        email = request.form.get('email')

        password = request.form.get('password')

        try:

            cur = conn.cursor()
            cur.execute(
                'INSERT INTO nurse(nssn, nid, fname, mname, lname, dateofbirth, sex, address, mobileNumber, age, department, email, password) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (
                    nssn, nid, fname, mname, lname, dateofbirth, sex, address, mobileNumber, age, department, email
                      , password
                )
            )
            conn.commit()
            return render_template('Reg_nurse.html', message="nurse registered successfully!")  # Success message
        except psycopg2.errors.CheckViolation as e:
            print(f"Error: {e}")
            return render_template('Reg_nurse.html', error_message="Check Violation: Please review the entered data for any constraints.")
        except Exception as e:
            print(f"Error registering doctor: {e}")
            return render_template('Reg_nurse.html', error_message="An error occurred while registering the nurse.")
        finally:
            conn.close()

########################################################################################################################
########################################################################################################################

@app.route('/submit_reception_reg', methods=['GET', 'POST'])
def submit_reception_reg():
    conn = connect_db()
    if request.method == 'GET':
        return render_template('Reg_reciption.html', data=conn)

    if request.method == 'POST':
        rssn = request.form.get('rssn')
        rid = request.form.get('rid')
        fname = request.form.get('fname')
        mname = request.form.get('mname')
        lname = request.form.get('lname')
        dateofbirth = request.form.get('dateofbirth')
        sex = request.form.get('sex')
        address = request.form.get('address')
        mobileNumber = request.form.get('mobileNumber')

        email = request.form.get('email')
        password = request.form.get('password')

        try:

            cur = conn.cursor()
            cur.execute(
                'INSERT INTO receptionist(rssn, rid, fname, mname, lname, dateofbirth, sex, address, mobileNumber, email, password) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (
                    rssn, rid, fname, mname, lname, dateofbirth, sex, address, mobileNumber,  email
                      , password
                )
            )
            conn.commit()
            return render_template('Reg_reciption.html', message="nurse registered successfully!")  # Success message
        except psycopg2.errors.CheckViolation as e:
            print(f"Error: {e}")
            return render_template('Reg_reciption.html', error_message="Check Violation: Please review the entered data for any constraints.")
        except Exception as e:
            print(f"Error registering doctor: {e}")
            return render_template('Reg_reciption.html', error_message="An error occurred while registering the nurse.")
        finally:
            conn.close()

########################################################################################################################
########################################################################################################################

@app.route('/patients_without_doctors')
def patients_without_doctors():
    try:
        conn = connect_db()
        if conn is None:
            return "Error connecting to database.", 500

        cur = conn.cursor()
        cur.execute("""SELECT p.PSSN, p.pid, p.fname, p.lname 
                       FROM patient p 
                       LEFT JOIN treat t ON p.PSSN = t.patientssn
                       WHERE t.doctorssn IS NULL""")
        data = cur.fetchall()
        conn.close()

        data_remp = []
        for row in data:
            data_remp.append({'pssn': row[0], 'pid': row[1], 'fname': row[2], 'lname': row[3]})

        return render_template('rempatient.html', data=data_remp)

    except (Exception, psycopg2.Error) as e:
        print(f"Error fetching patients: {e}")
        return "An error occurred while fetchingpatients.",500

##########################
@app.route('/assign_doctor', methods=['POST'])
def assign_doctor():
    patient_ssn = request.form.get('patientssn')
    doctor_ssn = request.form.get('doctorssn')

    if not patient_ssn or not doctor_ssn:
        return "Patient SSN and Doctor SSN are required.", 400

    try:
        conn = connect_db()
        if conn is None:
            return "Error connecting to database.", 500

        cur = conn.cursor()
        cur.execute("INSERT INTO treat (patientssn, doctorssn) VALUES (%s, %s)", (patient_ssn, doctor_ssn))
        conn.commit()
        conn.close()

        return redirect('/patients_without_doctors')

    except (Exception, psycopg2.Error) as e:
        print(f"Error inserting into treat table: {e}")
        return "An error occurred while assigning the doctor.", 500

############################################################################################################
############################################################################################################



@app.route('/view_patient_records')
def view_patient_records():
    patient_id = request.args.get('pid')

    if not patient_id:
        return "Missing patient ID.", 400

    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=DictCursor)

        # Fetch records for the patient
        cursor.execute("""
            SELECT *
            FROM Patient_Record
            WHERE patient_id = %s
        """, (patient_id,))
        records = cursor.fetchall()

        # Fetch patient name
        cursor.execute("""
            SELECT fname, lname
            FROM patient
            WHERE pid = %s
        """, (patient_id,))
        patient = cursor.fetchone()

        patient_name = "Unknown"
        if patient and 'fname' in patient and 'lname' in patient:
            patient_name = f"{patient['fname']} {patient['lname']}"

        return render_template('PatientRecords.html', records=records, patient_name=patient_name)

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while fetching patient records.", 500

    finally:
        if conn:
            conn.close()


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('admin_login.html')



if __name__ == '__main__':
    app.run(debug=True)


###########################

if __name__ == '__main__':
    app.run(debug=True)
