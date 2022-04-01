# A mini app to connect to and store data on a cloud based instance of PostgreSQL 
# Works by being associated with a Heroku app that has the database 

from tkinter import *
import psycopg2
import os
from dotenv import load_dotenv
import subprocess



    
root = Tk()
root.title('Postgres Cloud App')
root.geometry("500x550")

def get_env_var():
    # remove current database url variable from the dictionary of environment variables
    try:
        del os.environ['DATABASE_URL']
    except KeyError:
        pass
    
    # Run bash script with shell
    subprocess.call("get_env.sh", shell=True)
    # Load environment variable into os.environ dictionary
    load_dotenv()
    '''
    for i, j in os.environ.items():
        print(i, j)
    '''
def query():
    # Assign database url environment variable to database_url
    DATABASE_URL = os.environ['DATABASE_URL']
    # Configure and connect to Postgres
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # Create a cursor
    c = conn.cursor()

    # Create a table
    c.execute('''CREATE TABLE IF NOT EXISTS customers
        (first_name TEXT,
         last_name TEXT);
         ''')
    conn.commit()
    conn.close()


def submit():
    first_name = f_name.get()
    last_name = l_name.get()

    DATABASE_URL = os.environ['DATABASE_URL']
    # Configure and connect to Postgres
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # Create a cursor
    c = conn.cursor()

    # Insert data into table
    c.execute("INSERT INTO customers VALUES (%s, %s)", (first_name, last_name))
    conn.commit()
    conn.close()
    
    # Update app with new records from database
    update()

def update():
    DATABASE_URL = os.environ['DATABASE_URL']
    # Configure and connect to Postgres
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # Create a cursor
    c = conn.cursor()

    # Grab stuff from database
    c.execute("SELECT * FROM customers")
    records = c.fetchall()
    output = ""

    for record in records:
        output_label.config(text=f"{output}\n{record[0]} {record[1]}")
        output = output_label['text']
    conn.commit()
    conn.close()


# Create the GUI for the app
my_frame = LabelFrame(root, text="Postgres Example")
my_frame.pack(pady=20)

f_label = Label(my_frame, text="First Name:")
f_label.grid(row=0, column=0, pady=10)

f_name = Entry(my_frame, font=("Helvetica, 18"))
f_name.grid(row=0, column=1, pady=10, padx=10)

l_label = Label(my_frame, text="Last Name:")
l_label.grid(row=1, column=0, pady=10, padx=10)

l_name = Entry(my_frame, font=("Helvetica, 18"))
l_name.grid(row=1, column=1, pady=10, padx=10)

submit_button = Button(my_frame, text="Submit",  command=submit)
submit_button.grid(row=2, column=0, pady=10, padx=10)

update_button = Button(my_frame, text="Update", command=update)
update_button.grid(row=2, column=1, pady=10, padx=10)

output_label = Label(root, text="")
output_label.pack(pady=50)

get_env_var()
query()
root.mainloop()