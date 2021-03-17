# Advance_Python_assignment
Advance Python Assignment

**WorkfLow of the App:**

1- Launch the app using Docker, under Advance_python_assignment - build docker image and run image. (No docker compose file because only one docker image needed)
    Build - docker build -t <image_name>:latest .
    Run - docker run -d -p 5000:5000 <image_name>
   
2- Launch the host, user will land on Home page with option to switch to Home, About, Employee Registration, Employee Login, Admin Login using Navbar at the top.

3- Register a new user input the details, user if successfully registered will land on Login Page.

4- Upon Loging in the user can see and update his/her details.

5- To register a new admin there should be an existing employee corresponding to the admin which can be promoted to admin using the terminal with code as below
    from flaskassignment import db
    from flaskassignment.models import Employee
    employee = Employee.query.filter_by(email=<email_id>).first()
    employee.is_admin = True
    db.session.add(employe)
    db.session.commit()
    One of the admin credentials are email - admin@admin.com password - admin123
    
6- Login with the admin under Admin login (Note: now you cannot use admin login credentials to login into employee interface) which will land you on Admin home and you can      see list of employees with their Name and email-id and upon selecting a particular employee you can edit or delete him/her. You can also add new employee and search as        well. Under Profile tab you can edit the current admin profile details.



**Functionalities Achieved :**

1 - Responsive pages irrespective of the Device Screen Resolution.

2 - Two roles (Admin, Employee) with appropriate permission Handling.

3 - Registration of any new Employee can be done using mandatory fields like (First name, Email, Phone Number, DOB and Address) and one optional field (Last Name). Validators
    are doing there work validating 
      i - First Name - Required, length b/w 2 - 20
      ii - Last Name - length b/w 2 - 20
      iii - Email - Required, Email Field, Unique 
      iv - Password - Required, length b/w 6 - 20
      v - Confirm Password - Required, Equal to Password
      vi - Phone Number - Required, Length equal to 10, Unique
      vii - Date Of Birth - Required, Year-Month-Date format, Age above 18
      viii - Address - Required
    All these field are used to Register a new employee by himself or Admin when he/she is logged in using his/her credentials.
    
4 - Login feature for different roles(Admin, Employee) when prompted to login, cross-checked with credentials saved in database. Neither Admin can use his/her credentials to     login in Employee interface nor Employee can use his/her credentials to Login in Admin Interface.
    
5 - After Loging in Employee can see only his/her detalils and update only his/her details and the allowed one in this version allowed updates are Name, Phone No, DOB, Address.

6 - After Loging in Admin can see List of all employees with details (Name and Email) do every operations on Employees like 
      i - Update Employees (in this version allowed updates are Name, Phone No, DOB, Address), 
      ii - Delete Employees (Delete any selected Employee from the database),
      iii - Search Employees (For Search we are using one field if input value matches First Name, Last Name or address the details are displayed as a list.Search done using             RESTful API registered at 'http://127.0.0.1:5000/api/search_result' which is secured using Json Web Token and data transfer done using json objects)
     He/She can also Update his/her details which corresponds to above mentioned criteria.
     
7 - Any URL can not be accessed by any unauthorized user ensuring security and permission handling.

8 - Blueprint used for Admin, Employee, Api and landing page to ensure scalabilty.

9 - Logging of user process is done along with default logger.
     
10 - Dockerfile and requirements.txt To create and image and launch a container.


**FUTURE SCOPE**

 1 - Updating the Home and About Pages with required details.

 2 - Upgrade Employees Right.
 
 3 - Increase data input at time of Registration like Profile Picture, Authentic details given by institute (can be cross-checked with database).
 
 4 - Allocating the Employee and admin a UID(world-wide) similar to our Nagarro ID's 
 
 5 - Updgrading access to update password, advancing the search field criteria using more specific data's.
 
 6 - In case User forgets Password, a Password Reset method can be opted.
 
 7 - Updating the Front-end for web app to look more interactive and user friendly.
 
