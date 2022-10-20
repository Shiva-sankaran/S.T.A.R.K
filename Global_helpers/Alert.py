from tkinter import *
from PIL import ImageTk, Image
import time

def callback(event):
    webbrowser.open_new(event.widget.cget("text"))

def alert_popup(title, message, image_path,link = None):
    """Generate a pop-up window for special messages."""
    root = Tk()
    root.title(title)

    w = 400     # popup window width
    h = 500     # popup window height

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    x = sw
    y = 0
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    m = message
    m += '\n'
    

    
    img = ImageTk.PhotoImage(Image.open(image_path))
    panel = Label(root, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    w = Label(root, text=m, width=120, height=10)
    w.pack()
    b = Button(root, text="OK", command=root.destroy, width=10)
    b.pack()
    lbl = Label(root, text=link, fg="blue", cursor="hand2")
    lbl.pack()
    lbl.bind("<Button-1>", callback)
    
    mainloop()


# Examples


#alert_popup("Success!", "Processing completed. Your report was saved here:", "/home/shivasankaran/STARK/res/images/water/3.jpeg","http://www.gmail.com")