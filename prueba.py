import tkinter as tk
from tkinter import ttk
from datetime import datetime
import requests

class AddArticleApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Añadir artículo")

        # Variables de control
        self.titulo_var = tk.StringVar()
        self.resumen_var = tk.StringVar()
        self.contenido_var = tk.StringVar()
        self.autores_seleccionados = []

        # Obtener autores desde la API
        self.autores = self.obtener_autores()

        # Interfaz de usuario
        self.create_widgets()

    def obtener_autores(self):
        try:
            response = requests.get('http://localhost:4000/api/autor')
            if response.ok:
                return response.json().get("body", [])
            else:
                print(f"Error al obtener la lista de autores. Código de estado: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error durante la solicitud de autores: {e}")
            return []

    def obtener_ultimo_codigo_articulo(self):
        try:
            response = requests.get('http://localhost:4000/api/articulo')
            if response.ok:
                data = response.json().get("body", [])
                return data[-1]["id"] if data else 0
            else:
                print(f"Error al obtener el último código de artículo. Código de estado: {response.status_code}")
                return 0
        except Exception as e:
            print(f"Error durante la solicitud del último código de artículo: {e}")
            return 0

    def obtener_fecha_actual(self):
        fecha = datetime.now()
        return fecha.strftime("%Y-%m-%d")

    def create_widgets(self):
        # Widgets para seleccionar autores
        self.autor_tree = ttk.Treeview(self.master, columns=("ID", "Nombre", "Apellido", "Institución"), displaycolumns=(1, 2, 3))
        self.autor_tree.heading("#0", text="Autores")
        self.autor_tree["show"] = "headings"
        for col in ["ID", "Nombre", "Apellido", "Institución"]:
            self.autor_tree.heading(col, text=col)
            self.autor_tree.column(col, width=50)  # Establecer ancho de columna
        for autor in self.autores:
            self.autor_tree.insert("", "end", values=(autor["id"], autor["nombre"], autor["apellido"], autor["institucion"]))
        self.autor_tree.grid(row=0, column=0, padx=10, pady=10, rowspan=3, sticky="w")

        # Widgets para mostrar autores seleccionados en tabla
        self.autores_seleccionados_tree = ttk.Treeview(self.master, columns=("ID", "Nombre", "Apellido", "Institución"), displaycolumns=(1, 2, 3))
        self.autores_seleccionados_tree.heading("#0", text="Autores Seleccionados")
        self.autores_seleccionados_tree["show"] = "headings"
        for col in ["ID", "Nombre", "Apellido", "Institución"]:
            self.autores_seleccionados_tree.heading(col, text=col)
            self.autores_seleccionados_tree.column(col, width=50)  # Establecer ancho de columna
        self.autores_seleccionados_tree.grid(row=0, column=1, padx=10, pady=10, rowspan=3, sticky="w")

        # Widgets para información del artículo
        self.titulo_label = tk.Label(self.master, text="Título:")
        self.titulo_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.titulo_entry = tk.Entry(self.master, textvariable=self.titulo_var)
        self.titulo_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.resumen_label = tk.Label(self.master, text="Resumen:")
        self.resumen_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.resumen_text = tk.Text(self.master, height=5, width=40)
        self.resumen_text.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.contenido_label = tk.Label(self.master, text="Contenido:")
        self.contenido_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")

        self.contenido_text = tk.Text(self.master, height=10, width=40)
        self.contenido_text.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Widgets para agregar autores
        self.agregar_button = tk.Button(self.master, text="Agregar Autor", command=self.handle_agregar)
        self.agregar_button.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        # Botón para agregar artículo
        self.agregar_articulo_button = tk.Button(self.master, text="Agregar Artículo", command=self.handle_agregar_articulo)
        self.agregar_articulo_button.grid(row=4, column=2, padx=10, pady=5, rowspan=2, sticky="w")

        # Mensaje de éxito
        self.success_label = tk.Label(self.master, text="")
        self.success_label.grid(row=6, column=0, columnspan=3, pady=10)

    def handle_agregar(self):
        selected_item = self.autor_tree.selection()
        if selected_item:
            autor_id = self.autor_tree.item(selected_item, "values")[0]
            if autor_id not in self.autores_seleccionados:
                self.autores_seleccionados.append(autor_id)
                self.update_autores_seleccionados_tree()

    def update_autores_seleccionados_tree(self):
        self.autores_seleccionados_tree.delete(*self.autores_seleccionados_tree.get_children())
        for autor_id in self.autores_seleccionados:
            autor = self.obtener_autor_por_id(autor_id)
            if autor:
                self.autores_seleccionados_tree.insert("", "end", values=(autor["id"], autor["nombre"], autor["apellido"], autor["institucion"]))

    def handle_agregar_articulo(self):
        try:
            # Obtener la información del artículo desde las variables de control
            titulo = self.titulo_var.get()
            resumen = self.resumen_text.get("1.0", "end-1c")
            contenido = self.contenido_text.get("1.0", "end-1c")

            # Agregar el artículo
            response_articulo = requests.post('http://localhost:4000/api/articulo', json={
                "id": 0,
                "titulo": titulo,
                "resumen": resumen,
                "contenido": contenido,
                "activo": 1
            })

            if not response_articulo.ok:
                print(f"Error al agregar artículo. Código de estado: {response_articulo.status_code}")
                return

            # Mostrar mensaje de éxito y limpiar campos
            self.success_label.config(text="Artículo agregado exitosamente", fg="green")
            self.titulo_var.set("")
            self.resumen_text.delete("1.0", tk.END)
            self.contenido_text.delete("1.0", tk.END)
            self.autores_seleccionados = []
            self.update_autores_seleccionados_tree()

        except Exception as e:
            print(f"Error durante la solicitud: {e}")

    def obtener_autor_por_id(self, autor_id):
        try:
            response = requests.get(f'http://localhost:4000/api/autor/{autor_id}')
            if response.ok:
                return response.json().get("body", [])[0]
            else:
                print(f"Error al obtener el autor. Código de estado: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error durante la solicitud del autor: {e}")
            return None

def main():
    root = tk.Tk()
    app = AddArticleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
