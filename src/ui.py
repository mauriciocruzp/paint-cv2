import tkinter

from src.canvas import BottonFrame, Canvas


def run():
    window = tkinter.Tk()
    window.title("Paint CV2")
    window.geometry("900x700")

    canvas = Canvas(window, bg="white")
    canvas.pack(fill=tkinter.BOTH, expand=True)

    botton_frame = BottonFrame(window, canvas)


    def move_frame(event):
        x, y = event.x, event.y
        botton_frame.place_configure(x=x, y=y)


    botton_frame.place(x=50, y=300)
    botton_frame.bind("<B1-Motion>", move_frame)

    window.mainloop()
