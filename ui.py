import tkinter as tk

class MovingSquare:
    def __init__(self, canvas, start_x, start_y, end_x, color, moving_squares, size=50):
        self.canvas = canvas
        self.size = size
        self.x = start_x
        self.y = start_y
        self.end_x = end_x - 30 - size
        self.color = color
        self.square = canvas.create_rectangle(self.x, self.y, self.x + size, self.y + size, fill=color)
        self.moving = True
        self.moving_squares = moving_squares
        self.move_square()

    def move_square(self):
        if self.moving:
            # Check if there's any square to the right blocking the path
            can_move = True
            for square in self.moving_squares:
                if square != self and square.x < self.x + self.size + 5 < square.x + square.size and self.y == square.y:
                    can_move = False
                    break

            if can_move and self.x < self.end_x:
                self.x += 5
                self.canvas.coords(self.square, self.x, self.y, self.x + self.size, self.y + self.size)
            elif self.x >= self.end_x:
                self.canvas.itemconfig(self.square, fill="green")
                self.canvas.after(1000, self.remove_square)
            self.canvas.after(5, self.move_square)

    def remove_square(self):
        self.moving = False
        self.canvas.delete(self.square)
        self.moving_squares.remove(self)


class ui:
    def __init__(self):

        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Simulación de Biblioteca")
        self.root.geometry("800x600")  # Tamaño de la ventana

        # Crear un lienzo para dibujar
        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.canvas.pack()

        # Parámetros del cuadrado azul
        canvas_width = 800
        canvas_height = 600
        blue_square_size = 50  # Tamaño del cuadrado azul
        self.blue_square_x = canvas_width - blue_square_size  # Posición X del cuadrado azul en el borde derecho
        blue_square_y = (canvas_height / 3) - (blue_square_size / 2)  # Posición Y del cuadrado azul en el centro

        # Crear el cuadrado azul
        self.canvas.create_rectangle(self.blue_square_x, blue_square_y, self.blue_square_x + blue_square_size, blue_square_y + blue_square_size, fill="blue")

        # Parámetros del cuadrado rojo
        red_square_size = 50  # Tamaño del cuadrado rojo
        self.red_square_y = (canvas_height / 3) - (red_square_size / 2)  # Posición Y del cuadrado rojo en el centro

        # Lista para almacenar los cuadrados rojos en movimiento
        self.moving_squares = []

    def main(self):
        # Ejecutar la aplicación
        self.root.mainloop()

    def add_red_square(self):
        new_square = MovingSquare(self.canvas, 0, self.red_square_y, self.blue_square_x, "red", self.moving_squares)
        self.moving_squares.append(new_square)
