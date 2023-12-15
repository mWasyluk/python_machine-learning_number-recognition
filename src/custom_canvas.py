from tkinter import Canvas
from PIL import Image
import io

class CustomCanvas(Canvas):
    global width, height
    width, height = 64, 64

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_rectangle(0, 0, width, height, fill='white', outline='white')
        self.bind('<Button-1>', self.click)
        self.bind('<B1-Motion>', self.move)
        self.last_x, self.last_y = None, None

    def reset_canvas(self, event):
        self.delete("all")
        self.create_rectangle(0, 0, 64, 64, fill='white', outline='white')
    
    def click(self, event):
        global prev
        prev, x, y = event, event.x, event.y
        self.create_oval(x - 1, y + 1, x + 1, y - 1, width=2)

    def move(self, event):
        global prev
        self.create_line(prev.x, prev.y, event.x, event.y, width=4, capstyle='round', smooth=True)
        prev = event  
    
    def toImage(self):
        image = self.postscript(colormode='color', pageheight=width-1, pagewidth=height-1)
        image = Image.open(io.BytesIO(image.encode('utf-8')))
        return image
