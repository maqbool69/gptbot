import tkinter as tk
from tkinter import filedialog
import pandas as pd
import time

# Function to start monitoring the CSV file
def start_monitoring():
    global previous_values
    global countdown
    
    # Get the selected file path
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path, delimiter='\t')
        
        # Initialize the previous values dictionary
        previous_values = {}
        
        # Function to update the countdown label
        def update_countdown():
            global countdown
            countdown -= 1
            countdown_label.config(text=f"Time Remaining: {countdown} seconds")
            if countdown > 0:
                countdown_label.after(1000, update_countdown)
            else:
                # Start monitoring the file
                for index, row in df.iterrows():
                    symbol = row['L']
                    current_value = row['L']
                    
                    if symbol in previous_values:
                        if current_value > previous_values[symbol]:
                            df.at[index, 'Q'] += 1
                            previous_values[symbol] = current_value
                    else:
                        previous_values[symbol] = current_value
                
                # Save the updated DataFrame back to the CSV file
                df.to_csv(file_path, sep='\t', index=False)
                countdown_label.config(text="Monitoring Complete")
        
        # Start the countdown timer
        countdown = 60  # 60 seconds
        update_countdown()

# Create the main window
root = tk.Tk()
root.title("Excel Checker")

# Configure dark theme
root.tk_setPalette(background='#333', foreground='#fff')

# Create and configure the browse button
browse_button = tk.Button(root, text="Browse File", command=start_monitoring)
browse_button.pack(pady=20)

# Create a label for the countdown timer
countdown_label = tk.Label(root, text="", font=("Helvetica", 14), fg="#fff", bg="#333")
countdown_label.pack()

# Start the main loop
root.mainloop()
