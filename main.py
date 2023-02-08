import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import uuid
import matplotlib.colors as colors


# TODO comment code
# TODO add error/invalid input handling


# The selected font is default for mac and will (probably) not work with windows


class WaterMarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WaterMarker")
        self.minsize(width=300, height=100)
        self.configure(padx=20, pady=20)

        self.canvas = None
        self.image_container = None
        self.options_frame = None

        self.image = None
        self.output_image = None
        self.output_photo_image = None
        self.resized_image = None
        self.photo_image = None
        self.select_image_button = None
        self.quit_button = None

        self.THUMBNAIL_WIDTH = 400
        self.THUMBNAIL_HEIGHT = 400

        self.water_mark_text = None
        self.x_pos = None
        self.y_pos = None
        self.size = None
        self.alpha_value = None
        self.color = None
        self.rotation_value = None

        self.create_initial_widgets()

    def create_initial_widgets(self):
        self.select_image_button = ttk.Button(text="Select Image", command=self.get_image)
        self.select_image_button.grid(column=0, row=0)

        self.quit_button = ttk.Button(text="Quit", command=exit)
        self.quit_button.grid(column=0, row=1)

    def get_image(self):
        image_path = tkinter.filedialog.askopenfilename()
        self.image = Image.open(image_path).convert("RGBA")
        self.resized_image = self.image
        self.resized_image.thumbnail((self.THUMBNAIL_WIDTH, self.THUMBNAIL_HEIGHT))
        self.photo_image = ImageTk.PhotoImage(self.resized_image)

        self.edit_image()

    def edit_image(self):
        self.select_image_button.grid_forget()
        self.quit_button.grid_forget()

        self.canvas = tk.Canvas(width=self.THUMBNAIL_WIDTH, height=self.THUMBNAIL_HEIGHT)
        self.image_container = self.canvas.create_image(self.THUMBNAIL_WIDTH / 2, self.THUMBNAIL_HEIGHT / 2,
                                                        image=self.photo_image)
        self.canvas.grid(column=0, row=0)

        self.options()

    def options(self):
        self.water_mark_text = tk.StringVar()
        self.x_pos = tk.IntVar()
        self.y_pos = tk.IntVar()
        self.size = tk.IntVar()
        self.alpha_value = tk.DoubleVar()
        self.color = tk.StringVar()
        self.rotation_value = tk.IntVar()

        self.options_frame = ttk.LabelFrame(text="Water Mark Options", labelanchor="n")
        text_label = ttk.Label(master=self.options_frame, text="Water Mark")
        text_entry = ttk.Entry(master=self.options_frame, textvariable=self.water_mark_text)
        x_position_label = ttk.Label(master=self.options_frame, text="X position")
        x_position_entry = ttk.Entry(master=self.options_frame, textvariable=self.x_pos)
        y_position_label = ttk.Label(master=self.options_frame, text="Y position")
        y_position_entry = ttk.Entry(master=self.options_frame, textvariable=self.y_pos)
        size_label = ttk.Label(master=self.options_frame, text="Size")
        size_entry = ttk.Entry(master=self.options_frame, textvariable=self.size)
        opacity_label = ttk.Label(master=self.options_frame, text="Opacity (0 - 1)")
        opacity_entry = ttk.Entry(master=self.options_frame, textvariable=self.alpha_value)
        color_label = ttk.Label(master=self.options_frame, text="Color Hex Code")
        color_entry = ttk.Entry(master=self.options_frame, textvariable=self.color)
        rotation_label = ttk.Label(master= self.options_frame, text="Rotation")
        rotation_entry = ttk.Entry(master=self.options_frame, textvariable=self.rotation_value)
        add_button = ttk.Button(master=self.options_frame, text="Add", command=self.add_watermark)
        save_button = ttk.Button(master=self.options_frame, text="Save", command=self.save)

        self.options_frame.grid(column=1, row=0)
        text_label.grid(column=0, row=0)
        text_entry.grid(column=0, row=1)
        x_position_label.grid(column=0, row=2)
        x_position_entry.grid(column=0, row=3)
        y_position_label.grid(column=0, row=4)
        y_position_entry.grid(column=0, row=5)
        size_label.grid(column=0, row=6)
        size_entry.grid(column=0, row=7)
        opacity_label.grid(column=0, row=8)
        opacity_entry.grid(column=0, row=9)
        color_label.grid(column=0, row=10)
        color_entry.grid(column=0, row=11)
        rotation_label.grid(column=0, row=12)
        rotation_entry.grid(column=0, row=13)
        add_button.grid(column=0, row=14)
        save_button.grid(column=0, row=15)

    def add_watermark(self):
        color_tuple = colors.hex2color(self.color.get())
        water_mark = Image.new("RGBA", self.image.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(water_mark)
        # TODO create an options menu for to select the font installed on a users computer instead of hardcode for mac
        font = ImageFont.truetype("Arial Unicode.ttf", size=self.size.get())
        d.text((self.x_pos.get(),
                self.y_pos.get()),
               self.water_mark_text.get(),
               fill=(
                   int(color_tuple[0]*255),
                   int(color_tuple[1]*255),
                   int(color_tuple[2]*255),
                   int(self.alpha_value.get() * 255)),
               font=font)

        self.output_image = Image.alpha_composite(self.image, water_mark.rotate(self.rotation_value.get()))

        self.update_preview_image()

    def update_preview_image(self):
        self.output_photo_image = ImageTk.PhotoImage(self.output_image)
        self.canvas.itemconfig(self.image_container, image=self.output_photo_image)

    def save(self):
        self.output_image.save(f"img{uuid.uuid4()}.png", "PNG")
        self.restart()

    def restart(self):
        self.canvas.grid_forget()
        self.options_frame.grid_forget()

        self.create_initial_widgets()


root = WaterMarkApp()
root.mainloop()
