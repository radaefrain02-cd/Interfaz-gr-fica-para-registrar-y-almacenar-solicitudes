#Registro de solicitudes de soporte tecnico, usando
#Tkinter, validaciones y archivo csv

import tkinter as tk
from tkinter import ttk
import csv
import os

#El archivo se guarda en la misma carpeta que este programa
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(CARPETA, "solicitudes.csv")

TIPOS = ["equipo", "software", "conectividad"]
PRIORIDADES = ["bajo", "medio", "alto"]


def mostrar(texto):
    #Muestra un mensaje en el area de resultados
    area.config(state="normal")
    area.delete("1.0", "end")
    area.insert("1.0", texto)
    area.config(state="disabled")


def registrar():
    #Leer los datos del formulario
    nombre = entry_nombre.get().strip()
    codigo = entry_codigo.get().strip()
    tipo = combo_tipo.get()
    descripcion = texto_desc.get("1.0", "end").strip()
    prioridad = var_prioridad.get()

    #Validaciones
    errores = []
    if nombre == "":
        errores.append("- El nombre no puede estar vacio")
    if codigo == "":
        errores.append("- El codigo de estudiante no puede estar vacio")
    if tipo not in TIPOS:
        errores.append("- Debe seleccionar un tipo de solicitud valido")
    if descripcion == "":
        errores.append("- La descripcion no puede estar vacia")
    if prioridad not in PRIORIDADES:
        errores.append("- Debe seleccionar una prioridad valida")

    if len(errores) > 0:
        mostrar("No se pudo guardar la solicitud. Coorregir lo siguiente:\n" + "\n".join(errores))
        return

    # Guardar enn archivo
    try:
        existe = os.path.exists(ARCHIVO)
        with open(ARCHIVO, "a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if not existe:
                escritor.writerow(["nombre", "codigo", "tipo", "descripcion", "prioridad"])
            escritor.writerow([nombre, codigo, tipo, descripcion, prioridad])
        mostrar("Solicitud guardada correctamente.")
        limpiar(False)
    except OSError:
        mostrar("Error:no se pudo escribir en el archivo.")


def consultar():
    try:
        with open(ARCHIVO, "r", newline="", encoding="utf-8") as f:
            filas = list(csv.reader(f))
    except FileNotFoundError:
        mostrar("Todavia no hay solicitudes guardadas (el archivo no existe).")
        return
    except OSError:
        mostrar("Error: no se pudo leer el archivo.")
        return

    #La primera fila son los titulos asi que se omite
    registros = filas[1:]
    if len(registros) == 0:
        mostrar("El archivo no tiene solicitudes.")
        return

    texto = "Solicitudes guardadas: " + str(len(registros)) + "\n\n"
    for fila in registros:
        texto += "Nombre: " + fila[0] + "\n"
        texto += "Codigo: " + fila[1] + "\n"
        texto += "Tipo: " + fila[2] + "\n"
        texto += "Descripcion: " + fila[3] + "\n"
        texto += "Prioridad: " + fila[4] + "\n"
        texto += "-----\n"
    mostrar(texto)


def limpiar(borrar_mensaje=True):
    entry_nombre.delete(0, "end")
    entry_codigo.delete(0, "end")
    combo_tipo.set("")
    texto_desc.delete("1.0", "end")
    var_prioridad.set("")
    if borrar_mensaje:
        mostrar("")


#Ventana
ventana = tk.Tk()
ventana.title("Solicitudes de soporte tecnico")

tk.Label(ventana, text="Nombre del solicitante:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nombre = tk.Entry(ventana, width=40)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(ventana, text="Codigo de estudiante:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_codigo = tk.Entry(ventana, width=40)
entry_codigo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(ventana, text="Tipo de solicitud:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
combo_tipo = ttk.Combobox(ventana, values=TIPOS, state="readonly", width=37)
combo_tipo.grid(row=2, column=1, padx=5, pady=5)

tk.Label(ventana, text="Descripcion del problema:").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
texto_desc = tk.Text(ventana, width=30, height=4)
texto_desc.grid(row=3, column=1, padx=5, pady=5)

tk.Label(ventana, text="Prioridad:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
var_prioridad = tk.StringVar(value="")
marco = tk.Frame(ventana)
marco.grid(row=4, column=1, sticky="w", padx=5, pady=5)
for p in PRIORIDADES:
    tk.Radiobutton(marco, text=p, variable=var_prioridad, value=p).pack(side="left", padx=5)

marco_botones = tk.Frame(ventana)
marco_botones.grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(marco_botones, text="Registrar solicitud", command=registrar).pack(side="left", padx=5)
tk.Button(marco_botones, text="Consultar solicitudes", command=consultar).pack(side="left", padx=5)
tk.Button(marco_botones, text="Limpiar formulario", command=limpiar).pack(side="left", padx=5)

area = tk.Text(ventana, width=60, height=12, state="disabled")
area.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

ventana.mainloop()
