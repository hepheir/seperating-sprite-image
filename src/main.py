import os

from tkinter import Button, Frame, Label, Spinbox, StringVar, Tk, filedialog
from PIL import Image


class App(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.image_filename = StringVar()
        self.columns = StringVar(value=0)
        self.rows = StringVar(value=0)
        self.add_widgets()

    def add_widgets(self):
        Label(self, text="Columns: ")\
            .grid(row=1, column=0)
        Spinbox(self, increment=1, textvariable=self.columns)\
            .grid(row=1, column=1)
        Label(self, text="Rows: ")\
            .grid(row=2, column=0)
        Spinbox(self, increment=1, textvariable=self.rows)\
            .grid(row=2, column=1)
        Button(self, text="Open Image", command=self.open_image)\
            .grid(row=3, column=0)
        Button(self, text="Process Image", command=self.process_image)\
            .grid(row=3, column=1)

    def open_image(self):
        options = {
            'filetypes': [('Image files', ['*.webp', '*.jpg', '*.jpeg', '*.png', '*.gif'])],
        }
        filename = filedialog.askopenfilename(**options)
        self.image_filename.set(filename)
        self.show_image()

    def show_image(self):
        with Image.open(self.image_filename.get()) as image:
            image.show()

    def process_image(self):
        if not self.image_filename.get():
            return
        basename, extension = os.path.splitext(
            filedialog.asksaveasfilename(defaultextension='png'))
        with Image.open(self.image_filename.get()) as image:
            for x in range(int(self.columns.get())):
                for y in range(int(self.rows.get())):
                    image.crop(self.create_box(image, x, y)).save(
                        f'{basename}-{x}-{y}{extension}')

    def create_box(self, image: Image.Image, x: int, y: int) -> tuple[int, int, int, int]:
        sprite_width = image.width / int(self.columns.get())
        sprite_height = image.height / int(self.rows.get())
        left = sprite_width * x
        up = sprite_height * y
        right = left + sprite_width
        down = up + sprite_height
        return (left, up, right, down)


def main():
    window: Tk = Tk()
    window.title("Sperating Sprite Image")
    window.resizable(width=False, height=False)
    app = App(window)
    app.mainloop()


if __name__ == "__main__":
    main()
