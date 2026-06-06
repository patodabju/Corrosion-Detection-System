import serial
import csv
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# ==================================================
# CONFIGURACIÓN
# ==================================================

PUERTO = "COM4"      # CAMBIAR
BAUDRATE = 115200

# ==================================================
# RUTAS DEL PROYECTO
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FOLDER = BASE_DIR / "data"
EXPORT_FOLDER = BASE_DIR / "software" / "exports"

CURRENT_SESSION = DATA_FOLDER / "current_session.csv"

DATA_FOLDER.mkdir(parents=True, exist_ok=True)
EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)

# ==================================================

esp32 = None
running = False

# ==================================================
# CSV
# ==================================================

def crear_csv():

    with open(CURRENT_SESSION,
              "w",
              newline="",
              encoding="utf-8") as archivo:

        writer = csv.writer(archivo)

        writer.writerow([
            "FechaHora",
            "Estado"
        ])


def contar_registros():

    if not CURRENT_SESSION.exists():
        return 0

    with open(CURRENT_SESSION,
              "r",
              encoding="utf-8") as archivo:

        return max(sum(1 for _ in archivo) - 1, 0)


def actualizar_contador():

    lbl_contador.config(
        text=f"Registros en sesión: {contar_registros()}"
    )


# ==================================================
# SESIONES
# ==================================================

def nueva_sesion():

    if messagebox.askyesno(
            "Nueva sesión",
            "¿Deseas iniciar una nueva sesión?"):

        crear_csv()

        for item in tabla.get_children():
            tabla.delete(item)

        lbl_ultima.config(
            text="Última captura: ninguna"
        )

        actualizar_contador()


def exportar_sesion():

    if contar_registros() == 0:

        messagebox.showwarning(
            "Exportar",
            "No hay registros para exportar."
        )

        return

    nombre = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S.csv"
    )

    destino = EXPORT_FOLDER / nombre

    shutil.copy(
        CURRENT_SESSION,
        destino
    )

    messagebox.showinfo(
        "Exportación exitosa",
        f"Archivo exportado:\n\n{destino.name}"
    )


def abrir_exports():

    subprocess.Popen(
        f'explorer "{EXPORT_FOLDER}"'
    )


# ==================================================
# SERIAL
# ==================================================

def conectar():

    global esp32
    global running

    try:

        esp32 = serial.Serial(
            PUERTO,
            BAUDRATE,
            timeout=1
        )

        running = True

        lbl_estado.config(
            text=f"Conectado ({PUERTO})",
            fg="green"
        )

        leer_serial()

    except Exception as e:

        messagebox.showerror(
            "Error de conexión",
            str(e)
        )


def detener():

    global running
    global esp32

    running = False

    try:
        if esp32:
            esp32.close()
    except:
        pass

    lbl_estado.config(
        text="Desconectado",
        fg="red"
    )


# ==================================================
# DATOS
# ==================================================

def guardar_dato(estado):

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(CURRENT_SESSION,
              "a",
              newline="",
              encoding="utf-8") as archivo:

        writer = csv.writer(archivo)

        writer.writerow([
            fecha,
            estado
        ])

    tabla.insert(
        "",
        "end",
        values=(fecha, estado)
    )

    tabla.yview_moveto(1)

    lbl_ultima.config(
        text=f"Última captura: {fecha} | {estado}"
    )

    actualizar_contador()


def leer_serial():

    global running

    if running:

        try:

            linea = esp32.readline()\
                .decode(
                    "utf-8",
                    errors="ignore"
                )\
                .strip()

            if linea in [
                "CORROIDA",
                "NO_CORROIDA"
            ]:

                guardar_dato(
                    linea
                )

        except:
            pass

    root.after(
        100,
        leer_serial
    )


# ==================================================
# CARGAR SESIÓN EXISTENTE
# ==================================================

def cargar_sesion_actual():

    if not CURRENT_SESSION.exists():
        crear_csv()
        return

    with open(CURRENT_SESSION,
              "r",
              encoding="utf-8") as archivo:

        reader = csv.reader(archivo)

        next(reader, None)

        for fila in reader:

            if len(fila) == 2:

                tabla.insert(
                    "",
                    "end",
                    values=(fila[0], fila[1])
                )


# ==================================================
# GUI
# ==================================================

root = tk.Tk()

root.title(
    "Corrosion Detection System"
)

root.geometry(
    "950x600"
)

titulo = tk.Label(
    root,
    text="Corrosion Detection System",
    font=("Arial", 18, "bold")
)

titulo.pack(pady=10)

lbl_estado = tk.Label(
    root,
    text="Desconectado",
    fg="red",
    font=("Arial", 11)
)

lbl_estado.pack()

lbl_contador = tk.Label(
    root,
    text="Registros en sesión: 0",
    font=("Arial", 11)
)

lbl_contador.pack()

lbl_ultima = tk.Label(
    root,
    text="Última captura: ninguna",
    font=("Arial", 11)
)

lbl_ultima.pack(pady=5)

frame_botones = tk.Frame(root)

frame_botones.pack(pady=10)

tk.Button(
    frame_botones,
    text="Conectar",
    width=20,
    command=conectar
).grid(row=0, column=0, padx=5)

tk.Button(
    frame_botones,
    text="Nueva sesión",
    width=20,
    command=nueva_sesion
).grid(row=0, column=1, padx=5)

tk.Button(
    frame_botones,
    text="Exportar sesión",
    width=20,
    command=exportar_sesion
).grid(row=0, column=2, padx=5)

tk.Button(
    frame_botones,
    text="Abrir exportaciones",
    width=20,
    command=abrir_exports
).grid(row=0, column=3, padx=5)

columnas = (
    "FechaHora",
    "Estado"
)

tabla = ttk.Treeview(
    root,
    columns=columnas,
    show="headings"
)

tabla.heading(
    "FechaHora",
    text="Fecha y Hora"
)

tabla.heading(
    "Estado",
    text="Estado"
)

tabla.column(
    "FechaHora",
    width=300
)

tabla.column(
    "Estado",
    width=200
)

tabla.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# ==================================================
# INICIALIZACIÓN
# ==================================================

if not CURRENT_SESSION.exists():
    crear_csv()

cargar_sesion_actual()
actualizar_contador()

root.protocol(
    "WM_DELETE_WINDOW",
    lambda: (
        detener(),
        root.destroy()
    )
)

root.mainloop()