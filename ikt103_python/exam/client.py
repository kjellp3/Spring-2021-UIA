from view.frontend import Interface, center
from PIL import Image, ImageTk
from tkinter import Tk
import os
root = Tk()


def main():
    app = Interface(root)

    icon = ImageTk.PhotoImage(Image.open(f'{os.path.realpath(__file__).replace("client.py","")}\\view\\car.png'))
    app.master.iconphoto(False, icon)
    app.master.title("Car rental interface")
    app.master.minsize(1200, 800)
    center(root)

    app.mainloop()


if __name__ == '__main__':
    main()
