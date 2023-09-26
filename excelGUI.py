import pandas as pd
import time
import tkinter as tk
from tkinter import filedialog

# Function to run the main program
def run_program():
    global file_path, previous_values
    
    # Read the selected CSV file into a DataFrame
    file_path = file_path_var.get()
    df = pd.read_excel(file_path)  # Assuming it's a CSV file, change as needed
    
    # Create a dictionary to store the previous values of each cell in the "High" column
    previous_values = {cell_index: value for cell_index, value in enumerate(df['High'])}
    

    while True:
        # Read the Excel file again into a DataFrame
        df = pd.read_excel(file_path)

        # Select the 'High' and 'Max' columns from the DataFrame
        high_column = df['High']
        max_column = df['Maximum_High']
        trading_symbol_column = df['Trading Symbol']


        # Compare each cell's value with its previous value
        for cell_index, current_value in enumerate(high_column):
            previous_value = previous_values.get(cell_index)
            
            if previous_value is not None and current_value > previous_value:
                # Increment the corresponding 'Max' column value by 1
                max_column.at[cell_index] += 1
                print(f"Row {cell_index + 2}: Incremented 'Max' column value to {max_column.at[cell_index]}")
                print(f"Trading Symbol: {trading_symbol_column.at[cell_index]}")


            # Update the previous value for this cell
            previous_values[cell_index] = current_value

        # Save the updated DataFrame back to the Excel file in xlsx format
        df.to_excel(file_path, index=False, engine='xlsxwriter')

        # Wait for 5 seconds before checking again
        time.sleep(15)


# Function to open a file dialog and update the file path variable
def browse_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.xls")])  # You can change the file types
    
    # Update the entry widget with the selected file path
    file_path_var.set(file_path)

# Create the main window
root = tk.Tk()
root.title("CSV File Processor")

# Create a variable to store the selected file path
file_path_var = tk.StringVar()

# Create a label and entry widget to display and select the file path
file_label = tk.Label(root, text="Select CSV File:")
file_label.pack()
file_entry = tk.Entry(root, textvariable=file_path_var, width=50)
file_entry.pack()
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

# Create a button to start the program
start_button = tk.Button(root, text="Start", command=run_program)
start_button.pack()

# Start the Tkinter main loop
root.mainloop()
