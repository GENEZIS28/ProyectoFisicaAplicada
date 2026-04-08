import tkinter as tk
from tkinter import messagebox
import math
import matplotlib.pyplot as plt

# Constante de Coulomb
k = 9 * 10**9

# Lista donde se almacenan las cargas (q, x, y)
cargas = []

# Colores de la interfaz
FONDO = "#3A3A3A"
BOTON = "#000080"
TEXTO = "white"
CAJA = "#4A4A4A"

# ---------------- FUNCIONES ---------------- #

def actualizar_contador():
    """Actualiza el número de cargas ingresadas."""
    contador.set(f"Cargas ingresadas: {len(cargas)}")


def agregar_carga():
    """
    Agrega una carga a la lista interna y a la lista visual.
    """
    try:
        q = float(entry_q.get())
        x = float(entry_x.get())
        y = float(entry_y.get())

        cargas.append((q, x, y))
        lista_cargas.insert(tk.END, f"q={q} C, x={x}, y={y}")

        actualizar_contador()

        # Limpiar campos
        entry_q.delete(0, tk.END)
        entry_x.delete(0, tk.END)
        entry_y.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Ingrese valores numéricos válidos")


def eliminar_carga():
    """
    Elimina la carga seleccionada de la lista visual
    y de la lista interna.
    """
    seleccion = lista_cargas.curselection()

    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione una carga para eliminar")
        return

    index = seleccion[0]

    lista_cargas.delete(index)
    cargas.pop(index)

    actualizar_contador()


def limpiar_todo():
    """
    Elimina todas las cargas ingresadas.
    """
    lista_cargas.delete(0, tk.END)
    cargas.clear()
    actualizar_contador()


def calcular():
    """
    Calcula la fuerza neta sobre la carga objetivo
    usando la Ley de Coulomb y muestra el procedimiento.
    """
    try:
        if not cargas:
            messagebox.showwarning("Advertencia", "Debe ingresar al menos una carga")
            return

        q_obj = float(entry_q_obj.get())
        x_obj = float(entry_x_obj.get())
        y_obj = float(entry_y_obj.get())

        Fx_total = 0
        Fy_total = 0
        procedimiento = ""

        for i, (q, x, y) in enumerate(cargas):

            # Diferencias en coordenadas
            dx = x_obj - x
            dy = y_obj - y

            # Distancia al cuadrado
            r2 = dx**2 + dy**2

            # Distancia
            r = math.sqrt(r2)

            if r == 0:
                messagebox.showerror("Error", "Dos cargas en la misma posición")
                return

            # Ley de Coulomb
            F = k * (q * q_obj) / r2

            # Componentes de la fuerza
            Fx = F * (dx / r)
            Fy = F * (dy / r)

            # Suma de fuerzas (superposición)
            Fx_total += Fx
            Fy_total += Fy

            # Procedimiento detallado
            procedimiento += f"""
Carga {i+1}:
dx = {dx:.2f}, dy = {dy:.2f}
r² = {r2:.2f}
r = {r:.2f}
F = {F:.2e}
Fx = {Fx:.2e}, Fy = {Fy:.2e}
-----------------------
"""

        # Magnitud de la fuerza total
        F_total = math.sqrt(Fx_total**2 + Fy_total**2)

        resultado.set(f"Fuerza: <{Fx_total:.2e}, {Fy_total:.2e}> N | Magnitud: {F_total:.2e} N")

        # Mostrar procedimiento
        text_procedimiento.delete("1.0", tk.END)
        text_procedimiento.insert(tk.END, procedimiento)

    except ValueError:
        messagebox.showerror("Error", "Datos inválidos")


def ver_plano():
    """
    Muestra el plano cartesiano con:
    - Cargas positivas (rojo)
    - Cargas negativas (azul)
    - Carga objetivo (verde)
    """
    if not cargas:
        messagebox.showwarning("Advertencia", "No hay cargas para graficar")
        return

    try:
        x_obj = float(entry_x_obj.get())
        y_obj = float(entry_y_obj.get())

        plt.figure()
        ax = plt.gca()

        # Dibujar cargas
        for i, (q, x, y) in enumerate(cargas):
            color = "red" if q > 0 else "blue"
            ax.scatter(x, y, color=color, s=80)
            ax.text(x, y, f"q{i+1}")

        # Dibujar carga objetivo
        ax.scatter(x_obj, y_obj, color="green", s=100)
        ax.text(x_obj, y_obj, "Objetivo")

        # Ejes
        ax.axhline(0)
        ax.axvline(0)
        ax.set_title("Plano Cartesiano")
        ax.grid()

        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Datos inválidos")


# ---------------- INTERFAZ ---------------- #

ventana = tk.Tk()
ventana.title("Ley de Coulomb")
ventana.geometry("600x700")
ventana.configure(bg=FONDO)

tk.Label(ventana, text="Calculadora Ley de Coulomb",
         bg=FONDO, fg=TEXTO, font=("Arial", 14)).pack(pady=5)

# CARGAS
tk.Label(ventana, text="Cargas", bg=FONDO,
         fg="cyan", font=("Arial", 12)).pack(pady=5)

frame_carga = tk.Frame(ventana, bg=FONDO)
frame_carga.pack(pady=5)

tk.Label(frame_carga, text="Magnitud:", bg=FONDO, fg=TEXTO).grid(row=0, column=0)
entry_q = tk.Entry(frame_carga, width=10, bg=CAJA, fg="white", insertbackground="white")
entry_q.grid(row=0, column=1, padx=5)

tk.Label(frame_carga, text="X:", bg=FONDO, fg=TEXTO).grid(row=0, column=2)
entry_x = tk.Entry(frame_carga, width=10, bg=CAJA, fg="white", insertbackground="white")
entry_x.grid(row=0, column=3, padx=5)

tk.Label(frame_carga, text="Y:", bg=FONDO, fg=TEXTO).grid(row=0, column=4)
entry_y = tk.Entry(frame_carga, width=10, bg=CAJA, fg="white", insertbackground="white")
entry_y.grid(row=0, column=5, padx=5)

tk.Button(ventana, text="Agregar carga",
          bg=BOTON, fg="white", command=agregar_carga).pack(pady=5)

tk.Button(ventana, text="Eliminar carga",
          bg=BOTON, fg="white", command=eliminar_carga).pack(pady=5)

tk.Button(ventana, text="Limpiar todo",
          bg=BOTON, fg="white", command=limpiar_todo).pack(pady=5)

contador = tk.StringVar()
contador.set("Cargas ingresadas: 0")
tk.Label(ventana, textvariable=contador, bg=FONDO, fg="cyan").pack()

lista_cargas = tk.Listbox(ventana, height=5, bg=CAJA, fg="white")
lista_cargas.pack(fill=tk.BOTH, padx=10, pady=5)

# CARGA OBJETIVO
tk.Label(ventana, text="Carga Objetivo", bg=FONDO,
         fg="cyan", font=("Arial", 12)).pack(pady=5)

frame_obj = tk.Frame(ventana, bg=FONDO)
frame_obj.pack(pady=5)

tk.Label(frame_obj, text="Magnitud:", bg=FONDO, fg=TEXTO).grid(row=0, column=0)
entry_q_obj = tk.Entry(frame_obj, width=10, bg=CAJA, fg="white", insertbackground="white")
entry_q_obj.grid(row=0, column=1, padx=5)

tk.Label(frame_obj, text="X:", bg=FONDO, fg=TEXTO).grid(row=0, column=2)
entry_x_obj = tk.Entry(frame_obj, width=10, bg=CAJA, fg="white", insertbackground="white")
entry_x_obj.grid(row=0, column=3, padx=5)

tk.Label(frame_obj, text="Y:", bg=FONDO, fg=TEXTO).grid(row=0, column=4)
entry_y_obj = tk.Entry(frame_obj, width=10, bg=CAJA, fg="white", insertbackground="white")
entry_y_obj.grid(row=0, column=5, padx=5)

# BOTONES PRINCIPALES
tk.Button(ventana, text="Calcular",
          bg=BOTON, fg="white", command=calcular).pack(pady=5)

tk.Button(ventana, text="Ver Plano Cartesiano",
          bg=BOTON, fg="white", command=ver_plano).pack(pady=5)

# RESULTADO
resultado = tk.StringVar()
tk.Label(ventana, textvariable=resultado,
         bg=FONDO, fg="cyan").pack(pady=5)

# PROCEDIMIENTO
text_procedimiento = tk.Text(ventana, height=15,
                            bg=CAJA, fg="white", insertbackground="white")
text_procedimiento.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

ventana.mainloop()