
import customtkinter as ctk
import math
import matplotlib.pyplot as plt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# La Constante de Coulomb: k = 9 × 10^9 N·m²/C²
k = 9 * 10**9

# Lista donde se almacenarán las cargas ingresadas, Cada carga se guarda como una tupla: (q, x, y)
cargas = []



# FUNCIONES PRINCIPALES

def agregar_carga():
    """
    Esta función toma los valores ingresados por el usuario y los agrega a la lista cargas
    tengo hambrita Allysson

    """
    try:
        # Se leen los datos ingresados 
        q = float(entry_q.get())   # Magnitud de la carga
        x = float(entry_x.get())   # Posición x
        y = float(entry_y.get())   # Posición y

        # Se agrega la carga a la lista global
        cargas.append((q, x, y))

        lista_cargas.insert("end", f"q={q} C | ({x}, {y})\n")

        # Se actualiza el contador de cargas ingresadas
        contador.configure(text=f"Cargas ingresadas: {len(cargas)}")

        # se clean
        entry_q.delete(0, "end")
        entry_x.delete(0, "end")
        entry_y.delete(0, "end")

    except ValueError:
        # solo numero se aceptan
        resultado.configure(text="Ingresa datos numéricos válidos")


def calcular():
    """
    Esta función calcula la fuerza eléctrica neta sobre una carga objetivo
    usando la Ley de Coulomb.

    """
    try:
        # Si no hay cargas ingresadas, no se puede calcular
        if not cargas:
            resultado.configure(text="Debes ingresar al menos una carga")
            return

       
        q_obj = float(entry_q_obj.get())   # Carga objetivo
        x_obj = float(entry_x_obj.get())   # Posición x de la carga objetivo
        y_obj = float(entry_y_obj.get())   # Posición y de la carga objetivo

        # Variables acumuladoras para las componentes totales
        Fx_total = 0
        Fy_total = 0

        
        procedimiento = ""

        #se recorre cada carga ingresada
        for i, (q, x, y) in enumerate(cargas):
            # Diferencia en posición entre la carga objetivo y la carga actual
            dx = x_obj - x
            dy = y_obj - y

            # Distancia entre ambas cargas
            r = math.sqrt(dx**2 + dy**2)

            # Validación: si la distancia es 0, ambas cargas están en el mismo punto
            if r == 0:
                resultado.configure(text=" Error: una carga coincide con la carga objetivo")
                return

            # Ley de Coulombbb:
            # F = k * (q1 * q2) / r^2
            F = k * (q * q_obj) / (r**2)

            # Descomposición de la fuerza en sus componentes x e y
            Fx = F * (dx / r)
            Fy = F * (dy / r)

            # Acumular componentes totales
            Fx_total += Fx
            Fy_total += Fy

            
            procedimiento += (
                f"Carga {i+1}\n"
                f"q = {q} C\n"
                f"Posición = ({x}, {y})\n"
                f"dx = {dx:.2f}, dy = {dy:.2f}\n"
                f"r = {r:.2f}\n"
                f"F = {F:.2e} N\n"
                f"Fx = {Fx:.2e}, Fy = {Fy:.2e}\n"
                f"-----------------------------\n"
            )

        # Magnitud de la fuerza neta resultante
        F_total = math.sqrt(Fx_total**2 + Fy_total**2)

        resultado.configure(
            text=f"Fuerza neta:\n<{Fx_total:.2e}, {Fy_total:.2e}> N\nMagnitud: {F_total:.2e} N"
        )

        # Limpiar el área de procedimiento antes de insertar el nuevo
        text_procedimiento.delete("1.0", "end")

        # Insertar el procedimiento completo
        text_procedimiento.insert("end", procedimiento)

    except ValueError:
        # Error si algún dato ingresado no es numérico
        resultado.configure(text="Verifica los datos ingresados plis")


def ver_plano():
    """
    Esta función muestra un plano cartesiano con:
    las cargas ingresadas
    la posición de la carga objetivo

    Colores:
    rojito = carga positiva
    azul = carga negativa
    verde = carga objetivo
    """
    if not cargas:
        resultado.configure(text="No hay cargas para mostrar")
        return

    try:
        # Lee posición de la carga objetivo
        x_obj = float(entry_x_obj.get())
        y_obj = float(entry_y_obj.get())

        # el plano poderoso
        plt.figure(figsize=(7, 7))
        ax = plt.gca()

        # Dibujar cada carga ingresada
        for i, (q, x, y) in enumerate(cargas):
            # Rojo para positivas, azul para negativas
            color = "red" if q > 0 else "blue"

            ax.scatter(x, y, color=color, s=90)

            ax.text(x, y, f"q{i+1}", fontsize=10)

        # Dibujar carga objetivo en verde
        ax.scatter(x_obj, y_obj, color="green", s=110)
        ax.text(x_obj, y_obj, "Objetivo", fontsize=10)

        
        ax.axhline(0, color="black")
        ax.axvline(0, color="black")

        ax.set_title("Plano Cartesiano")
        ax.grid(True)

        plt.show()

    except ValueError:
        # Error por si no se ingresaron correctamente los datos de la carga objetivo
        resultado.configure(text="Error al generar el plano")


def limpiar_todo():

    global cargas
    cargas = []

    lista_cargas.delete("1.0", "end")
    text_procedimiento.delete("1.0", "end")

    entry_q.delete(0, "end")
    entry_x.delete(0, "end")
    entry_y.delete(0, "end")

    entry_q_obj.delete(0, "end")
    entry_x_obj.delete(0, "end")
    entry_y_obj.delete(0, "end")

    contador.configure(text="Cargas ingresadas: 0")
    resultado.configure(text="")



# La interfaz

# Ventana principal
app = ctk.CTk()
app.title("Calculadora Ley de Coulomb")
app.geometry("1200x760")
app.configure(fg_color="#0A1A44") 




titulo = ctk.CTkLabel(
    app,
    text="Calculadora Ley de Coulomb",
    text_color="white",
    font=("Arial", 30, "bold")
)
titulo.pack(pady=20)



# Frame principal dividido en dos columnas mi compu es muy pequena no me daba 
main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)



# Carga objetivo 

left_frame = ctk.CTkFrame(main_frame, fg_color="#10285C", corner_radius=15)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

left_frame.grid_columnconfigure(0, weight=1)


label_obj = ctk.CTkLabel(
    left_frame,
    text="Carga Objetivo",
    text_color="white",
    font=("Arial", 24, "bold")
)
label_obj.pack(pady=(20, 10))

frame_obj = ctk.CTkFrame(left_frame, fg_color="#173A7A")
frame_obj.pack(pady=10, padx=20)

entry_q_obj = ctk.CTkEntry(frame_obj, placeholder_text="Magnitud", width=180)
entry_q_obj.grid(row=0, column=0, padx=8, pady=12)

# Entrada para posición X 
entry_x_obj = ctk.CTkEntry(frame_obj, placeholder_text="X", width=120)
entry_x_obj.grid(row=0, column=1, padx=8, pady=12)

# Entrada para posición Y 
entry_y_obj = ctk.CTkEntry(frame_obj, placeholder_text="Y", width=120)
entry_y_obj.grid(row=0, column=2, padx=8, pady=12)

frame_botones = ctk.CTkFrame(left_frame, fg_color="transparent")
frame_botones.pack(pady=20)

btn_calcular = ctk.CTkButton(
    frame_botones,
    text="Calcular",
    fg_color="white",
    text_color="#0A1A44",
    hover_color="#DADADA",
    width=150,
    command=calcular
)
btn_calcular.grid(row=0, column=0, padx=10, pady=5)

# Botón para mostrar el plano cartesiano
btn_plano = ctk.CTkButton(
    frame_botones,
    text="Ver Plano",
    fg_color="white",
    text_color="#0A1A44",
    hover_color="#DADADA",
    width=150,
    command=ver_plano
)
btn_plano.grid(row=0, column=1, padx=10, pady=5)

btn_limpiar = ctk.CTkButton(
    frame_botones,
    text="Limpiar",
    fg_color="white",
    text_color="#0A1A44",
    hover_color="#DADADA",
    width=150,
    command=limpiar_todo
)
btn_limpiar.grid(row=0, column=2, padx=10, pady=5)

# Etiqueta donde se mostrará el resultado final
resultado = ctk.CTkLabel(
    left_frame,
    text="",
    text_color="white",
    font=("Arial", 17, "bold"),
    wraplength=500,
    justify="center"
)
resultado.pack(pady=10, padx=15)

# Título del área de procedimiento
label_proc = ctk.CTkLabel(
    left_frame,
    text="Procedimiento",
    text_color="white",
    font=("Arial", 20, "bold")
)
label_proc.pack(pady=(15, 8))

# Caja de texto donde se muestra el desarrollo paso a paso
text_procedimiento = ctk.CTkTextbox(
    left_frame,
    width=500,
    height=320,
    fg_color="#173A7A",
    text_color="white",
    scrollbar_button_color="white",
    scrollbar_button_hover_color="#DADADA"
)
text_procedimiento.pack(padx=20, pady=(0, 20), fill="both", expand=True)



# Pa agregar cargas 

right_frame = ctk.CTkFrame(main_frame, fg_color="#10285C", corner_radius=15)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

right_frame.grid_columnconfigure(0, weight=1)

label_cargas = ctk.CTkLabel(
    right_frame,
    text="Agregar Cargas",
    text_color="white",
    font=("Arial", 24, "bold")
)
label_cargas.pack(pady=(20, 10))

frame_cargas = ctk.CTkFrame(right_frame, fg_color="#173A7A")
frame_cargas.pack(pady=10, padx=20)

entry_q = ctk.CTkEntry(frame_cargas, placeholder_text="Magnitud", width=180)
entry_q.grid(row=0, column=0, padx=8, pady=12)

# Entrada para posición X
entry_x = ctk.CTkEntry(frame_cargas, placeholder_text="X", width=120)
entry_x.grid(row=0, column=1, padx=8, pady=12)

# Entrada para posición Y
entry_y = ctk.CTkEntry(frame_cargas, placeholder_text="Y", width=120)
entry_y.grid(row=0, column=2, padx=8, pady=12)

btn_agregar = ctk.CTkButton(
    right_frame,
    text="Agregar carga",
    fg_color="white",
    text_color="#0A1A44",
    hover_color="#DADADA",
    width=180,
    command=agregar_carga
)
btn_agregar.pack(pady=10)

contador = ctk.CTkLabel(
    right_frame,
    text="Cargas ingresadas: 0",
    text_color="white",
    font=("Arial", 16)
)
contador.pack(pady=5)

# Título de la lista visual de cargas
label_lista = ctk.CTkLabel(
    right_frame,
    text="Lista de cargas",
    text_color="white",
    font=("Arial", 20, "bold")
)
label_lista.pack(pady=(15, 8))

# Caja de texto donde se muestran las cargas ingresadas
lista_cargas = ctk.CTkTextbox(
    right_frame,
    width=500,
    height=500,
    fg_color="#173A7A",
    text_color="white",
    scrollbar_button_color="white",
    scrollbar_button_hover_color="#DADADA"
)
lista_cargas.pack(padx=20, pady=(0, 20), fill="both", expand=True)




# Inicia el bucle principal de la interfaz
app.mainloop()