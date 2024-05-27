import tkinter as tk

class MovingSquare:
    def __init__(self, canvas, start_x, start_y, end_x, color, size=50):
        self.canvas = canvas
        self.size = size
        self.x = start_x
        self.y = start_y
        self.end_x = end_x - 30 - size
        self.color = color
        self.square = canvas.create_rectangle(self.x, self.y, self.x + size, self.y + size, fill=color)
        self.moving = True
        self.move_square()

    def move_square(self):
        if self.moving:
            # Check if there's any square to the right blocking the path
            can_move = True
            for square in moving_squares:
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
        moving_squares.remove(self)

def add_red_square():
    new_square = MovingSquare(canvas, 0, red_square_y, blue_square_x, "red")
    moving_squares.append(new_square)

# Crear la ventana principal
root = tk.Tk()
root.title("Simulación de Biblioteca")
root.geometry("800x600")  # Tamaño de la ventana

# Crear un lienzo para dibujar
canvas = tk.Canvas(root, width=800, height=500)
canvas.pack()

# Parámetros del cuadrado azul
canvas_width = 800
canvas_height = 600
blue_square_size = 50  # Tamaño del cuadrado azul
blue_square_x = canvas_width - blue_square_size  # Posición X del cuadrado azul en el borde derecho
blue_square_y = (canvas_height / 3) - (blue_square_size / 2)  # Posición Y del cuadrado azul en el centro

# Crear el cuadrado azul
canvas.create_rectangle(blue_square_x, blue_square_y, blue_square_x + blue_square_size, blue_square_y + blue_square_size, fill="blue")

# Parámetros del cuadrado rojo
red_square_size = 50  # Tamaño del cuadrado rojo
red_square_y = (canvas_height / 3) - (red_square_size / 2)  # Posición Y del cuadrado rojo en el centro

# Lista para almacenar los cuadrados rojos en movimiento
moving_squares = []

# Botón para agregar cuadrados rojos
add_button = tk.Button(root, text="Agregar Cuadro Rojo", command=add_red_square)
add_button.pack()

# Ejecutar la aplicación
root.mainloop()
