import pandas as pd
import os
import glob
from datetime import datetime

def process_folder_csvs(folder_path):
    """
    Find all CSV files in a folder and create an Excel file with multiple tabs
    
    Parameters:
    folder_path (str): Path to the folder containing CSV files
    """
    
    # Ensure folder path exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        return
    
    # Find all CSV files in the folder
    csv_pattern = os.path.join(folder_path, "*.csv")
    csv_files = glob.glob(csv_pattern)
    
    if len(csv_files) == 0:
        print(f"No CSV files found in folder: {folder_path}")
        return
    
    # Sort files for consistent ordering
    csv_files.sort()
    
    print(f"Found {len(csv_files)} CSV files:")
    for f in csv_files:
        print(f"  - {os.path.basename(f)}")
    
    # If more than 3 files, take first 3
    if len(csv_files) > 3:
        print(f"\nUsing first 3 CSV files (found {len(csv_files)} total)")
        csv_files = csv_files[:3]
    
    # Generate Excel filename with timestamp
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y%m%d-%H%M%S")
    excel_filename = f"test-data-load-{timestamp}.xlsx"
    
    # Ensure Excel file is saved in the same directory
    excel_path = os.path.join(folder_path, excel_filename)
    
    # Create Excel writer object
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        
        for i, csv_file in enumerate(csv_files):
            try:
                # Read CSV file
                df = pd.read_csv(csv_file)
                
                # Add sequence number as first column
                df.insert(0, 'seqno', range(1, len(df) + 1))
                
                # Add timestamp columns
                current_time = datetime.now()
                timestamp = current_time.strftime("%Y-%m-%d %I:%M%p")
                df['create_ts'] = timestamp
                df['updt_ts'] = timestamp
                
                # Use filename without extension as sheet name
                sheet_name = os.path.splitext(os.path.basename(csv_file))[0]
                
                # Ensure sheet name is valid (Excel has 31 character limit)
                sheet_name = sheet_name[:31]
                
                # Write dataframe to Excel sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                print(f"Successfully added '{os.path.basename(csv_file)}' to sheet '{sheet_name}' with {len(df)} rows and timestamp: {timestamp}")
                
            except FileNotFoundError:
                print(f"Error: File '{csv_file}' not found")
            except pd.errors.EmptyDataError:
                print(f"Error: File '{csv_file}' is empty")
            except Exception as e:
                print(f"Error processing '{csv_file}': {str(e)}")
    
    print(f"Excel file created at: {excel_path}")

# Example usage
if __name__ == "__main__":
    # Specify the folder path containing your CSV files
    folder_path = input("Enter the folder path containing CSV files: ").strip()
    
    # Process the folder
    process_folder_csvs(folder_path)
