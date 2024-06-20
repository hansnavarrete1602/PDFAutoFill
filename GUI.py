from guizero import App, Box, Text, PushButton, TextBox, Picture, ButtonGroup

colors = ['#27272A',
          '#202020',
          '#05111D',
          '#111828']

tab_opt = [["Header", "1"],
           ["Description", "2"],
           ["Location", "3"],
           ["Contact", "4"],
           ["Results", "5"]]


class Gui:

    def __init__(self):
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
        Box(self.content_box,
            width=self.content_box.width,
            height=int((self.content_box.height / 10) / 2),
            border=False,
            grid=[0, 0])
        self.main_box = Box(self.content_box,
                            width=self.content_box.width,
                            height=int(self.content_box.height / 10) * 9,
                            border=True,
                            grid=[0, 1])
        self.main_box.bg = colors[3]
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
             text="Select a tab\nto fill content:",
             size=10,
             font="Arial Black",
             color="#C71585",
             align="top",
             grid=[0, 0, 1, 2])
        self.tabs = ButtonGroup(self.tabs_box_content,
                                options=tab_opt,
                                selected="1",
                                horizontal=False,
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

    def display(self):
        self.app.display()


if __name__ == "__main__":
    Gui()

