import tkinter as tk
from tkinter import ttk, BooleanVar
from guizero import App, Box, Text, PushButton, TextBox, Picture, ButtonGroup, Combo, CheckBox
import pandas as pd
import json
import pdfrw
import datetime

colors = ['#27272A',
          '#202020',
          '#05111D',
          '#111828',
          '#6495ED',
          '#4B0082']

tab_opt = [["Header", "1"],
           ["Description", "2"],
           ["Location", "3"],
           ["Contact", "4"],
           ["Results", "5"]]

INVOICE_TEMPLATE_PATH = 'Template.pdf'
INVOICE_OUTPUT_PATH = 'filled_PDF'
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

# pyinstaller --onefile --name WorkPDFill --windowed --paths C:\Users\hansn\OneDrive\Escritorio\PDF_Filler GUI.py


class Gui:

    def __init__(self):
        self.textboxes_contact = None
        self.section_sec = None
        self.textboxes_location = None
        self.textboxes_description = None
        self.textboxes_header = None
        self.tabs = None
        self.tabs_to_sections = {"1": "header", "2": "description", "3": "location", "4": "contact", "5": "results"}
        self.history = {"header": [], "description": [], "location": [], "contact": [], "results": []}
        self.history_file_path = 'history.json'
        self.data = self.load_data_from_file()
        self.app = App(title="Work in Texas PDF Filler",
                       width=800, height=620,
                       layout="grid",
                       bg=colors[1])
        self.box_header = Box(self.app,
                              width=self.app.width,
                              height=50,
                              border=False,
                              grid=[0, 0])
        self.box_header.bg = colors[1]
        Text(self.box_header,
             text="Work in Texas PDF Form",
             size=25,
             font="Arial",
             color="white",
             align="bottom")
        Box(self.app,
            width=self.app.width,
            height=15,
            border=False,
            grid=[0, 1])
        self.box_body = Box(self.app,
                            width=self.app.width,
                            height=int(self.app.height) - 115,
                            border=False,
                            grid=[0, 2],
                            layout="grid")
        self.box_body.bg = colors[2]
        self.box_footer = Box(self.app,
                              width=self.app.width,
                              height=50,
                              border=False,
                              grid=[0, 3],
                              layout="grid")
        Box(self.box_footer,
            width=50,
            height=50,
            border=False,
            grid=[0, 0])
        self.time_label = Text(self.box_footer,
                               text="",
                               size=10,
                               font="Arial",
                               color="white",
                               grid=[1, 0])
        Box(self.box_footer,
            width=430,
            height=50,
            border=False,
            grid=[2, 0])
        PushButton(self.box_footer,
                   text="Export History",
                   command=self.export_history,
                   grid=[3, 0]).tk.config(activebackground=colors[4],
                                          activeforeground="white",
                                          borderwidth=1,
                                          cursor="hand2",
                                          fg="white",
                                          bg=colors[5],
                                          relief="sunken")
        Box(self.box_footer,
            width=15,
            height=50,
            border=False,
            grid=[4, 0])
        PushButton(self.box_footer,
                   text="Show PDF",
                   command=self.show_pdf,
                   grid=[5, 0]).tk.config(activebackground=colors[4],
                                          activeforeground="white",
                                          borderwidth=1,
                                          cursor="hand2",
                                          fg="white",
                                          bg=colors[5],
                                          relief="sunken")
        Box(self.box_body,
            width=int(self.box_body.width / 6),
            height=self.box_body.height,
            border=False,
            grid=[0, 0])
        self.content_box = Box(self.box_body,
                               width=int((int(self.box_body.width) / 10) * 5),
                               height=self.box_body.height,
                               border=False,
                               grid=[1, 0],
                               layout="grid")
        self.content_box.bg = colors[2]
        self.tab_title = Box(self.content_box,
                             width=self.content_box.width,
                             height=int((self.content_box.height / 10) / 2),
                             border=False,
                             grid=[0, 0])
        self.tab_title.bg = colors[2]
        self.title_tab = Text(self.tab_title,
                              text="",
                              size=15,
                              font="Arial",
                              color="#C71585",
                              align="bottom")
        self.main_box = Box(self.content_box,
                            width=self.content_box.width,
                            height=int(self.content_box.height / 10) * 9,
                            border=True,
                            grid=[0, 1])
        self.main_box.bg = colors[3]
        print(self.main_box.width, self.main_box.height)
        self.header_box = Box(self.main_box,
                              width=self.main_box.width,
                              height=self.main_box.height,
                              border=False,
                              layout="grid")
        self.header_box.visible = False
        self.description_box = Box(self.main_box,
                                   width=self.main_box.width,
                                   height=self.main_box.height,
                                   border=False,
                                   layout="grid")
        self.description_box.visible = False
        self.location_box = Box(self.main_box,
                                width=self.main_box.width,
                                height=self.main_box.height,
                                border=False,
                                layout="grid")
        self.location_box.visible = False
        self.contact_box = Box(self.main_box,
                               width=self.main_box.width,
                               height=self.main_box.height,
                               border=False,
                               layout="grid")
        self.contact_box.visible = False
        self.results_box = Box(self.main_box,
                               width=self.main_box.width,
                               height=self.main_box.height,
                               border=False,
                               layout="grid")
        self.results_box.visible = False
        Box(self.content_box,
            width=self.content_box.width,
            height=int((self.content_box.height / 10) / 2),
            border=False,
            grid=[0, 2])
        Box(self.box_body,
            width=int((int(self.box_body.width) / 10) / 8),
            height=self.box_body.height,
            border=False,
            grid=[2, 0])
        self.tabs_box = Box(self.box_body,
                            width=int((int(self.box_body.width) / 10) * 2),
                            height=self.box_body.height,
                            border=False,
                            grid=[3, 0],
                            layout="grid")
        self.tabs_box.bg = colors[2]
        Box(self.tabs_box,
            width=self.tabs_box.width,
            height=int((self.tabs_box.height / 8)),
            border=False,
            grid=[0, 0])
        self.tabs_box_content = Box(self.tabs_box,
                                    width=self.tabs_box.width,
                                    height=int(self.tabs_box.height / 8) * 6,
                                    border=True,
                                    grid=[0, 1],
                                    layout="grid")
        self.tabs_box_content.bg = colors[3]
        Box(self.tabs_box,
            width=self.tabs_box.width,
            height=int((self.tabs_box.height / 8)),
            border=False,
            grid=[0, 2])
        Box(self.box_body,
            width=int(self.box_body.width / 10),
            height=self.box_body.height,
            border=False,
            grid=[4, 0])
        self.tabs_menu()
        self.time_label.repeat(1000, self.update_time)
        self.app.when_closed = self.do_this_when_closed
        self.app.display()

    def get_unique_output_path(self, base_output_path):
        week_date = self.data.get('WEEK', '')
        end_date = self.data.get('END_DATE', '')
        try:
            week_date = datetime.datetime.strptime(week_date, '%Y/%m/%d').strftime('%d-%b-%y')
            end_date = datetime.datetime.strptime(end_date, '%Y/%m/%d').strftime('%d-%b-%y')
        except ValueError:
            pass
        output_path = f"{base_output_path}_{week_date}_{end_date}.pdf"
        return output_path

    def update_time(self):
        # Actualizar la hora y la fecha actual
        now = datetime.datetime.now()
        self.time_label.value = now.strftime("%Y-%m-%d\n%H:%M:%S")

    def export_history(self):
        try:
            # Leer el archivo JSON
            with open(self.history_file_path, 'r') as f:
                history = json.load(f)

            # Aplanar el JSON y convertirlo en un DataFrame
            flattened_data = []
            for section, records in history.items():
                for record in records:
                    for key, value in record.items():
                        if isinstance(value, list) and value and isinstance(value[0], dict):
                            for i, item in enumerate(value):
                                flattened_item = {f"{key}_{sub_key}_{i}": sub_value for sub_key, sub_value in item.items()}
                                flattened_data.append(flattened_item)
                        else:
                            flattened_data.append({key: value})

            df = pd.json_normalize(flattened_data)

            # Reemplazar los NaN con una cadena vacía
            df = df.fillna('')

            # Exportar el DataFrame a CSV sin nombres de columnas
            csv_file_path = 'history.csv'
            df.to_csv(csv_file_path, sep=',', index=False, header=False)

            self.app.info("Success", "History exported successfully.")
        except Exception as e:
            self.app.error("Error", f"An error occurred while exporting the history: {e}")

    def show_pdf(self):
        import webbrowser
        try:
            webbrowser.open_new_tab(self.get_unique_output_path(INVOICE_OUTPUT_PATH))
        except Exception as e:
            self.app.error("Error", f"Error opening the PDF file: {e}")
            pass

    @staticmethod
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

    @staticmethod
    def save_data_to_file(data, file_path='data.json'):
        # Prepare a new dictionary to hold the serializable data
        serializable_data = {}
        for key, value in data.items():
            # If the value is a CheckBox, store its state (value property)
            if isinstance(value, CheckBox):
                serializable_data[key] = value.value
            else:
                # If the value is not a CheckBox, store it as is
                serializable_data[key] = value
        try:
            with open(file_path, 'w') as f:
                json.dump(serializable_data, f)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    @staticmethod
    def load_data_from_file(file_path='data.json'):
        try:
            with open(file_path, 'r') as f:
                data = f.read()
                return json.loads(data) if data else {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def tabs_menu(self):
        Text(self.tabs_box_content,
             text="Select a tab\nto fill section:",
             size=10,
             font="Monospace",
             color="#FFCE51",
             align="top",
             grid=[0, 0, 1, 2])
        self.tabs = ButtonGroup(self.tabs_box_content,
                                options=tab_opt,
                                selected="",
                                horizontal=False,
                                command=self.section_select,
                                grid=[0, 2, 1, 2])

        self.tabs.bg = colors[3]
        self.tabs.text_size = 8
        for radio_button in self.tabs.children:
            radio_button.tk.config(activebackground="green",
                                   activeforeground="white",
                                   borderwidth=2,
                                   cursor="hand2",
                                   fg="white",
                                   relief="flat",
                                   selectcolor="blue")

    def set_active(self, select_box):
        boxes = [self.header_box,
                 self.description_box,
                 self.location_box,
                 self.contact_box,
                 self.results_box]
        for box in boxes:
            if box == select_box:
                box.visible = True
                box.enabled = True
            else:
                box.visible = False
                box.enabled = False

    def section_select(self):
        self.app.update()
        match self.tabs.value:
            case "1":
                self.title_tab.value = "Header Section"
                self.set_active(self.header_box)
                self.header_section()
            case "2":
                self.title_tab.value = "Description Section"
                self.set_active(self.description_box)
                self.description_section()
            case "3":
                self.title_tab.value = "Location Section"
                self.set_active(self.location_box)
                self.location_section()
            case "4":
                self.title_tab.value = "Contact Section"
                self.set_active(self.contact_box)
                self.contact_section()
            case "5":
                self.title_tab.value = "Results Section"
                self.set_active(self.results_box)
                self.results_section()
            case _:
                self.title_tab.value = ""

    @staticmethod
    def create_element(parent, label_text, grid_pos):
        Text(parent,
             text=label_text,
             size=10,
             font="Arial",
             color="white",
             grid=[0, grid_pos],
             align="left")
        entry_var = tk.StringVar()
        entry = ttk.Entry(parent.tk, textvariable=entry_var, width=25)
        entry.grid(column=1, row=grid_pos)
        return entry_var

    def populate_textboxes(self, textboxes):
        for key, textbox in textboxes.items():
            if textbox is not None and key in self.data:
                textbox.set(self.data[key])

    def update_textboxes(self, textboxes, selected_number):
        self.data = self.load_data_from_file()
        for key, textbox in textboxes.items():
            full_key = f"{key}_{selected_number}"
            if full_key in self.data:
                if isinstance(textbox, CheckBox):
                    textbox.value = self.data[full_key]
                else:
                    textbox.set(self.data[full_key])
            else:
                if isinstance(textbox, CheckBox):
                    textbox.value = 0
                else:
                    textbox.set("")

    def clear_textboxes(self, textboxes, selected_number):
        for key, textbox in textboxes.items():
            if textbox is not None:
                if isinstance(textbox, CheckBox):
                    textbox.value = 0
                else:
                    textbox.set("")
                full_key = f"{key}_{selected_number}"
                if full_key in self.data:
                    del self.data[full_key]  # Elimina la entrada del diccionario
        self.save_data_to_file(self.data)  # Guarda el diccionario actualizado en el archivo JSON

    def show_history(self):
        section = self.tabs_to_sections[self.tabs.value]
        with open(self.history_file_path, 'r') as f:
            history = json.load(f).get(section, [])
        # Crea un DataFrame a partir de los registros de la historia, utilizando las claves como nombres de las columnas
        df = pd.DataFrame.from_records(history)
        self.show_df_in_table(df)

    @staticmethod
    def show_df_in_table(df):
        df = df.fillna('')  # Rellena los NaN con una cadena vacía
        df = df.transpose()  # Transpone el DataFrame si es necesario para tu diseño específico

        window = tk.Tk()
        window.title("DataFrame")
        frame = ttk.Frame(window)
        frame.pack(fill='both', expand=True)
        treeview = ttk.Treeview(frame)
        treeview["columns"] = list(df.columns)
        treeview["show"] = ""  # Modificado para no mostrar los encabezados

        for column in df.columns:
            treeview.column(column, width=100)
            # La línea siguiente se omite para no establecer encabezados
            # treeview.heading(column, text=column)  # No se establece el texto del encabezado

        for index, row in df.iterrows():
            treeview.insert("", "end", values=list(row))  # Inserta los valores en la tabla

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)
        treeview.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        window.mainloop()

    def submit_form(self, textboxes):
        selected_number = self.section_sec.value if hasattr(self,
                                                            'section_sec') and self.section_sec is not None else ''
        values = {}
        for k, v in textboxes.items():
            if isinstance(v, CheckBox):
                # Si es un CheckBox, almacena 1 si está seleccionado, de lo contrario almacena ""
                values[f"{k}_{selected_number}" if selected_number else k] = '1' if v.value else ''
            else:
                values[f"{k}_{selected_number}" if selected_number else k] = v.get() if hasattr(v, 'get') else v
        unique_output_path = self.get_unique_output_path(INVOICE_OUTPUT_PATH)
        existing_data = self.load_data_from_file()
        existing_data.update(values)
        section = self.tabs_to_sections[self.tabs.value]
        self.history[section].append(values)  # Add the values to the history of the section
        with open(self.history_file_path, 'w') as f:
            json.dump(self.history, f)
        if not (self.save_data_to_file(existing_data)):
            self.app.error("Error", "An error occurred while saving the data.")
        Gui.write_fillable_pdf(INVOICE_TEMPLATE_PATH, unique_output_path, existing_data)
        '''for k, v in existing_data.items():
            print(f"{k}: {v}")'''
        self.app.info("Success", "Form submitted successfully.")

    def header_section(self):
        def process_social_security(*args):
            social_security_value = social_security_var.get()
            parts = social_security_value.split("-")
            if len(parts) == 3:
                self.textboxes_header["SOCIAL_FIRST_3"], self.textboxes_header["SOCAL_MIDDLE_2"], \
                    self.textboxes_header[
                        "SOCAL_LAST_4"] = parts

        self.data = self.load_data_from_file()
        self.header_box.bg = colors[0]
        Box(self.header_box,
            width=self.header_box.width,
            height=30,
            border=False,
            grid=[0, 0])
        Text(self.header_box,
             text="If you are still unemployed after eight weeks of benefits,\n"
                  "you should reduce your salary requirement\n"
                  "and look at more job openings.\n"
                  "Make as many copies of this as you need,\n"
                  "or print copies at\n"
                  "www.twc.texas.gov/worksearchlog",
             size=12,
             font="Times New Roman",
             color="red",
             align="top",
             grid=[0, 1])
        Box(self.header_box,
            width=self.header_box.width,
            height=10,
            border=False,
            grid=[0, 2])
        cont = Box(self.header_box,
                   width=400,
                   height=300,
                   border=True,
                   grid=[0, 3],
                   layout="grid")
        cont.bg = colors[3]
        self.textboxes_header = {"NAME": self.create_element(cont,
                                                             "Name:",
                                                             0),
                                 "WEEK": self.create_element(cont,
                                                             "Week of:",
                                                             2),
                                 "END_DATE": self.create_element(cont,
                                                                 "To:",
                                                                 4),
                                 "SOCIAL_FIRST_3": None,  # Preparar para almacenar la primera parte
                                 "SOCAL_MIDDLE_2": None,  # Preparar para almacenar la segunda parte
                                 "SOCAL_LAST_4": None,  # Preparar para almacenar la tercera parte
                                 "REQUIRED_NUMBER": self.create_element(cont,
                                                                        "Required Search #:",
                                                                        8),
                                 "RESULT_JOB_SEARCH": self.create_element(cont,
                                                                          "Result Job Search:",
                                                                          10)}

        social_security_var = self.create_element(cont, "Social Security #:", 6)
        # Llamar a process_social_security cada vez que el valor de social_security_var cambie
        social_security_var.trace("w", process_social_security)
        self.populate_textboxes(self.textboxes_header)
        Box(self.header_box,
            width=self.header_box.width,
            height=10,
            border=False,
            grid=[0, 4])
        PushButton(self.header_box,
                   text="Submit",
                   command=lambda: self.submit_form(self.textboxes_header),
                   grid=[0, 5],
                   align="bottom").tk.config(activebackground="green",
                                             activeforeground="white",
                                             borderwidth=7,
                                             cursor="hand2",
                                             fg="white",
                                             bg=colors[4],
                                             relief="ridge")
        Box(self.header_box,
            width=self.header_box.width,
            height=25,
            border=False,
            grid=[0, 6])
        PushButton(self.header_box,
                   text="History",
                   width=40,
                   height=0,
                   command=self.show_history,
                   grid=[0, 7],
                   align="top").tk.config(activebackground=colors[4],
                                          activeforeground="white",
                                          borderwidth=7,
                                          cursor="hand2",
                                          fg="white",
                                          bg=colors[5],
                                          relief="sunken")

    def description_section(self):
        self.data = self.load_data_from_file()
        self.description_box.bg = colors[0]
        Box(self.description_box,
            width=self.description_box.width,
            height=45,
            border=False,
            grid=[0, 0])
        Text(self.description_box,
             text="Applied for job, submitted resume, attended job fair,\n"
                  "interviewed, used Workforce Center, searched online, etc.",
             size=12,
             font="Times New Roman",
             color="red",
             align="top",
             grid=[0, 1])
        Box(self.description_box,
            width=self.description_box.width,
            height=50,
            border=False,
            grid=[0, 2])
        cont = Box(self.description_box,
                   width=400,
                   height=300,
                   border=True,
                   grid=[0, 3],
                   layout="grid")
        cont.bg = colors[3]
        self.textboxes_description = {"DATE_ACT": self.create_element(cont,
                                                                      "Date of Activity:",
                                                                      0),
                                      "WORK_SEARCH": self.create_element(cont,
                                                                         "Work Search Activity:",
                                                                         2),
                                      "JOB_TYPE": self.create_element(cont,
                                                                      "Type of Job:",
                                                                      4)}
        Text(cont,
             text="Select Form Section:",
             size=10,
             font="Arial",
             color="#FFCE51",
             grid=[0, 6],
             align="left")
        self.section_sec = Combo(cont,
                                 options=["1", "2", "3", "4", "5"],
                                 selected="",
                                 align="top",
                                 grid=[0, 7])
        self.section_sec.bg = "#C71585"
        self.populate_textboxes(self.textboxes_description)
        Text(cont,
             text="Options Section:",
             size=10,
             font="Arial",
             color="#FFCE51",
             grid=[1, 6, 1, 2],
             align="left")
        PushButton(cont,
                   text="Read",
                   command=lambda: self.update_textboxes(self.textboxes_description, self.section_sec.value),
                   grid=[1, 6],
                   align="right").tk.config(activebackground="green",
                                            activeforeground="white",
                                            borderwidth=2,
                                            cursor="hand2",
                                            fg="white",
                                            bg=colors[5],
                                            relief="sunken")
        PushButton(cont,
                   text="Erase",
                   command=lambda: self.clear_textboxes(self.textboxes_description, self.section_sec.value),
                   grid=[1, 7],
                   align="right").tk.config(activebackground="red",
                                            activeforeground="white",
                                            borderwidth=2,
                                            cursor="hand2",
                                            fg="white",
                                            bg=colors[5],
                                            relief="sunken")
        Box(self.description_box,
            width=self.description_box.width,
            height=10,
            border=False,
            grid=[0, 4])
        PushButton(self.description_box,
                   text="Submit",
                   command=lambda: self.submit_form(self.textboxes_description),
                   grid=[0, 5],
                   align="bottom").tk.config(activebackground="green",
                                             activeforeground="white",
                                             borderwidth=7,
                                             cursor="hand2",
                                             fg="white",
                                             bg=colors[4],
                                             relief="ridge")
        Box(self.description_box,
            width=self.description_box.width,
            height=25,
            border=False,
            grid=[0, 6])
        PushButton(self.description_box,
                   text="History",
                   width=40,
                   height=0,
                   command=self.show_history,
                   grid=[0, 7],
                   align="top").tk.config(activebackground=colors[4],
                                          activeforeground="white",
                                          borderwidth=7,
                                          cursor="hand2",
                                          fg="white",
                                          bg=colors[5],
                                          relief="sunken")

    def location_section(self):
        self.data = self.load_data_from_file()
        self.location_box.bg = colors[0]
        Box(self.location_box,
            width=self.location_box.width,
            height=10,
            border=False,
            grid=[0, 0])
        Text(self.location_box,
             text="Name, Location and Telephone Number of\n"
                  "Employer/Service/Agency\n"
                  "(For address, use street or Internet address)",
             size=12,
             font="Times New Roman",
             color="red",
             align="top",
             grid=[0, 1])
        Box(self.location_box,
            width=self.location_box.width,
            height=15,
            border=False,
            grid=[0, 2])
        cont = Box(self.location_box,
                   width=400,
                   height=300,
                   border=True,
                   grid=[0, 3],
                   layout="grid")
        cont.bg = colors[3]
        self.textboxes_location = {"ORG_NAME": self.create_element(cont,
                                                                   "Name:",
                                                                   0),
                                   "ORG_ADD": self.create_element(cont,
                                                                  "Address:",
                                                                  2),
                                   "C_S_Z": self.create_element(cont,
                                                                "City, Staate, Zip Code:",
                                                                4),
                                   "AREA_CODE": self.create_element(cont,
                                                                    "Area Code:",
                                                                    6),
                                   "PHONE_3_MIDDLE": self.create_element(cont,
                                                                         "Phone 3 first number:",
                                                                         8),
                                   "PHONE_4_LAST": self.create_element(cont,
                                                                       "Phone 4 last number:",
                                                                       10)}
        Text(cont,
             text="Select Form Section:",
             size=10,
             font="Arial",
             color="#FFCE51",
             grid=[0, 12],
             align="left")
        self.section_sec = Combo(cont,
                                 options=["1", "2", "3", "4", "5"],
                                 selected="",
                                 align="top",
                                 grid=[0, 13])
        self.section_sec.bg = "#C71585"
        self.populate_textboxes(self.textboxes_location)
        Text(cont,
             text="Options Section:",
             size=10,
             font="Arial",
             color="#FFCE51",
             grid=[1, 12, 1, 2],
             align="left")
        PushButton(cont,
                   text="Read",
                   command=lambda: self.update_textboxes(self.textboxes_location, self.section_sec.value),
                   grid=[1, 12],
                   align="right").tk.config(activebackground="green",
                                            activeforeground="white",
                                            borderwidth=2,
                                            cursor="hand2",
                                            fg="white",
                                            bg=colors[5],
                                            relief="sunken")
        PushButton(cont,
                   text="Erase",
                   command=lambda: self.clear_textboxes(self.textboxes_location, self.section_sec.value),
                   grid=[1, 13],
                   align="right").tk.config(activebackground="red",
                                            activeforeground="white",
                                            borderwidth=2,
                                            cursor="hand2",
                                            fg="white",
                                            bg=colors[5],
                                            relief="sunken")
        Box(self.location_box,
            width=self.location_box.width,
            height=10,
            border=False,
            grid=[0, 4])
        PushButton(self.location_box,
                   text="Submit",
                   command=lambda: self.submit_form(self.textboxes_location),
                   grid=[0, 5],
                   align="bottom").tk.config(activebackground="green",
                                             activeforeground="white",
                                             borderwidth=7,
                                             cursor="hand2",
                                             fg="white",
                                             bg=colors[4],
                                             relief="ridge")
        Box(self.location_box,
            width=self.location_box.width,
            height=10,
            border=False,
            grid=[0, 6])
        PushButton(self.location_box,
                   text="History",
                   width=40,
                   height=0,
                   command=self.show_history,
                   grid=[0, 7],
                   align="top").tk.config(activebackground=colors[4],
                                          activeforeground="white",
                                          borderwidth=7,
                                          cursor="hand2",
                                          fg="white",
                                          bg=colors[5],
                                          relief="sunken")

    def contact_section(self):
        self.data = self.load_data_from_file()
        self.contact_box.bg = colors[0]
        Box(self.contact_box,
            width=self.contact_box.width,
            height=10,
            border=False,
            grid=[0, 0])
        Text(self.contact_box,
             text="Contact Information\n"
                  "Complete all that apply",
             size=12,
             font="Times New Roman",
             color="red",
             align="top",
             grid=[0, 1])
        Box(self.contact_box,
            width=self.contact_box.width,
            height=15,
            border=False,
            grid=[0, 2])
        cont = Box(self.contact_box,
                   width=400,
                   height=300,
                   border=True,
                   grid=[0, 3],
                   layout="grid")
        cont.bg = colors[3]
        self.textboxes_contact = {"CONTACT_PERSON": self.create_element(cont,
                                                                        "Person Contacted:",
                                                                        0),
                                  "ORG_ADD": self.create_element(cont,
                                                                 "Mail:",
                                                                 2),
                                  "MAIL_ADD": self.create_element(cont,
                                                                  "Email:",
                                                                  4),
                                  "FAX_AREA_CODE": self.create_element(cont,
                                                                       "Fax Area Code:",
                                                                       6),
                                  "FAX_3_MIDDLE_NUMBER": self.create_element(cont,
                                                                             "Fax 3 Middle Number:",
                                                                             8),
                                  "FAX_4_LAST_NUMBER": self.create_element(cont,
                                                                           "Fax 4 Last Number:",
                                                                           10),
                                  "MAIL_CONTACT_CHECK": CheckBox(cont,
                                                                 text="By Mail",
                                                                 grid=[3, 2, 1, 2]),
                                  "MAIL_CONTACTED_CHECK": CheckBox(cont,
                                                                   text="By Email",
                                                                   grid=[3, 4, 1, 2]),
                                  "FAX_CONTACT_CHECK": CheckBox(cont,
                                                                text="By Fax",
                                                                grid=[3, 6, 1, 5])}
        self.textboxes_contact["MAIL_CONTACT_CHECK"].bg = "#C71585"
        self.textboxes_contact["MAIL_CONTACT_CHECK"].text_color = "white"
        self.textboxes_contact["MAIL_CONTACTED_CHECK"].bg = "#C71585"
        self.textboxes_contact["MAIL_CONTACTED_CHECK"].text_color = "white"
        self.textboxes_contact["FAX_CONTACT_CHECK"].bg = "#C71585"
        self.textboxes_contact["FAX_CONTACT_CHECK"].text_color = "white"
        Text(cont,
             text="Select Form Section:",
             size=10,
             font="Arial",
             color="#FFCE51",
             grid=[0, 13],
             align="left")
        self.section_sec = Combo(cont,
                                 options=["1", "2", "3", "4", "5"],
                                 selected="",
                                 align="top",
                                 grid=[0, 14])
        self.section_sec.bg = "#C71585"
        self.populate_textboxes(self.textboxes_contact)
        Text(cont,
             text="Options Section:",
             size=10,
             font="Arial",
             color="#FFCE51",
             grid=[1, 13, 1, 2],
             align="left")
        PushButton(cont,
                   text="Read",
                   command=lambda: self.update_textboxes(self.textboxes_contact, self.section_sec.value),
                   grid=[1, 13],
                   align="right").tk.config(activebackground="green",
                                            activeforeground="white",
                                            borderwidth=2,
                                            cursor="hand2",
                                            fg="white",
                                            bg=colors[5],
                                            relief="sunken")
        PushButton(cont,
                   text="Erase",
                   command=lambda: self.clear_textboxes(self.textboxes_contact, self.section_sec.value),
                   grid=[1, 14],
                   align="right").tk.config(activebackground="red",
                                            activeforeground="white",
                                            borderwidth=2,
                                            cursor="hand2",
                                            fg="white",
                                            bg=colors[5],
                                            relief="sunken")
        Box(self.contact_box,
            width=self.contact_box.width,
            height=10,
            border=False,
            grid=[0, 4])
        PushButton(self.contact_box,
                   text="Submit",
                   command=lambda: self.submit_form(self.textboxes_contact),
                   grid=[0, 5],
                   align="bottom").tk.config(activebackground="green",
                                             activeforeground="white",
                                             borderwidth=7,
                                             cursor="hand2",
                                             fg="white",
                                             bg=colors[4],
                                             relief="ridge")
        Box(self.contact_box,
            width=self.contact_box.width,
            height=20,
            border=False,
            grid=[0, 6])
        PushButton(self.contact_box,
                   text="History",
                   width=40,
                   height=0,
                   command=self.show_history,
                   grid=[0, 7],
                   align="top").tk.config(activebackground=colors[4],
                                          activeforeground="white",
                                          borderwidth=7,
                                          cursor="hand2",
                                          fg="white",
                                          bg=colors[5],
                                          relief="sunken")

    def results_section(self):
        self.data = self.load_data_from_file()
        self.results_box.bg = colors[0]
        Box(self.results_box,
            width=self.results_box.width,
            height=35,
            border=False,
            grid=[0, 0])
        Text(self.results_box,
             text="Results of Job Search",
             size=12,
             font="Times New Roman",
             color="red",
             align="top",
             grid=[0, 1])
        Box(self.results_box,
            width=self.results_box.width,
            height=40,
            border=False,
            grid=[0, 2])
        cont = Box(self.results_box,
                   width=400,
                   height=300,
                   border=True,
                   grid=[0, 3],
                   layout="grid")
        cont.bg = colors[3]
        self.textboxes_results = {"HIRED": CheckBox(cont,
                                                    text="Hired",
                                                    grid=[0, 0],
                                                    align="left"),
                                  "NOT_HIRED": CheckBox(cont,
                                                        text="Not Hired",
                                                        grid=[0, 1],
                                                        align="left"),
                                  "START_DATE_HIRED": self.create_element(cont,
                                                                          "Start Date:",
                                                                          3),
                                  "CHECK_APPLICATION_FILL": CheckBox(cont,
                                                                     text="Application Fill",
                                                                     grid=[1, 0],
                                                                     align="left"),
                                  "CHECK_OTHER": CheckBox(cont,
                                                          text="Other",
                                                          grid=[1, 1],
                                                          align="left"),
                                  "OTHER_JOB_RES": self.create_element(cont,
                                                                       "Other Job Results:",
                                                                       4)}
        self.textboxes_results["HIRED"].bg = "#C71585"
        self.textboxes_results["HIRED"].text_color = "white"
        self.textboxes_results["NOT_HIRED"].bg = "#C71585"
        self.textboxes_results["NOT_HIRED"].text_color = "white"
        self.textboxes_results["CHECK_APPLICATION_FILL"].bg = "#C71585"
        self.textboxes_results["CHECK_APPLICATION_FILL"].text_color = "white"
        self.textboxes_results["CHECK_OTHER"].bg = "#C71585"
        self.textboxes_results["CHECK_OTHER"].text_color = "white"
        Text(cont,
             text="Select Form Section:",
             size=10,
             font="Arial",
             color="#FFCE51",
             grid=[0, 6],
             align="left")
        self.section_sec = Combo(cont,
                                 options=["1", "2", "3", "4", "5"],
                                 selected="",
                                 align="top",
                                 grid=[0, 7])
        self.section_sec.bg = "#C71585"
        self.populate_textboxes(self.textboxes_results)
        Text(cont,
             text="Options Section:",
             size=10,
             font="Arial",
             color="#FFCE51",
             grid=[1, 6, 1, 2],
             align="left")
        PushButton(cont,
                   text="Read",
                   command=lambda: self.update_textboxes(self.textboxes_results, self.section_sec.value),
                   grid=[1, 6],
                   align="right").tk.config(activebackground="green",
                                            activeforeground="white",
                                            borderwidth=2,
                                            cursor="hand2",
                                            fg="white",
                                            bg=colors[5],
                                            relief="sunken")
        PushButton(cont,
                   text="Erase",
                   command=lambda: self.clear_textboxes(self.textboxes_results, self.section_sec.value),
                   grid=[1, 7],
                   align="right").tk.config(activebackground="red",
                                            activeforeground="white",
                                            borderwidth=2,
                                            cursor="hand2",
                                            fg="white",
                                            bg=colors[5],
                                            relief="sunken")
        Box(self.results_box,
            width=self.results_box.width,
            height=10,
            border=False,
            grid=[0, 13])
        PushButton(self.results_box,
                   text="Submit",
                   command=lambda: self.submit_form(self.textboxes_results),
                   grid=[0, 14],
                   align="bottom").tk.config(activebackground="green",
                                             activeforeground="white",
                                             borderwidth=7,
                                             cursor="hand2",
                                             fg="white",
                                             bg=colors[4],
                                             relief="ridge")
        Box(self.results_box,
            width=self.results_box.width,
            height=35,
            border=False,
            grid=[0, 15])
        PushButton(self.results_box,
                   text="History",
                   width=40,
                   height=0,
                   command=self.show_history,
                   grid=[0, 16],
                   align="top").tk.config(activebackground=colors[4],
                                          activeforeground="white",
                                          borderwidth=7,
                                          cursor="hand2",
                                          fg="white",
                                          bg=colors[5],
                                          relief="sunken")

    def do_this_when_closed(self):
        if self.app.yesno("Close", "Do you want to quit?"):
            self.app.destroy()


if __name__ == "__main__":
    Gui()
