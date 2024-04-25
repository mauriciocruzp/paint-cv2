import tkinter as tk
from tkinter import filedialog
import numpy as np
import cv2
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename


class BottonFrame(tk.Frame):
    def __init__(self, master, canvas, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.canvas = canvas
        self.create_buttons()

    def create_buttons(self):
        modes = [
            ("Linea recta"),
            ("Polilinea"),
            ("Rectangulo"),
            ("Circulo"),
            ("Borrar"),
        ]

        for i, (mode) in enumerate(modes):
            if mode:
                button = tk.Button(
                    self, text=mode, command=lambda m=mode: self.canvas.set_draw_mode(m)
                )
            button.grid(row=i, column=0, padx=5, pady=5)
        button = tk.Button(self, text="Cambiar color", command=self.canvas.change_color)
        button.grid(row=5, column=0, padx=5, pady=5)
        button = tk.Button(self, text="Guardar", command=self.canvas.save)
        button.grid(row=6, column=0, padx=5, pady=5)


class Canvas(tk.Canvas):
    colors = ["black", "purple", "red", "green", "blue", "yellow", "magenta", "cyan"]
    selected_color = "purple"

    def __init__(self, master, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.mode = "Polilinea"
        self.coordinates = None
        self.bind("<Button-1>", self.start_draw)
        self.bind("<B1-Motion>", self.draw_figure)
        self.bind("<ButtonRelease-1>", self.save_figure)
        self.init_canvas()

    def init_canvas(self):
        frame = np.zeros((600, 800, 3), dtype=np.uint8)
        frame[:, :] = (255, 255, 255)
        image = Image.fromarray(frame)
        image = ImageTk.PhotoImage(image)

        self.canvas_opencv = frame.copy()
        self.create_image(0, 0, image=image, anchor=tk.NW)

    def set_draw_mode(self, mode):
        self.mode = mode

    def start_draw(self, event):
        self.coordinates = [event.x, event.y]

    def draw_figure(self, event):
        if self.coordinates:
            if self.mode == "Polilinea":
                self.draw_poliline(event)
            elif self.mode == "Linea recta":
                self.draw_line(event)
            elif self.mode == "Circulo":
                self.draw_circle(event)
            elif self.mode == "Rectangulo":
                self.draw_rectangle(event)
            elif self.mode == "Borrar":
                self.erase(event)

    def draw_poliline(self, event):
        x, y = event.x, event.y
        self.create_line(
            self.coordinates[0],
            self.coordinates[1],
            x,
            y,
            fill=self.selected_color,
            width=2,
        )
        cv2.line(
            self.canvas_opencv,
            (self.coordinates[0], self.coordinates[1]),
            (x, y),
            (0, 0, 0),
            2,
        )
        self.coordinates = [x, y]

    def draw_line(self, event):
        x, y = event.x, event.y
        self.delete("line-temporal")
        self.create_line(
            self.coordinates[0],
            self.coordinates[1],
            x,
            y,
            fill=self.selected_color,
            width=2,
            tags="line-temporal",
        )

    def draw_circle(self, event):
        x, y = event.x, event.y
        self.delete("circle-temporal")
        self.create_oval(
            self.coordinates[0],
            self.coordinates[1],
            x,
            y,
            outline=self.selected_color,
            width=2,
            tags="circle-temporal",
        )

    def draw_rectangle(self, event):
        x, y = event.x, event.y
        self.delete("rectangle-temporal")
        self.create_rectangle(
            self.coordinates[0],
            self.coordinates[1],
            x,
            y,
            outline=self.selected_color,
            width=2,
            tags="rectangle-temporal",
        )

    def erase(self, event):
        x, y = event.x, event.y
        self.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill="white", outline="white")
        cv2.circle(self.canvas_opencv, (x, y), 5, (255, 255, 255), -1)

    def save(self):
        file_path = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        )
        if file_path:
            cv2.imwrite(file_path, self.canvas_opencv)

    def change_color(self):
        self.color_index = self.colors.index(self.selected_color)
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.selected_color = self.colors[self.color_index]

    def save_figure(self, event):
        if self.mode == "Linea recta":
            x, y = event.x, event.y
            self.delete("line-temporal")
            self.create_line(
                self.coordinates[0],
                self.coordinates[1],
                x,
                y,
                fill=self.selected_color,
                width=2,
            )
            cv2.line(
                self.canvas_opencv,
                (self.coordinates[0], self.coordinates[1]),
                (x, y),
                (0, 0, 0),
                2,
            )
        elif self.mode == "Rectangulo":
            x, y = event.x, event.y
            self.delete("rectangle-temporal")
            self.create_rectangle(
                self.coordinates[0],
                self.coordinates[1],
                x,
                y,
                outline=self.selected_color,
                width=2,
            )
            cv2.rectangle(
                self.canvas_opencv,
                (self.coordinates[0], self.coordinates[1]),
                (x, y),
                (0, 0, 0),
                2,
            )
        elif self.mode == "Circulo":
            x, y = event.x, event.y
            self.delete("circle-temporal")
            self.create_oval(
                self.coordinates[0],
                self.coordinates[1],
                x,
                y,
                outline=self.selected_color,
                width=2,
            )
            cv2.circle(
                self.canvas_opencv,
                (self.coordinates[0], self.coordinates[1]),
                int(
                    np.sqrt(
                        (x - self.coordinates[0]) ** 2 + (y - self.coordinates[1]) ** 2
                    )
                ),
                (0, 0, 0),
                2,
            )
