import pandas as pd
import time

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'max.xls'

# Read the Excel file into a DataFrame
df = pd.read_excel(file_path)

# Create a dictionary to store the previous values of each cell in the "High" column
previous_values = {cell_index: value for cell_index, value in enumerate(df['High'])}

while True:
    # Read the Excel file again into a DataFrame
    df = pd.read_excel(file_path)

    # Select the 'High' and 'Max' columns from the DataFrame
    high_column = df['High']
    max_column = df['Max']
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
