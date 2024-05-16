import os
import pandas as pd
import pickle
import glob
import requests
import json
from tqdm import tqdm
import shutil
import zipfile
import random
from collections import Counter
import gspread
from google.auth import exceptions
import pyarrow.parquet as pq
from datetime import datetime
import hashlib
import ast

####################################################################################################
# FILE LOADERS
####################################################################################################

def load_file(path, delimiter = ";", decimal ="."):
    extension = os.path.splitext(os.path.basename(path))[1]
    if extension == ".parquet":
        df = load_parquet(path)
    elif extension == ".pickle":
        df = load_pickle(path)
    elif extension == ".json":
        df = load_json(path)
    elif extension == ".jsonl":
        df = load_jsonl(path)
    elif extension == ".csv":
        df = load_csv(path, delimiter = delimiter, decimal =decimal)
    elif extension == ".tsv":
        df = load_csv(path, delimiter = "\t", decimal =decimal)
    else :
        print("Check your input file. Extension isn't supported : .parquet, .pickle, .json, .jsonl, .csv, .tsv")
    return df

def load_parquet(path): 
    """
    Load a parquet file into a DataFrame
    """
    try:
        table = pq.read_table(path)
        df = table.to_pandas()
    except Exception as e:
        pass
        print(e)
    return df

# def load_pickle(path: str):
#     """
#     Load a pickle file into a dataframe
#     """
    
#     with open(path, 'rb') as f:
#         df=pickle.load(f)
#     return df
def load_pickle(path):
    return pd.read_pickle(path)

def write_pickle(data, path, filename):
    """
    Write a dataframe into a pickle file
    """
    file_path=os.path.join(path, filename+'.pickle')
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
    return file_path


def load_json(path: str):
    """
    Load a json file into a DataFrame
    """
    df=pd.DataFrame()
    try:
        with open(path, 'r') as json_file:
            data = json.load(json_file)
        df=pd.json_normalize(data)
        
    except Exception as e:
        pass
        print(e)
    return df

def load_jsonl(path: str):
    """
    Load a jsonl file into a dataframe
    """
    df = pd.DataFrame()
    try:
        data = []
        with open(path, 'r') as json_file:
            for line in tqdm(json_file):
                try:
                    data.append(json.loads(line))
                except:
                    pass
            
        df = pd.json_normalize(data)
    except Exception as e:
        pass
        print(e)
    return df


def load_csv(path: str, delimiter: str =";", decimal:str ="."):
    """
    Load a csv file into a dataframe 
    """
    df= pd.DataFrame()
    try:
        df = pd.read_csv(path, delimiter=delimiter, encoding="utf-8", decimal=decimal)
    except Exception as e:
        pass
        print(e)
    return df

def read_txt_to_list(file_path: str):
    """
    Read a text file line by line and append to a Python list 
    """
    
    # Initialize an empty list to store the lines
    lines = []

    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read each line and append it to the list
            lines = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return lines


def read_json(path: str):
    """
    Read a json file and return a dict
    """
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def read_txt_file(file_path: str) -> str:
    """
    Read a text file
    """
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def read_jsonl(path: str):
    """
    Load a jsonl file into a dataframe
    """
    json_data = []
    with open(path, 'r') as json_file:
        for line in tqdm(json_file):
            try:
                json_data.append(json.loads(line))
            except Exception as e:
                pass
                print(e)
        
    return json_data


#########################################################################################
# FILE WRITERS
#########################################################################################


# def write_pickle(df: pd.DataFrame, path: str, name: str):
#     """
#     Write a dataframe into a pickle file
#     """
#     file_path=os.path.join(path, name+'.pickle')
    
#     with open(file_path, 'wb') as f:
#         pickle.dump(df, f)
#     return file_path


def write_list_to_txt(input_list: list, path: str, name: str):
    """
    Write a list to a text file, with each item on a new line.

    Parameters:
    - file_path (str): The path to the text file.
    - input_list (list): The list to be written to the text file.
    """
    file_path=os.path.join(path, name+'.txt')
    with open(file_path, 'w') as file:
        for item in input_list:
            file.write(str(item) + '\n')
            
    return file_path

def write_jsonl(data: list,  path: str, name: str):
    """
    Write a jsonl file. Function takes as input a list of dict.
    """
    file_path=os.path.join(path, name+'.jsonl')
    with open(file_path, 'w') as file:
        for entry in data:
            json.dump(entry, file)
            file.write('\n')
    return file_path


def write_json(json_dict: dict, path: str, name: str):
    """
    Write a dict into a json file
    """
    file_path=os.path.join(path, name+'.json')
    with open(file_path, 'w') as outfile:
        json.dump(json_dict, outfile)
    return file_path


def write_dataframe_to_json(df: pd.DataFrame, path: str, name: str, orient='records'):
    """
    Write a dataframe into a json file
    """
    file_path=os.path.join(path, name+".json")
    df.to_json(file_path, orient=orient, lines=True)
    
    
def save_dataframe_excel(df: pd.DataFrame, path: str, name :str, sheet_name:str):
    """
    Write a dataframe into a XLSX file
    """
    
    file_path=os.path.join(path,  f"{name}.xlsx")
    df.to_excel(file_path, sheet_name=sheet_name, index=False)
    print(file_path, "- File created")
    return file_path

def add_dataframe_to_excel(df: pd.DataFrame, existing_file_path: str, new_sheet_name: str):
    """
    Adds a DataFrame to an existing Excel file as a new sheet.

    Parameters:
    - existing_file_path (str): Path to the existing Excel file.
    - dataframe (pd.DataFrame): The DataFrame to be added.
    - new_sheet_name (str): Name of the new sheet in the Excel file.

    Returns:
    - None
    """
    # Read existing Excel file into a dictionary of DataFrames
    excel_file = pd.read_excel(existing_file_path, sheet_name=None)

    # Add the new DataFrame to the dictionary with the specified sheet aname
    excel_file[new_sheet_name] = df

    # Write the updated dictionary of DataFrames back to the Excel file
    with pd.ExcelWriter(existing_file_path, engine='xlsxwriter') as writer:
        for sheet_name, df in excel_file.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def save_dataframe_csv(df: pd.DataFrame, path: str, name: str):
    """
    This function saves a DataFrame to a CSV file within a project directory.
    
    :param df: The DataFrame to be saved.
    :type df: pandas.DataFrame
    
    :param dir_csv: The directory where the CSV file will be saved.
    :type dir_csv: str
    
    :param name: The desired name for the CSV file (without extension).
    :type name: str
    """
    names = df.columns
    df.to_csv(
        os.path.join(path, f"{name}.csv"),
        header=names,
        sep=";",
        encoding="utf-8",
        index=False,
        decimal=",",
    )
    print("FILE SAVED: ", os.path.join(path, f"{name}.csv"))

def write_txt_file(data: str,  path: str, name: str):
    """
    Write a text file
    """
    file_path=os.path.join(path, name+'.txt')
    with open(file_path, "w") as file:
        file.write(data)
    return file_path

def split_df_into_chunks(df, path, name, chunk_size = 10000):
    """
    Split a dataframe into n pickle files
    """
    num_chunks = -(-len(df) // chunk_size)  # Calculate the number of chunks using ceil division

    file_paths=[]

    # create smaller datasets of chunk_size each
    for i in range(num_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        chunk = df.iloc[start:end]
        filename = f"{name}_{i}"  # Adjust the filename format as needed
        file_path = write_pickle(chunk, path, filename)
        file_paths.append(file_path)

    return file_paths



###################################################################################################
# FOLDERS / FILES HELPERS
###################################################################################################

def create_dir(path:str):
    """
    Create a local directory

    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, "- directory created")
    return path


def list_files_in_dir(path: str, filetype:str ='*.json'):
    """
    List files of a specific format in a directory
    """
    pattern = os.path.join(path, filetype)
    files = glob.glob(pattern)
    return files


def list_subdirectories(root_directory: str):
    """
    List subdirectories in a root directory
    """
    subdirectories = []
    for entry in os.scandir(root_directory):
        if entry.is_dir():
            subdirectories.append(entry.name)
    return subdirectories


def list_recursive_subdirectories(root_directory: str):
    """
    List recursively all subdirectories from a root directory
    """
    subdirectories = []
    for root, dirs, files in os.walk(root_directory):
        subdirectories.extend([os.path.join(root, d) for d in dirs])
    return subdirectories


def list_files_in_subdirectories(path:str, filetype:str='*.json'):
    """
    Walk through subdirectories of a root directory to list files of a specific format 
    """
    files = []

    # Check if the directory exists
    if not os.path.exists(path):
        print(f"The directory '{path}' does not exist.")
        return files

    # Use glob to get all files in the directory and its subdirectories
    pattern = os.path.join(path, '**', filetype)
    files = glob.glob(pattern, recursive=True)

    return files

def copy_file(source_path: str, destination_path: str, new_filename:str):
    """
    Function to copy a file to another path
    """
    if new_filename:
        file_path=os.path.join(destination_path, new_filename)
    else:
        filename=os.path.basename(source_path)
        file_path=os.path.join(destination_path,filename)
    shutil.copy(source_path, file_path)
    return file_path

def remove_file(file_path):
    """
    Remove a single file
    """
    try:
        os.remove(file_path)
        print(f"File {file_path} removed successfully.")
    except OSError as e:
        print(f"Error removing file {file_path}: {e}")
        
def remove_folder(folder_path):
    """
    Remove a folder and all the files inside
    """
    try:
        shutil.rmtree(folder_path)
        print(f"Folder {folder_path} and its contents removed successfully.")
    except OSError as e:
        print(f"Error removing folder {folder_path}: {e}")  
           
        
def get_file_size(file_path):
    """
    Get a single file size in a readable format (KB, MB, GB)
    """
    try:
        size = os.path.getsize(file_path)

        # Define the units and their respective sizes
        units = ['B', 'KB', 'MB', 'GB']
        size_in_units = size
        unit_index = 0

        # Convert size to appropriate unit
        while size_in_units > 1024 and unit_index < len(units) - 1:
            size_in_units /= 1024
            unit_index += 1

        # Format the result
        formatted_size = "{:.2f} {}".format(size_in_units, units[unit_index])
        print(formatted_size)
        return size, formatted_size
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def get_folder_size(folder_path):
    """
    Get size of all files contained in a folder in a readable format (KB, MB, GB)
    """
    total_size = 0

    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)

        # Define the units and their respective sizes
        units = ['B', 'KB', 'MB', 'GB']
        size_in_units = total_size
        unit_index = 0

        # Convert size to appropriate unit
        while size_in_units > 1024 and unit_index < len(units) - 1:
            size_in_units /= 1024
            unit_index += 1

        # Format the result
        formatted_size = "{:.2f} {}".format(size_in_units, units[unit_index])

        return total_size, formatted_size
    except FileNotFoundError:
        print(f"Folder not found: {folder_path}")
        return None

def file_creation_date(file_path):
    """
    Return the last update timestamp
    """
    # Check if the file exists
    if os.path.exists(file_path):
        # Get the last modified timestamp
        last_update_timestamp = os.path.getmtime(file_path)
        # Convert the timestamp to a datetime object
        last_update_date = datetime.fromtimestamp(last_update_timestamp)
        return last_update_date
    else:
        return None
    
############################################################################
# LISTS HELPERS
############################################################################
    
    
def transform_to_n_items_list(input_list : list, n: int):
    """
    Transform a list into a list of n-items sublists.

    Parameters:
    - input_list: The input list to be transformed.
    - n: The number of items in each sublist.

    Returns:
    A list of n-items sublists.
    """
    return [input_list[i:i + n] for i in range(0, len(input_list), n)]

def unduplicate_list(lst):
    """ 
    Unduplicate elements of a list
    """
    return list(set(lst))


def sort_list(lst, reverse=False):
    """
    Sort the list in ascending or descending order.

    Parameters:
    - lst (list): The input list.
    - reverse (bool): If True, sort the list in descending order. 
                     If False (default), sort the list in ascending order.

    Returns:
    - list: A new list sorted based on the specified order.
    """
    return sorted(lst, reverse=reverse)


def map_list(lst, function):
    """
    Apply a function to each element of the list.

    Parameters:
    - lst (list): The input list.
    - function (callable): The function to apply to each element.

    Returns:
    - list: A new list with the function applied to each element.
    """
    return [function(element) for element in lst]


def flatten_list(lst):
    """
    Flatten a nested list into a single list.

    Parameters:
    - lst (list): The input nested list.

    Returns:
    - list: A new list with all nested elements flattened.
    """
    flattened_list = []

    def flatten_recursive(sublist):
        for element in sublist:
            if isinstance(element, list):
                flatten_recursive(element)
            else:
                flattened_list.append(element)

    flatten_recursive(lst)
    return flattened_list


def find_occurrences(lst, element):
    """
    Find the occurrences of a specific element in the list.

    Parameters:
    - lst (list): The input list.
    - element: The element to find occurrences of.

    Returns:
    - int: The number of occurrences of the specified element in the list.
    """
    return lst.count(element)


def is_subset(subset, superset):
    """
    Check if one list is a subset of another.

    Parameters:
    - subset (list): The potential subset list.
    - superset (list): The superset list.

    Returns:
    - bool: True if the subset is a subset of the superset, False otherwise.
    """
    return all(element in superset for element in subset)

def common_elements(list1, list2):
    """
    Find the common elements between two lists.

    Parameters:
    - list1 (list): The first list.
    - list2 (list): The second list.

    Returns:
    - list: A new list containing the common elements between list1 and list2.
    """
    return list(set(list1) & set(list2))


def shuffle_list(lst):
    """
    Shuffle the elements of the list randomly.

    Parameters:
    - lst (list): The input list.

    Returns:
    - list: A new list with the elements shuffled randomly.
    """
    shuffled_list = lst.copy()
    random.shuffle(shuffled_list)
    return shuffled_list


def sample_list(lst, sample_size):
    """
    Sample a list based on an integer or a float representing the sample size.

    Parameters:
    - lst (list): The input list.
    - sample_size (int or float): If an integer, the number of elements to keep.
                                 If a float, the percentage of elements to keep.

    Returns:
    - list: A new list containing the sampled elements.
    """
    if isinstance(sample_size, int):
        if sample_size < 0:
            raise ValueError("Sample size must be a non-negative integer.")
        return random.sample(lst, min(sample_size, len(lst)))
    elif isinstance(sample_size, float):
        if not 0 <= sample_size <= 1:
            raise ValueError("Sample size must be a float between 0 and 1.")
        sample_size = int(sample_size * len(lst))
        return random.sample(lst, sample_size)
    else:
        raise TypeError("Sample size must be an integer or a float.")

def count_elements(lst):
    """
    Count the occurrences of each element in the list.

    Parameters:
    - lst (list): The input list.

    Returns:
    - dict: A dictionary where keys are unique elements from the list, and values are their counts.
    """
    return dict(Counter(lst))

def scale_list(lst, min_val=1, max_val=5):
    min_w = min(lst)
    max_w = max(lst)
    scaled_w = [ ]
    for x in lst:
        try:
            scaled_value = (x - min_w) / (max_w - min_w) * (max_val - min_val) + min_val
        except : 
            pass
            scaled_value = min_val
        
        scaled_w.append(scaled_value)
    return scaled_w

def df_scale_column(df, col_to_scale, col_out, min_val, max_val):
    min_freq = df[col_to_scale].min()
    max_freq = df[col_to_scale].max()
    df[col_out] = df[col_to_scale].apply(lambda x : ((x - min_freq) / (max_freq - min_freq)) * (max_val - min_val) + min_val)
    return df

############################################################################
# ZIP HELPERS
############################################################################      
    
def zip_file(source_file_path, zip_file_path, name):
    """
    Zip a single file.

    Args:
        source_file_path (str): Path to the file to be zipped.
        zip_file_path (str): Path for the resulting zip file.

    Returns:
        None
    """
    file_path=os.path.join(zip_file_path, name+".zip")
 
    with zipfile.ZipFile(file_path, 'w') as zip_file:
        # The second argument to `arcname` is used to set the name of the file inside the zip
        zip_file.write(source_file_path, arcname=os.path.basename(source_file_path))

    return file_path
    
def zip_folder(source_folder_path, zip_file_path, name):
    """
    Zip an entire folder.

    Args:
        source_folder_path (str): Path to the folder to be zipped.
        zip_file_path (str): Path for the resulting zip file.

    Returns:
        None
    """
    file_path=os.path.join(zip_file_path, name+".zip")
    
    with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for foldername, subfolders, filenames in os.walk(source_folder_path):
            for filename in filenames:
                fpath = os.path.join(foldername, filename)
                arcname = os.path.relpath(fpath, source_folder_path)
                zip_file.write(fpath, arcname=arcname)
                
    return file_path

def unzip_file(zip_file_path, destination_path):
    """
    unzip a zip file
    """
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(destination_path)
        
    

############################################################################
# Google Spreadsheets HELPERS
############################################################################   


def create_google_spreadsheet_client(credentials:str):
    """
    Create a Gspread client to interact with Google Sheets
    """
    return gspread.service_account(filename=credentials)

def read_google_spreadsheet(client, sheet_id: str, worksheet_name: str):
    """
    Function to read a Google spreadsheet in a DataFrame
    """
    try:
    
        # Open the Google Spreadsheet by name
        sheet = client.open_by_key(sheet_id)
        
        # Select a specific worksheet by name
        worksheet = sheet.worksheet(worksheet_name)
        
        # Get all values from the worksheet
        df = pd.DataFrame(worksheet.get_all_records())
        
        return df
    except exceptions.GoogleAuthError as e:
        print(f"Authentication error: {e}")
    except gspread.exceptions.APIError as e:
        print(f"API error: {e}")
    except gspread.exceptions.WorksheetNotFound as e:
        print(f"Worksheet not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def list_google_worksheets(client, sheet_id:str):
    """
    Return a list of worksheet names for a spreadsheet ID
    """
    sheet = client.open_by_key(sheet_id)
    worksheet_obj = sheet.worksheets()
    worksheet_list = [sheet.title for sheet in worksheet_obj]
    return worksheet_list
    
def get_spreadsheet_permissions(client, sheet_id:str):
    """
    Return a DataFrame with the list of user email and type that can access the document
    """
    sheet = client.open_by_key(sheet_id)
    permissions=sheet.list_permissions()
    user_list=[(user.get("emailAddress"),user.get("type")) for user in permissions if user.get("emailAddress") is not None]
    df = pd.DataFrame(user_list, columns=['email', 'type'])
    return df


def create_google_spreadsheet(client, df, filename:str, worksheet_name:str = "Sheet1"):
    """
    Load a dataframe in a new spreadsheet 
    """
    spreadsheet = client.create(filename)
    worksheet = spreadsheet.sheet1
    if worksheet_name != "Sheet1":
        worksheet.update_title(worksheet_name)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    return spreadsheet

def share_google_spreadsheet(spreadsheet, email, user_type="user", user_role="writer", notify=False, email_message=None, with_link=False):
    """
    Share a spreadsheet with a user
    """
    spreadsheet.share(email, perm_type=user_type, role=user_role, notify = notify, email_message=email_message, with_link=with_link)
    return spreadsheet


def generate_short_id(variables : dict):
    """
    Generate a 8 characters ID using a dict as input
    """
    # Serialize variables into JSON string
    serialized_variables = json.dumps(variables, sort_keys=True)
    # Generate a hash of the serialized variables
    hash_value = hashlib.sha256(serialized_variables.encode()).hexdigest()
    # Take the first 8 characters of the hash as the short ID
    short_id = hash_value[:8]
    return short_id, serialized_variables

def df_transform_column_as_list(column):
    def transform(cell):
        if isinstance(cell, str):
            # Check if it's a list formatted as string, and convert to list
            if cell == "nan":
                values = []
            else:
                try:
                    values = ast.literal_eval(cell)
                    
                except Exception as e:
                    pass
                    # If it's a single URL as string, make it a list
                    values = [cell]
        elif isinstance(cell, (int, float, bool)):
            # Convert single value to list
            values = [cell]
        elif isinstance(cell, list):
            # If it's already a list, use it as is
            values = cell
        elif cell is None:
            values=[]
        else:
            values=[cell]
        return values

    return column.apply(transform)


def top_rows_per_category(df, col_to_sort, col_to_gb, cols_to_keep, top_rows) : 
    """
    Select top rows for each category in a dataframe
    """
    df_gb = (df.sort_values(by=col_to_sort, ascending=False)
                 .groupby(col_to_gb)
                 .apply(lambda group: group.head(top_rows))
                 .reset_index(drop=True)
                )[cols_to_keep]
    return df_gb

def format_number(number):
    """
    Function to format a number in K, M or B
    """
    if number < 1000:
        return str(number)
    elif number < 1000000:
        return f"{number / 1000:.1f}K"
    elif number < 1000000000:
        return f"{number / 1000000:.1f}M"
    else:
        return f"{number / 1000000000:.1f}B"