import tkinter as tk
from tkinter import ttk
from guizero import App, Box, Text, PushButton, TextBox, Picture, ButtonGroup, Combo

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


class Gui:

    def __init__(self):
        self.combos = None
        self.textboxes = None
        self.tabs = None
        self.app = App(title="PDF AutoFiller",
                       width=800, height=600,
                       layout="grid",
                       bg=colors[1])
        self.box_header = Box(self.app,
                              width=self.app.width,
                              height=50,
                              border=False,
                              grid=[0, 0])
        self.box_header.bg = colors[1]
        Text(self.box_header,
             text="PDF AutoFiller",
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
                            height=int(self.app.height) - 100,
                            border=False,
                            grid=[0, 2],
                            layout="grid")
        self.box_body.bg = colors[2]
        Box(self.box_body,
            width=int((int(self.box_body.width) / 10) * 1.5),
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
            width=int((int(self.box_body.width) / 10) / 2),
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
            width=int((int(self.box_body.width) / 10) * 1.5),
            height=self.box_body.height,
            border=False,
            grid=[4, 0])
        self.tabs_menu()
        self.display()

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

    def header_section(self):
        @staticmethod
        def submit_form():
            values = {k: v.get() for k, v in self.textboxes.items()}
            for k, v in values.items():
                print(f"{k}: {v}")
            self.app.info("Success", "Form submitted successfully.")

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
        self.textboxes = {"NAME": self.create_element(cont,
                                                      "Name:",
                                                      0),
                          "WEEK": self.create_element(cont,
                                                      "Week of:",
                                                      2),
                          "END_DATE": self.create_element(cont,
                                                          "To:",
                                                          4),
                          "Social Security #": self.create_element(cont,
                                                                   "Social Security #:",
                                                                   6),
                          "REQUIRED_NUMBER": self.create_element(cont,
                                                                 "Required Search #:",
                                                                 8),
                          "RESULT_JOB_SEARCH": self.create_element(cont,
                                                                   "Result Job Search:",
                                                                   10)}
        Box(self.header_box,
            width=self.header_box.width,
            height=10,
            border=False,
            grid=[0, 4])
        PushButton(self.header_box,
                   text="Submit",
                   command=submit_form,
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
                   command=None,
                   grid=[0, 7],
                   align="top").tk.config(activebackground=colors[4],
                                          activeforeground="white",
                                          borderwidth=7,
                                          cursor="hand2",
                                          fg="white",
                                          bg=colors[5],
                                          relief="sunken")

    def description_section(self):
        self.description_box.bg = colors[0]
        pass

    def location_section(self):
        self.location_box.bg = colors[0]
        pass

    def contact_section(self):
        self.contact_box.bg = colors[0]
        pass

    def results_section(self):
        self.results_box.bg = colors[0]
        pass

    def do_this_when_closed(self):
        if self.app.yesno("Close", "Do you want to quit?"):
            self.app.destroy()

    def display(self):
        self.app.when_closed = self.do_this_when_closed
        self.app.display()


if __name__ == "__main__":
    Gui()
