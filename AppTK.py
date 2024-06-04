import json
import pdfrw
import datetime
import tkinter as tk
from tkinter import messagebox

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

def create_dict(i, *args):
    data_dict = {}
    for key, value in args:
        data_dict['{}_{}'.format(key, i)] = value
    return data_dict

class PDFGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Generator")

        self.data_dict_header = data_dict_header.copy()
        self.data_dict_details = {key: '' for key in data_keys_names}

        self.create_widgets()

    def create_widgets(self):
        # Header fields
        row = 0
        for key in self.data_dict_header:
            label = tk.Label(self.root, text=key)
            label.grid(row=row, column=0, padx=10, pady=5)
            entry = tk.Entry(self.root)
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.data_dict_header[key] = entry
            row += 1

        # Detail fields
        row = 0
        col = 2
        for key in self.data_dict_details:
            label = tk.Label(self.root, text=key)
            label.grid(row=row, column=col, padx=10, pady=5)
            entry = tk.Entry(self.root)
            entry.grid(row=row, column=col+1, padx=10, pady=5)
            self.data_dict_details[key] = entry
            row += 1
            if row == 10:  # Adjust the layout if there are too many fields
                row = 0
                col += 2

        # Generate PDF Button
        generate_button = tk.Button(self.root, text="Generate PDF", command=self.generate_pdf)
        generate_button.grid(row=row+1, column=0, columnspan=4, pady=20)

    def generate_pdf(self):
        data_dict_header_filled = {key: entry.get() for key, entry in self.data_dict_header.items()}
        data_dict_details_filled = {key: entry.get() for key, entry in self.data_dict_details.items()}

        # Save to JSON
        save_dict_to_file(data_dict_header_filled, 'data_dict_header.json')
        save_dict_to_file(data_dict_details_filled, 'data_dict_details.json')

        # Generate PDF
        unique_output_path = get_unique_output_path(INVOICE_OUTPUT_PATH)
        write_fillable_pdf(INVOICE_TEMPLATE_PATH, unique_output_path, data_dict_header_filled)
        write_fillable_pdf(unique_output_path, unique_output_path, data_dict_details_filled)

        messagebox.showinfo("Success", f"PDF generated successfully: {unique_output_path}")

if __name__ == '__main__':
    root = tk.Tk()
    app = PDFGeneratorApp(root)
    root.mainloop()
