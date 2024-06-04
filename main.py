import json
import pdfrw
import datetime

INVOICE_TEMPLATE_PATH = 'Busqueda trabajo workintexas may 06-may10 segunda semana.pdf'
INVOICE_OUTPUT_PATH = 'filled_PDF'
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

data_dict_header = {
    'NAME': '',
    'WEEK': '',
    'END_DATE': '',
    'SOCIAL_FIRST_3': '',
    'SOCAL_MIDDLE_2': '',
    'SOCAL_LAST_4': '',
    'REQUIRED_NUMBER': ''
}

data_keys_names = (
    'DATE_ACT',
    'WORK_SEARCH',
    'JOB_TYPE',
    'ORG_ADD',
    'C_S_Z',
    'AREA_CODE',
    'PHONE_3_MIDDLE',
    'PHONE_4_LAST',
    'CONTACT_PERSON',
    'MAIL_CONTACT_CHECK',
    'MAIL_CONTACTED_CHECK',
    'MAIL_ADD',
    'FAX_CONTACT_CHECK',
    'FAX_AREA_CODE',
    'FAX_3_MIDDLE_NUMBER',
    'FAX_4_LAST_NUMBER',
    'HIRED',
    'NOT_HIRED',
    'START_DATE_HIRED',
    'CHECK_APPLICATION_FILL',
    'CHECK_OTHER',
    'OTHER_JOB_RES'
)


def get_unique_output_path(base_output_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    output_path = f"{base_output_path}_{timestamp}.pdf"
    return output_path


def save_dict_to_file(data_dict, file_path='data_dict.json'):
    with open(file_path, 'w') as f:
        json.dump(data_dict, f)


def load_dict_from_file(file_path='data_dict.json'):
    with open(file_path, 'r') as f:
        data_dict = json.load(f)
    return data_dict


def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotations = template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    if isinstance(data_dict[key], bool):
                        if data_dict[key]:
                            annotation.update(
                                pdfrw.PdfDict(V=pdfrw.PdfName('X'), AS=pdfrw.PdfName('X'))
                            )
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V=pdfrw.PdfName(''), AS=pdfrw.PdfName(''))
                            )
                    else:
                        annotation.update(
                            pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                        )
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


def get_user_input_for_dict_keys(data_dict, file_path='data_dict.json'):
    try:
        data_dict = load_dict_from_file(file_path)
        use_saved_values = input("¿Desea utilizar los valores almacenados en la sesión anterior? (s/n): ")
        if use_saved_values.lower() != 's':
            while True:
                # Mostrar un índice con las claves de los valores almacenados
                for i, key in enumerate(data_dict.keys()):
                    print(f"{i}: {key}")
                # Solicitar al usuario que seleccione la clave que desea modificar
                key_index = int(input("Por favor, seleccione el índice de la clave que desea modificar: "))
                key_to_modify = list(data_dict.keys())[key_index]
                # Solicitar al usuario que ingrese el nuevo valor para la clave seleccionada
                data_dict[key_to_modify] = input(f"Por favor, ingrese el nuevo valor para {key_to_modify}: ")
                # Preguntar al usuario si desea cambiar otro valor
                change_another_value = input("¿Desea cambiar otro valor? (s/n): ")
                if change_another_value.lower() != 's':
                    break
            save_dict_to_file(data_dict, file_path)
    except FileNotFoundError:
        for key in data_dict.keys():
            data_dict[key] = input(f"Por favor, ingrese el valor para {key}: ")
        save_dict_to_file(data_dict, file_path)
    return data_dict


def create_dict(i, *args):
    data_dict = {}
    for key, value in args:
        data_dict['{}_{}'.format(key, i)] = value
    return data_dict


if __name__ == '__main__':
    unique_output_path = get_unique_output_path(INVOICE_OUTPUT_PATH)
    write_fillable_pdf(INVOICE_TEMPLATE_PATH, unique_output_path, get_user_input_for_dict_keys(data_dict_header))
    write_fillable_pdf(unique_output_path, unique_output_path, create_dict(
        5,
        (data_keys_names[0], '2024-05-06'),
        (data_keys_names[1], 'Software Developer'),
        (data_keys_names[2], 'Full Time')))
