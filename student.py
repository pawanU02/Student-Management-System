import mysql.connector
import streamlit as st
import pandas as pd
import configparser

# '''
# Establish the connection to mysql server
# '''

config = configparser.ConfigParser()
config.read('config.ini')
host = config['database']['host']
user = config['database']['user']
password = config['database']['password']
database = config['database']['database']

mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Crete a cursor
mycursor = mydb.cursor()
print("Connection Established")


def main():
    st.title("Student Management System")
    
    # Display options for CRUD operations
    option = st.sidebar.selectbox("Select an Opearton", ("Reset ID", "Create", "Read", "Update", "Delete", "Delete All"))

    # calculate the gpa
    def calculate_gpa(marks):
        percentage = (marks / 500) * 100
        gpa = (percentage / 100) * 4.0
        return gpa
        
    def get_grade(marks):
        percentage = (marks / 500) * 100

        if percentage >= 90:
            return "A+"
        elif percentage >= 85:
            return "A"
        elif percentage >= 80:
            return "A-"
        elif percentage >= 75:
            return "B+"
        elif percentage >= 70:
            return "B"
        elif percentage >= 65:
            return "B-"
        elif percentage >= 60:
            return "C+"
        elif percentage >= 55:
            return "C"
        elif percentage >= 50:
            return "C-"
        elif percentage >= 45:
            return "D+"
        elif percentage >= 40:
            return "D"
        else:
            return "F"
 
    # Perform selected operation
    if option == "Create":
        st.subheader("Create a Record of Student")
        first_name = st.text_input("Enter first name of Student")
        last_name = st.text_input("Enter last name of Student")
        email = st.text_input("Enter email of Student")
        marks = st.number_input("Enter marks of Student", min_value=0)
        # grade = st.text_input("Enter grade of Student")
        
        gpa = calculate_gpa(marks)
        grade = get_grade(marks)
        
        # Insert values when create button is clicked
        if st.button("Create"):
            sql = "insert into students(first_name, last_name, email, marks, grade, gpa) values(%s, %s, %s, %s, %s, %s)"
            val = (first_name, last_name, email, marks, grade, gpa)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Created Successfully!!!!!")
    
    # reset auto-increment of ID
    elif option == "Reset ID":
        if st.button("Reset ID"):
            mycursor.execute("ALTER TABLE students AUTO_INCREMENT = 1")
            mydb.commit()
            st.success("ID Reset Successfully!!!!!")
    
    # read the records    
    elif option == "Read":
        st.subheader("Read a Record")
        if st.button("Read"):
            mycursor.execute("SELECT * FROM students")
            result = mycursor.fetchall()
            
            # Convert the result into a list of lists
            data = [list(row) for row in result]
            
            # Create a DataFrame from the data
            df = pd.DataFrame(data, columns=["ID", "First Name", "Last Name", "Email", "Marks", "Grade", "gpa"])
            
            # Display the DataFrame as a table
            st.table(df)
                
    
    # Update the records           
    elif  option == "Update":
        st.subheader("Update a Record")
        id = st.number_input("Enter ID", min_value=1)
        first_name = st.text_input("Enter first name of Student")
        last_name = st.text_input("Enter last name of Student")
        email = st.text_input("Enter email of Student")
        marks = st.number_input("Enter marks of Student", min_value=0)
        
        if st.button("Update"):
            
            gpa = calculate_gpa(marks)
            grade = get_grade(marks)
            
            sql = "update students set first_name=%s, last_name= %s, email= %s, marks= %s, grade= %s, gpa= %s where id = %s"
            val = (first_name, last_name, email, marks, grade, gpa, id)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Updated Successfully!!!!!")
            
    
    # Delete single record using ID    
    elif option == "Delete":
        st.subheader("Delete a Record")
        id = st.number_input("Enter ID", min_value=1)
        if st.button("Delete"):
            sql = "delete from students where id=%s"
            val = (id,)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Deleted Successfully!!!!!")
    
    
    # Delet All Records
    else:
        st.subheader("Delete All Records")
        
        # Confirmation
        confirmation = st.checkbox("I confirm that I want to delete all records")

        # Check if the confirmation checkbox is checked and the button is clicked
        if confirmation and st.button("Clear all records"):
            sql = 'DELETE FROM students'
            mycursor.execute(sql)
            mydb.commit()
            st.warning('All records have been deleted')
    

if __name__ == "__main__":
    main()
