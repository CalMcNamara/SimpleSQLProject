# Simple Kitchen Item Datebase program - Cal McNamara 
# 1.0V
# Currently The app 
#
#
#

import sqlite3
from sqlite3 import Error
from tkinter import *
import tkinter as tk  

item_location = " "
item_name = " "
item_dategot = " "
item_date_expired = " "
all_items_list = []

def create_connection(db_file):
  # par db_file , The name of the db in which is being connected to. 
  # creates the connection to the db. 
  conn = None
  try:
    conn = sqlite3.connect(db_file)
    return conn
  except Error as e:
    print(e)
  return conn

def create_table(conn, create_table_sql):
  # par conn, create_table_sql
  # Needs a valid connection and a valid SQL statment to execute the creation of a table within the db
  try:
      c = conn.cursor()
      c.execute(create_table_sql)
  except Error as e:
        print(e)

def create_inventory(conn, inventory):
  # par conn, inventory : requires a valid conn and inventory items. 
  # Uses the inventory par to insert into the Values(?,?,?,?
  # )
  sql = '''INSERT or IGNORE INTO inventory(name,location,begin_date,end_date)
  Values(?,?,?,?)  '''

  cur = conn.cursor()
  cur.execute(sql,inventory)
  return cur.lastrowid

def get_items(conn):
  # par conn : requires a valid conn
  # Selects all from inventory and prints it to the console. 
  cur = conn.cursor()
  with conn:
    cur.execute("SELECT * FROM inventory")
    print(cur.fetchall())

def get_kitchen_items(conn):
  # par conn : requires a valid conn
  # Selects all from kitchen and prints it to the console. 
  cur = conn.cursor()
  with conn:
    cur.execute("SELECT * from inventory where location = 'Kitchen'")
    print(cur.fetchall())


def get_fridge_items(conn):
  # par conn : requires a valid conn
  # Selects all from fridge and prints it to the console.
  cur = conn.cursor()
  with conn:
    cur.execute("SELECT * from inventory where location = 'Fridge'")
    print(cur.fetchall())

def get_pantry_items(conn):
  # par conn : requires a valid conn
  # Selects all from fridge and prints it to the console. 
  cur = conn.cursor()
  with conn:
    cur.execute("SELECT * from inventory where location = 'Pantry'")
    pantry_item_list = cur.fetchall()
    print(pantry_item_list)



def main():
  #db name can be changed to have a new db. 
  database = "inventory.db"
  sql_create_inventory_table = """ CREATE TABLE IF NOT EXISTS inventory (
                                        name text PRIMARY KEY,
                                        location text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """
    
    # create a database connection
  conn = create_connection(database)
    # create tables
  if conn is not None:
    # create projects table
      create_table(conn, sql_create_inventory_table,)
  else:
      print("Error! cannot create the database connection.")
  window = tk.Tk()

  def fetch_inputs():
    # par : None
    # gets all items from the boxes and sets them to variables. 
    global item_location
    global item_name
    global item_dategot
    global item_date_expired
    
    item_location = v.get()
    if(item_location == 1):
      item_location = "Freezer"
    if(item_location == 2):
      item_location = "Fridge"
    if(item_location == 3):
      item_location = "Kitchen"
    if(item_location == 4):
      item_location = "Pantry"
    item_name = name_entry.get()
    item_dategot = bdate_entry.get()
    item_date_expired = expdate_entry.get()

    print(item_location, item_name, item_dategot,item_date_expired)
    return(item_location, item_name, item_dategot,item_date_expired)
  
  
  
  def add_values():
    # par : None
    inventory = [item_name,item_location,item_dategot,item_date_expired]
    
    if(item_name != " " or item_location != " " or item_date_expired != " " or item_dategot != " "):
    
      create_inventory(conn, inventory)
    else:
      print("Please Ensure that there are values in each slot.")
  

  def load_items():
    # par : None
    # Fetchs all inputs put puts them on the screen in a listbox does the same thing as get_items()
    # This is where the creation of the delete button and the detele method can be found. 
    cur = conn.cursor()
    
    with conn:
      cur.execute("SELECT * FROM inventory")
      global all_items_list
      all_items_list = cur.fetchall()
      #List Box creation 
      loaded_item_lb = Listbox(window)
      loaded_item_lb.configure(width = 80, height = 30)

      i = 0
      for item in all_items_list:
        loaded_item_lb.insert(i,item) 
        i += 1
      #List box placement 
      loaded_item_lb.grid(column = 3, row = 15)
      
      #delete button creation and placement 
      del_button = Button(window, text = "Delete", command  = lambda: delete_from_db()) 
      del_button.grid(column = 3, row = 16)
      
      def delete_from_db():
        # par : None
        # takes the selected item from the list box and deletes that item from the db
        # it uses the name and that data that it expires to ensure unique item gets deleted from the db. 
        item = loaded_item_lb.get(tk.ACTIVE) 
        print(loaded_item_lb.get(tk.ACTIVE))
        print(item[0])
          #name,location,begin_date,end_date 
        cur = conn.cursor()
        #sql statement to delete the items from the db using the par : name , end_date.  
        sql = ('''DELETE FROM inventory WHERE name = ? and end_date = ?''')
        cur.execute(sql,(item[0],item[3]))
        load_items()
  
    
      
    
    
    
  
  
  #getting kitchen item button
  kitchenfetch_button = tk.Button(window,text = "Click me to load Kitchen Items.",command = lambda:get_kitchen_items(conn))
  kitchenfetch_button.grid(column = 0, row = 1)
    
  #getting fridge item button
  fridgefetch_button = tk.Button(window, text = "Click me to load Fridge Items", command = lambda:get_fridge_items(conn))
  fridgefetch_button.grid(column = 0, row = 0)

  #getting Pantry Items butoon
  pantryfetch_button = tk.Button(window, text = "Click me to load Pantry Items", command = lambda:get_pantry_items(conn))
  pantryfetch_button.grid(column = 0, row = 2)

  #item name label 
  item_label = tk.Label(text='Enter Name of Item')
  item_label.grid(column = 2, row = 0)

  #label Name creation 
  name_entry = Entry()
  name_entry.grid(column = 2, row = 1)

  #Label for bought date.
  bdate_label = tk.Label(text='Date you bought the item')
  bdate_label.grid(column = 3, row = 0)

  #entry for bought date
  bdate_entry = Entry()
  bdate_entry.grid(column = 3, row = 1)

  #Label for expired date
  expdate_label = tk.Label(text = 'Date the item expires')
  expdate_label.grid(column = 4, row = 0)

  #Entry for expirdate
  expdate_entry = Entry()
  expdate_entry.grid(column = 4, row = 1)
  
  #col 5 
  v = IntVar()

  button_Freezer = Radiobutton(text = "Freezer", variable = v, value = 1)
  button_Freezer.grid(column = 5, row = 1)

  button_Fridge = Radiobutton(text = "Fridge", variable = v, value = 2)
  button_Fridge.grid(column = 5, row = 2)

  button_Kitchen = Radiobutton(text = "Kitchen", variable = v, value = 3)
  button_Kitchen.grid(column = 5, row = 3)

  button_Pantry = Radiobutton(text = "Pantry" , variable = v, value = 4)
  button_Pantry.grid(column = 5, row = 4)

  #submit button
  submit_button = tk.Button(text = 'Submit',command = lambda: fetch_inputs())
  submit_button.grid(column = 6, row = 1)

  #add to db button
  value_print_button = tk.Button(text = 'Add values to db.',command = lambda: add_values())
  value_print_button.grid(column = 6, row = 2)

  #load all items on screen button
  load_button = tk.Button(text = " Load items ", command = lambda: load_items())
  load_button.grid( column = 3, row = 7)
  
  with conn:
    
    
    get_items(conn)
    window.mainloop()


if __name__ == '__main__':
    main()