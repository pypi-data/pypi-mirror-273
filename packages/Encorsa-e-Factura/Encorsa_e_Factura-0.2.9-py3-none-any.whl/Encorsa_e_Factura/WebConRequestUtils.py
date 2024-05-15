import json
import requests

try:
    from .XMLUtils import *
except ImportError:
    from XMLUtils import *


def create_webcon_body(parameters, xml_b64, pdf_b64, xml_file_data, id, cui, template_xml_path, wfd_id_duplicate, namespaces, document_type, id_anaf, iso_data_creare):

    processor = XMLProcessor(template_xml_path, xml_file_data, namespaces)
    all_lists_data, extracted_data = processor.process_xml()

    item_lists_json = create_list_of_dicts(all_lists_data)
    form_fields_json = create_form_filed_json(extracted_data)

    form_fields_json.extend([
        {
            "guid": parameters['id_field_guid'],
            "svalue": id
        },
        {
            "guid": parameters['cui_field_guid'],
            "svalue": cui
        }
    ])

    body = {
        "workflow": {
            "guid": parameters['webcon_wfid'],
        },
        "formType": {
            "guid": parameters['webcon_wfdid'],
        },
        "formFields": form_fields_json,
        "itemLists": item_lists_json,
        "attachments": [
            {
                "name": "fisierXML.xml",
                "content": xml_b64
            },
            {
                "name": "fisierPDF.pdf",
                "content": pdf_b64
            }
        ],
        "businessEntity": {
            "id": parameters['webcon_bentity']
        }
    }

    if "webcon_parent_wfdid" in parameters and parameters['webcon_parent_wfdid'] is not None and parameters['webcon_parent_wfdid'] not in ['', 0]:
        body["parentInstanceId"] = parameters['webcon_parent_wfdid']

    add_value_to_form_field(
        parameters, "duplicate_wfdid_field_guid", body, wfd_id_duplicate)
    add_value_to_form_field(
        parameters, "tipInregistrare_Nota_sau_Factura", body, document_type)
    add_value_to_form_field(parameters, "ID_Descarcare_ANAF", body, id_anaf)
    add_value_to_form_field(
        parameters, "Data_Creare_ANAF", body, iso_data_creare)

    return body


def add_value_to_form_field(parameters, parameter_key, body, value):
    if value is None:
        value = ''

    value = str(value)

    if parameter_key in parameters and parameters[parameter_key] is not None and parameters[parameter_key] not in ['', 0]:
        found = False
        for body_field in body["formFields"]:
            if body_field["guid"] == parameters[parameter_key]:
                body_field["svalue"] = value
                found = True
                break
        if not found:
            body["formFields"].append(
                {"guid": parameters[parameter_key], "svalue": value})


def create_list_of_dicts(data_dict):
    result_list = []
    for item_list_guid, rows in data_dict.items():
        item_list_wrapper = {}
        item_list_wrapper['guid'] = item_list_guid
        row_lists = []
        for row in rows:
            row_dict = {}
            cells_list = []
            for cell_guid, cell_value in row.items():  # Iterate over the items in the row dictionary
                cell_dict = {
                    'guid': cell_guid, 'svalue': cell_value if cell_value is not None else ''}
                cells_list.append(cell_dict)
            row_dict['cells'] = cells_list
            row_lists.append(row_dict)
        item_list_wrapper['rows'] = row_lists
        result_list.append(item_list_wrapper)
    return result_list


def create_form_filed_json(extracted_data):
    form_fields = []
    for key, value in extracted_data.items():
        field = {'guid': key, 'svalue': value if value is not None else ''}
        form_fields.append(field)
    return form_fields


"""
Această funcție obține un token de autentificare de la serviciul WebCon
"""


def get_webcon_token(base_url, client_id, client_secret):
    url = f"{base_url}/api/login"  # Ensure this is the correct API endpoint

    headers = {
        'Content-Type': 'application/json',
    }

    payload = {
        "clientId": client_id,
        "clientSecret": client_secret
    }

    try:
        proxies = {
            'http': None,
            'https': None
        }

        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload), proxies=proxies)

        if response.status_code == 200:
            try:
                return response.json()["token"]
            except KeyError:
                # Key 'token' does not exist in the response
                print(
                    "Error at getting WebCon TOKEN: The response JSON does not contain a 'token' key")
                raise Exception(
                    "Error at getting WebCon TOKEN: The response JSON does not contain a 'token' key")
        else:
            # For non-successful responses, raise an exception with status code and error
            print(
                f"Error at getting WebCon TOKEN: HTTP {response.status_code} - {response.text}")
            raise Exception(
                f"Error at getting WebCon TOKEN: HTTP {response.status_code} - {response.text}")
    except Exception as e:
        # A single catch-all for any exception, including request errors, HTTP errors, and JSON parsing errors
        print(f"Error at getting WebCon TOKEN: {str(e)}")
        raise Exception(f"Error at getting WebCon TOKEN: {str(e)}")


def create_invoice_instance(parameters, token, body):
    url = f"{parameters['webcon_base_url']}/api/data/{parameters['webcon_api_version']}/db/{parameters['webcon_dbid']}/elements?path={parameters['webcon_path']}&mode={parameters['webcon_mode']}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    proxies = {
        'http': None,
        'https': None
    }

    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps(body), proxies=proxies)

        if response.status_code == 200:
            return response.json()
        else:
            error_message = response.json().get('description', 'Unknown error occurred')
            error_code = response.status_code
            # Including more detailed information in the exception
            print(
                f"Failed to create WebCon invoice instance. Error code: {error_code}, Message: {error_message}")
            raise Exception(
                f"Failed to create WebCon invoice instance. Error code: {error_code}, Message: {error_message}")
    except Exception as e:
        # Catching any other exceptions that weren't anticipated
        print(
            f"Failed to create WebCon invoice instance. An unexpected error occurred: {str(e)}")
        raise Exception(
            f"Failed to create WebCon invoice instance. An unexpected error occurred: {str(e)}")


"""
Functia trebuie sa isi ia datele dintr-un raport cu facturi care
contine numai doua coloane: ID-factura si CUI, fara a schimba ordinea lor
"""


def check_if_invoice_exists(parameters, token, invoice_id, supplier_company_id):
    base_url = f"{parameters['webcon_base_url']}/api/data/{parameters['webcon_api_version']}"
    url = f"{base_url}/db/{parameters['webcon_dbid']}/applications/{parameters['webcon_report_app_id']}/reports/{parameters['webcon_report_id']}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    proxies = {
        'http': None,
        'https': None
    }

    filters = {
        f'{parameters["invoice_id_url_filter"]}': invoice_id,
        f'{parameters["supplier_company_id_url_filter"]}': supplier_company_id,
        'page': 1,
        'size': 1
    }

    try:
        response = requests.get(url, headers=headers,
                                params=filters, proxies=proxies)
        response.raise_for_status()
        data = response.json()
        count = len(data['rows'])

    except Exception as err:
        print(
            f"Failed to get Invoices list from WebCon report. An unexpected error occurred: {str(err)}")
        raise Exception(
            f"Failed to get Invoices list from WebCon report. An unexpected error occurred: {str(err)}")

    if count <= 0:
        return False, 0
    else:
        max_id = min(data['rows'], key=lambda x: x['id'])['id']
        return True, max_id if max_id else 0
