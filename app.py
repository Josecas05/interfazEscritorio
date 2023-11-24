import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import requests
import subprocess

# Definir treeview como variable global
treeview = None

def obtener_json(fecha_inicio, fecha_fin):
    # Construir la URL con las fechas proporcionadas
    url = f"http://localhost:4000/api/autorArticulo/{fecha_inicio}/{fecha_fin}"

    # Realizar la solicitud HTTP
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Devolver el contenido JSON
        return response.json()
    else:
        # Si hay un error, mostrar el código de estado
        return {"error": True, "status": response.status_code}

def eliminar_elemento(id_articulo, fecha_inicio, fecha_fin):
    # Construir la URL para eliminar el elemento (usando GET)
    url = f"http://localhost:4000/api/autorArticulo/{id_articulo}"

    # Realizar la solicitud HTTP GET
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        print("Elemento eliminado exitosamente.")
        # Actualizar la vista después de eliminar
        consultar_json(fecha_inicio, fecha_fin)
    else:
        # Si hay un error, mostrar el código de estado
        print(f"Error al eliminar el elemento. Código de estado: {response.status_code}")

def seleccionar_item(event, entry_fecha_inicio, entry_fecha_fin):
    global treeview
    item_seleccionado = treeview.selection()
    if item_seleccionado:
        # Obtener el ID del artículo seleccionado
        id_articulo = treeview.item(item_seleccionado)['values'][1]  # Suponiendo que el ID del artículo es la segunda columna
        if id_articulo is not None:
            # Confirmar la eliminación
            confirmacion = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar este elemento?")
            if confirmacion:
                eliminar_elemento(id_articulo, entry_fecha_inicio.get_date(), entry_fecha_fin.get_date())

def mostrar_ventana_consulta():
    # Declarar treeview como global para que sea accesible en otras funciones
    global treeview

    ventana_consulta = tk.Toplevel(ventana_principal)
    ventana_consulta.title("Consulta de Artículos por Fecha")

    label_fecha_inicio = ttk.Label(ventana_consulta, text="Fecha de inicio:")
    label_fecha_inicio.grid(row=0, column=0, padx=10, pady=10)
    entry_fecha_inicio = DateEntry(ventana_consulta, width=12, background='darkblue', foreground='white', borderwidth=2)
    entry_fecha_inicio.grid(row=0, column=1, padx=10, pady=10)

    label_fecha_fin = ttk.Label(ventana_consulta, text="Fecha de fin:")
    label_fecha_fin.grid(row=1, column=0, padx=10, pady=10)
    entry_fecha_fin = DateEntry(ventana_consulta, width=12, background='darkblue', foreground='white', borderwidth=2)
    entry_fecha_fin.grid(row=1, column=1, padx=10, pady=10)

    boton_consultar = ttk.Button(ventana_consulta, text="Consultar", command=lambda: consultar_json(entry_fecha_inicio, entry_fecha_fin))
    boton_consultar.grid(row=2, column=0, columnspan=2, pady=20, padx=20)  # Aumentar el espaciado y el tamaño del botón

    columns = ("Nombre Autor", "ID Articulo", "Título Artículo", "Fecha")
    treeview = ttk.Treeview(ventana_consulta, columns=columns, show="headings")
    treeview.grid(row=3, column=0, columnspan=3, padx=20, pady=20)  # Aumentar el espaciado de la tabla

    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=150)

    # Agregar el evento de selección
    treeview.bind("<ButtonRelease-1>", lambda event: seleccionar_item(event, entry_fecha_inicio, entry_fecha_fin))

def consultar_json(entry_fecha_inicio, entry_fecha_fin):
    # Acceder a la variable global treeview
    global treeview

    fecha_inicio = entry_fecha_inicio.get_date()
    fecha_fin = entry_fecha_fin.get_date()

    json_data = obtener_json(fecha_inicio, fecha_fin)

    # Limpiar la tabla
    for row in treeview.get_children():
        treeview.delete(row)

    if not json_data.get("error", False):
        for item in json_data["body"]:
            treeview.insert("", "end", values=(item["nombreAutor"], item["idArticulo"], item["tituloArticulo"], item["fecha"]))

def mostrar_ventana_prueba():
    subprocess.Popen(["python", "prueba.py"])

# Ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Proyecto Programación Comercial")
ventana_principal.geometry("500x300")  # Ajustar el tamaño de la ventana principal
ventana_principal.configure(bg='#1e1e1e')  # Establecer el color de fondo similar al tono de Visual Studio Code

# Título grande
label_titulo = ttk.Label(ventana_principal, text="Proyecto Programación Comercial", font=("Helvetica", 16), foreground='white', background='#1e1e1e')
label_titulo.pack(pady=10)

# Botón para abrir la ventana de consulta
boton_abrir_consulta = ttk.Button(ventana_principal, text="Abrir Ventana de Consulta", command=mostrar_ventana_consulta, style='TButton')
boton_abrir_consulta.pack(pady=20)

# Botón para abrir la ventana de prueba (desde el archivo prueba.py)
boton_prueba = ttk.Button(ventana_principal, text="Abrir Ventana de Prueba", command=mostrar_ventana_prueba, style='TButton')
boton_prueba.pack(pady=20)

# Estilo para los botones
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10, background='#007acc', foreground='black')

# Ejecutar el bucle principal
ventana_principal.mainloop()
