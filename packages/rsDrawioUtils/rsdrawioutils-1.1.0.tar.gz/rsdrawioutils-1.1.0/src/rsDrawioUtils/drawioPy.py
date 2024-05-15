import difflib
import re
from bs4 import BeautifulSoup
import openpyxl

def normalize_drawio_json(drawio_json: dict) -> dict:
    """
    Normalizes the drawio json to a format that can be used to compare to the excel file
    :param drawio_json: dict
    :return: dict
    """
    normalized = []
    for obj in drawio_json['mxfile']['diagram']['mxGraphModel']['root']['mxCell']:
        if '@edge' in obj:
            continue
        if '@value' in obj:
            obj_value_html = obj['@value']
            soup = BeautifulSoup(obj_value_html, 'html.parser')
            obj_value = soup.get_text(strip=True)
            if obj_value == '':
                obj_value = obj['@value']
            obj_id = obj['@id'].strip()
            obj_parent = obj['@parent'].strip()
            
            if normalized:
                is_class = True
                for item in normalized:
                    if item['id'] == obj_parent:
                        item['attributes'].append(obj_value)
                        is_class = False
                        break
                if is_class:
                    normalized.append({'id': obj_id, 'class': obj_value, 'attributes': []})
            else:
                normalized.append({'id': obj_id, 'class': obj_value, 'attributes': []})
                
    # loop over normalized to remove obj with empty children
    class_list = []
    for obj in normalized:
        if obj['attributes']:
            class_list.append(obj)
    
    num_class = len(class_list)
    num_attr = 0
    for obj in class_list:
        num_attr += len(obj['attributes'])
    info = {
        'num_classes': num_class,
        'num_attributes': num_attr
    }
                
    return class_list, normalized, info

def good_text(text):
    # Check for blank string (only whitespace or empty)
    if not text.strip():
        return False

    # Check for bad text: non-alphanumeric or HTML-like structures
    if re.search(r'^[\+\-!@#\$%\^&\*\(\)\[\]]', text) or re.search(r'<[^>]+>', text):
        return False

    # Assume any other non-blank text is generally 'Good Text'
    return True

def find_errors(class_list: dict) -> dict:
    '''
    A function to find errors in the normalized json
    :param normalized: dict
    :return: dict
    '''
    for obj in class_list:
        current_errors = []
        if obj['class'] == '':
            current_errors.append('class name is empty')
        if not obj['attributes']:
            current_errors.append('attributes list is empty')
        for attribute in obj['attributes']:
            if not good_text(attribute):
                current_errors.append(f'bad text: {attribute}')
        if current_errors:
            obj['errors'] = current_errors
    return class_list

def class_list_to_excel(class_list: dict, save_path: str):
    '''
    A function to save the class list to an excel file
    :param class_list: dict
    :param save_path: str
    :return: None
    '''
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Attribute Lists'
    
    
    for class_name in class_list:
        ws.append([class_name['class']])
        
        
def extract_model_info(info_cell):
    '''
    A function to extract model information from a cell in an Excel sheet
    
    :param info_cell: str
    :return: dict
    '''
    # Adjusted regular expression pattern to capture a variable model name
    pattern = r"(?i)(.*?) ([\d\.]+) derived from (.*?) ([\d\.]+) (draft|final) (\d{2}/\d{2}/\d{4})"
    
    # Dictionary to hold the extracted information
    model_info = {}

    # Extracting information using the defined regular expression
    match = re.search(pattern, info_cell, re.IGNORECASE)
    if match:
        model_info = {
            "model_name": match.group(1).lower(),
            "model_version": match.group(2),
            "derived_from_model": match.group(3).lower(),
            "derived_from_model_version": match.group(4),
            "status": match.group(5).lower(),
            "date": match.group(6).lower()
        }
        return model_info
    else:
        raise ValueError("Model information not found in the provided file.")
    
    
def compare_models(fileA: dict, fileB: dict) -> dict:
    """
    Compares two dictionaries and corrects the differences between them, excluding the detailed character position differences.
    :param fileA: dict containing objects with class and attributes.
    :param fileB: dict containing objects with class and attributes.
    :return: A list of dictionaries with the corrected attributes.
    """
    corrected = []
    
    for objA in fileA:
        class_name = objA['class']
        
        found = False
        for objB in fileB:
            if objB['class'] == class_name:
                difference = difflib.Differ().compare(objA['attributes'], objB['attributes'])
                # Filter out the lines that start with '?'
                filtered_difference = [line for line in difference if not line.startswith('?')]
                corrected.append({"class": class_name, "attributes": filtered_difference})
                found = True
                break  # Exit the inner loop once a match is found
        
        if not found:
            corrected.append(objA)
        
    return corrected