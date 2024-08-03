import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

# Create a connection to the SQLite database and obtain a cursor
conn = sqlite3.connect('Data_acquisition.db')
cursor = conn.cursor()

# Create the 'users' table if it does not already exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY,
                  The_appearance_is_not_bright_or_flat INTEGER,
                  Shadows INTEGER,
                  Scratches_or_peeling INTEGER,
                  Rust INTEGER,
                  Deformation INTEGER,
                  Incomplete_silk_screen_marking INTEGER,
                  Missing_accessories INTEGER,
                  Poor_rivet_columns_or_screw_holes INTEGER,
                  Extra_field INTEGER
                  )''')

# Create the main window of the GUI
root = tk.Tk()
root.title("Quality Control Acquisition")

# Create a notebook (tab container) to organize different functionalities
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Configure the grid to expand with the window size
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create frames for each tab in the notebook
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab5 = ttk.Frame(notebook)

# Add tabs to the notebook with respective titles
notebook.add(tab1, text="Read me first")
notebook.add(tab2, text="CREATE/ENTER new data")
notebook.add(tab3, text="READ ALL data")
notebook.add(tab4, text="UPDATE only data")
notebook.add(tab5, text="DELETE only last data")

# Function to submit new data to the database
def submit_data():
    extra_value = extra_entry.get()

    # Validate that the extra field contains exactly 8 digits
    if not extra_value.isdigit() or len(extra_value) != 8:
        messagebox.showwarning("Invalid Input", "Please enter exactly 8 digits.")
        return

    # Collect data from checkboxes and extra field
    data = {
        'The_appearance_is_not_bright_or_flat': check_var_1.get(),
        'Shadows': check_var_2.get(),
        'Scratches_or_peeling': check_var_3.get(),
        'Rust': check_var_4.get(),
        'Deformation': check_var_5.get(),
        'Incomplete_silk_screen_marking': check_var_6.get(),
        'Missing_accessories': check_var_7.get(),
        'Poor_rivet_columns_or_screw_holes': check_var_8.get(),
        'Extra_field': int(extra_value)
    }

    # Convert boolean values to integers (1 or 0)
    data = {k: int(v) for k, v in data.items()}

    # Insert the collected data into the 'users' table
    cursor.execute('''INSERT INTO users (
                      The_appearance_is_not_bright_or_flat,
                      Shadows,
                      Scratches_or_peeling,
                      Rust,
                      Deformation,
                      Incomplete_silk_screen_marking,
                      Missing_accessories,
                      Poor_rivet_columns_or_screw_holes,
                      Extra_field)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (data['The_appearance_is_not_bright_or_flat'],
                    data['Shadows'],
                    data['Scratches_or_peeling'],
                    data['Rust'],
                    data['Deformation'],
                    data['Incomplete_silk_screen_marking'],
                    data['Missing_accessories'],
                    data['Poor_rivet_columns_or_screw_holes'],
                    data['Extra_field']))

    # Commit the changes and clear the input fields
    conn.commit()
    check_var_1.set(False)
    check_var_2.set(False)
    check_var_3.set(False)
    check_var_4.set(False)
    check_var_5.set(False)
    check_var_6.set(False)
    check_var_7.set(False)
    check_var_8.set(False)
    extra_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Data submitted successfully!")

# Function to list all data from the 'users' table
def list_all_data():
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    # Define column widths for formatting
    column_widths = [3, 12, 10, 10, 5, 12, 10, 12, 8, 12]

    # Enable and clear the text widget
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)

    # Create and insert the header
    header = ("ID".ljust(column_widths[0]) + " | " +
              "Appearance".ljust(column_widths[1]) + " | " +
              "Shadows".ljust(column_widths[2]) + " | " +
              "Scratches".ljust(column_widths[3]) + " | " +
              "Rust".ljust(column_widths[4]) + " | " +
              "Deformation".ljust(column_widths[5]) + " | " +
              "Marking".ljust(column_widths[6]) + " | " +
              "Accessories".ljust(column_widths[7]) + " | " +
              "Rivets".ljust(column_widths[8]) + " | " +
              "Serial".ljust(column_widths[9]))
    text_widget.insert(tk.END, header + "\n")
    text_widget.insert(tk.END, "-" * len(header) + "\n")

    # Insert each row of data
    for row in rows:
        formatted_row = (str(row[0]).ljust(column_widths[0]) + " | " +
                         str(row[1]).ljust(column_widths[1]) + " | " +
                         str(row[2]).ljust(column_widths[2]) + " | " +
                         str(row[3]).ljust(column_widths[3]) + " | " +
                         str(row[4]).ljust(column_widths[4]) + " | " +
                         str(row[5]).ljust(column_widths[5]) + " | " +
                         str(row[6]).ljust(column_widths[6]) + " | " +
                         str(row[7]).ljust(column_widths[7]) + " | " +
                         str(row[8]).ljust(column_widths[8]) + " | " +
                         str(row[9]).ljust(column_widths[9]))
        text_widget.insert(tk.END, formatted_row + "\n")

    # Disable the text widget to prevent further editing
    text_widget.config(state=tk.DISABLED)

# Function to prepopulate the checkboxes and extra field with the last row's data
def prepopulate_checkbuttons():
    cursor.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()

    if row:
        # Set the state of each checkbox based on the last row's data
        check_var_update_1.set(bool(row[1]))
        check_var_update_2.set(bool(row[2]))
        check_var_update_3.set(bool(row[3]))
        check_var_update_4.set(bool(row[4]))
        check_var_update_5.set(bool(row[5]))
        check_var_update_6.set(bool(row[6]))
        check_var_update_7.set(bool(row[7]))
        check_var_update_8.set(bool(row[8]))
        extra_entry_update.delete(0, tk.END)
        extra_entry_update.insert(0, str(row[9]))

# Function to update the last row of data
def update_last_row():
    extra_value = extra_entry_update.get()

    # Validate the extra field
    if not extra_value.isdigit() or len(extra_value) != 8:
        messagebox.showwarning("Invalid Input", "Please enter exactly 8 digits.")
        return

    # Get the ID of the last row
    cursor.execute('SELECT id FROM users ORDER BY id DESC LIMIT 1')
    last_id = cursor.fetchone()

    if not last_id:
        messagebox.showwarning("Update Error", "No data available to update.")
        return

    last_id = last_id[0]

    # Collect updated data from checkboxes and extra field
    data = {
        'The_appearance_is_not_bright_or_flat': check_var_update_1.get(),
        'Shadows': check_var_update_2.get(),
        'Scratches_or_peeling': check_var_update_3.get(),
        'Rust': check_var_update_4.get(),
        'Deformation': check_var_update_5.get(),
        'Incomplete_silk_screen_marking': check_var_update_6.get(),
        'Missing_accessories': check_var_update_7.get(),
        'Poor_rivet_columns_or_screw_holes': check_var_update_8.get(),
        'Extra_field': int(extra_value)
    }

    # Convert boolean values to integers (1 or 0)
    data = {k: int(v) for k, v in data.items()}

    # Update the last row with the new data
    cursor.execute('''UPDATE users SET
                      The_appearance_is_not_bright_or_flat = ?,
                      Shadows = ?,
                      Scratches_or_peeling = ?,
                      Rust = ?,
                      Deformation = ?,
                      Incomplete_silk_screen_marking = ?,
                      Missing_accessories = ?,
                      Poor_rivet_columns_or_screw_holes = ?,
                      Extra_field = ?
                      WHERE id = ?''',
                   (data['The_appearance_is_not_bright_or_flat'],
                    data['Shadows'],
                    data['Scratches_or_peeling'],
                    data['Rust'],
                    data['Deformation'],
                    data['Incomplete_silk_screen_marking'],
                    data['Missing_accessories'],
                    data['Poor_rivet_columns_or_screw_holes'],
                    data['Extra_field'],
                    last_id))

    # Commit the changes and clear the input fields
    conn.commit()
    messagebox.showinfo("Success", "Data updated successfully!")

# Function to delete the last row of data
def delete_last_row():
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the last entry?"):
        cursor.execute('SELECT id FROM users ORDER BY id DESC LIMIT 1')
        last_id = cursor.fetchone()

        if not last_id:
            messagebox.showwarning("Delete Error", "No data available to delete.")
            return

        last_id = last_id[0]

        # Delete the row with the last ID
        cursor.execute('DELETE FROM users WHERE id = ?', (last_id,))
        conn.commit()
        messagebox.showinfo("Success", "Last data deleted successfully!")

# Tab 1: Read Me First
readme_label = ttk.Label(tab1, text="This is acquisition software for power inverter cosmetic damages classification.\nProcedure is simple.\nThe following are considered defective:\n1. The appearance is not bright/flat;\n2. Shadows;\n3. Scratches/peeling;\n4. Rust;\n5. Deformation;\n6. Incomplete silk screen marking;\n7. Missing accessories;\n8. Poor rivet columns/screw holes ")
readme_label.grid(row=0, column=0, padx=10, pady=10)

# Tab 2: Create/Enter New Data
label2 = ttk.Label(tab2, text="Please input the required fields and submit.")
label2.grid(row=0, column=0, padx=10, pady=5)

# Create BooleanVars for checkboxes to store boolean states (checked or unchecked)
check_var_1 = tk.BooleanVar()
check_var_2 = tk.BooleanVar()
check_var_3 = tk.BooleanVar()
check_var_4 = tk.BooleanVar()
check_var_5 = tk.BooleanVar()
check_var_6 = tk.BooleanVar()
check_var_7 = tk.BooleanVar()
check_var_8 = tk.BooleanVar()

# Create and place checkboxes for each defect
checkbox_1 = tk.Checkbutton(tab2, text="1. The appearance is not bright/flat;", variable=check_var_1)
checkbox_1.grid(row=1, column=0, padx=10, pady=5, sticky="w")
checkbox_2 = tk.Checkbutton(tab2, text="2. Shadows;", variable=check_var_2)
checkbox_2.grid(row=2, column=0, padx=10, pady=5, sticky="w")
checkbox_3 = tk.Checkbutton(tab2, text="3. Scratches/peeling;", variable=check_var_3)
checkbox_3.grid(row=3, column=0, padx=10, pady=5, sticky="w")
checkbox_4 = tk.Checkbutton(tab2, text="4. Rust;", variable=check_var_4)
checkbox_4.grid(row=4, column=0, padx=10, pady=5, sticky="w")
checkbox_5 = tk.Checkbutton(tab2, text="5. Deformation;", variable=check_var_5)
checkbox_5.grid(row=5, column=0, padx=10, pady=5, sticky="w")
checkbox_6 = tk.Checkbutton(tab2, text="6. Incomplete silk screen marking;", variable=check_var_6)
checkbox_6.grid(row=6, column=0, padx=10, pady=5, sticky="w")
checkbox_7 = tk.Checkbutton(tab2, text="7. Missing accessories;", variable=check_var_7)
checkbox_7.grid(row=7, column=0, padx=10, pady=5, sticky="w")
checkbox_8 = tk.Checkbutton(tab2, text="8. Poor rivet columns/screw holes;", variable=check_var_8)
checkbox_8.grid(row=8, column=0, padx=10, pady=5, sticky="w")

# Entry widget for extra field
extra_label = ttk.Label(tab2, text="Extra field (8 digits):")
extra_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
extra_entry = ttk.Entry(tab2)
extra_entry.grid(row=10, column=0, padx=10, pady=5, sticky="w")

# Submit button to submit data to the database
submit_button = ttk.Button(tab2, text="Submit", command=submit_data)
submit_button.grid(row=11, column=0, padx=10, pady=10)

# Tab 3: Read All Data
text_widget = tk.Text(tab3, wrap=tk.NONE, height=20, width=150)
text_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Button to list all data in the text widget
list_button = ttk.Button(tab3, text="List All Data", command=list_all_data)
list_button.grid(row=1, column=0, padx=10, pady=10)

# Tab 4: Update Only Data
prepopulate_checkbuttons_label = ttk.Label(tab4, text="Prepopulate the last row to update:")
prepopulate_checkbuttons_label.grid(row=0, column=0, padx=10, pady=5)

# Button to prepopulate checkboxes and entry with the last row's data
prepopulate_checkbuttons_button = ttk.Button(tab4, text="Prepopulate", command=prepopulate_checkbuttons)
prepopulate_checkbuttons_button.grid(row=1, column=0, padx=10, pady=5)

# Create BooleanVars for checkboxes used in updating data
check_var_update_1 = tk.BooleanVar()
check_var_update_2 = tk.BooleanVar()
check_var_update_3 = tk.BooleanVar()
check_var_update_4 = tk.BooleanVar()
check_var_update_5 = tk.BooleanVar()
check_var_update_6 = tk.BooleanVar()
check_var_update_7 = tk.BooleanVar()
check_var_update_8 = tk.BooleanVar()

# Create and place checkboxes for updating defects
checkbox_update_1 = tk.Checkbutton(tab4, text="1. The appearance is not bright/flat;", variable=check_var_update_1)
checkbox_update_1.grid(row=2, column=0, padx=10, pady=5, sticky="w")
checkbox_update_2 = tk.Checkbutton(tab4, text="2. Shadows;", variable=check_var_update_2)
checkbox_update_2.grid(row=3, column=0, padx=10, pady=5, sticky="w")
checkbox_update_3 = tk.Checkbutton(tab4, text="3. Scratches/peeling;", variable=check_var_update_3)
checkbox_update_3.grid(row=4, column=0, padx=10, pady=5, sticky="w")
checkbox_update_4 = tk.Checkbutton(tab4, text="4. Rust;", variable=check_var_update_4)
checkbox_update_4.grid(row=5, column=0, padx=10, pady=5, sticky="w")
checkbox_update_5 = tk.Checkbutton(tab4, text="5. Deformation;", variable=check_var_update_5)
checkbox_update_5.grid(row=6, column=0, padx=10, pady=5, sticky="w")
checkbox_update_6 = tk.Checkbutton(tab4, text="6. Incomplete silk screen marking;", variable=check_var_update_6)
checkbox_update_6.grid(row=7, column=0, padx=10, pady=5, sticky="w")
checkbox_update_7 = tk.Checkbutton(tab4, text="7. Missing accessories;", variable=check_var_update_7)
checkbox_update_7.grid(row=8, column=0, padx=10, pady=5, sticky="w")
checkbox_update_8 = tk.Checkbutton(tab4, text="8. Poor rivet columns/screw holes;", variable=check_var_update_8)
checkbox_update_8.grid(row=9, column=0, padx=10, pady=5, sticky="w")

# Entry widget for extra field used in updating
extra_label_update = ttk.Label(tab4, text="Extra field (8 digits):")
extra_label_update.grid(row=10, column=0, padx=10, pady=5, sticky="w")
extra_entry_update = ttk.Entry(tab4)
extra_entry_update.grid(row=11, column=0, padx=10, pady=5, sticky="w")

# Button to update the last row of data
update_button = ttk.Button(tab4, text="Update Last Data", command=update_last_row)
update_button.grid(row=12, column=0, padx=10, pady=10)

# Tab 5: Delete Only Last Data
# Button to delete the last row of data
delete_button = ttk.Button(tab5, text="Delete Last Data", command=delete_last_row)
delete_button.grid(row=0, column=0, padx=10, pady=10)

# Start the main event loop to run the GUI
root.mainloop()
