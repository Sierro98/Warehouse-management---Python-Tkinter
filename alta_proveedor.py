import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import Tk, Button


def actualizarcomboMercancias(event):
    mercanciaIndex = mercanciasProveedor.current()

def actualizarNombre(event):
    nombre = nombreProveedor.get()

def actualizarDireccion():
    direccion = direccionProveedor.get()

def actualizarTelefono(event):
    telefono = telefonoProveedor.get()

def actualizarCiudad(event):
    ciudadIndex = ciudadProveedor.current()

def actualizarObservaciones(event):
    observaciones = observacionesProveedor.get("1.0", "end-1c")


def grabar():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    nombre = nombreProveedor.get()
    direccion = direccionProveedor.get()
    telefono = telefonoProveedor.get()
    mercanciaIndex = mercanciasProveedor.current()
    ciudadIndex = ciudadProveedor.current()
    observaciones = observacionesProveedor.get("1.0","end-1c")

    if mercanciaIndex == 0:
        mercancia = 'Hardware'
    elif mercanciaIndex == 1:
        mercancia = 'Software'

    if ciudadIndex == 0:
        ciudad = "Madrid"
    elif ciudadIndex == 1:
        ciudad = "Alcala de Henares"
    elif ciudadIndex == 2:
        ciudad = "Villalba"
    elif ciudadIndex == 3:
        ciudad = "Galapagar"
    elif ciudadIndex == 4:
        ciudad = "Valdemoro"
    elif ciudadIndex == 5:
        ciudad = "Alcobendas"
    elif ciudadIndex == 6:
        ciudad = "Mostoles"

    try:
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS proveedores (
                           CODIGO INTEGER PRIMARY KEY AUTOINCREMENT,
                           NOMBRE VARCHAR(40) NOT NULL,
                           DIRECCION VARCHAR(100) NOT NULL,
                           CIUDAD VARCHAR(40) NOT NULL,
                           TELEFONO INT NOT NULL,
                           MERCANCIAS VARCHAR(50) NOT NULL,
                           OBSERVACIONES TEXT NOT NULL)

                       ''')
        print("Tabla creada correctamente")
    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

    registro = "INSERT INTO proveedores (NOMBRE, DIRECCION, CIUDAD, TELEFONO, MERCANCIAS, OBSERVACIONES)" \
               " VALUES(?, ?, ?, ?, ?, ?)"
    cursor.execute(registro, [nombre, direccion, ciudad, telefono, mercancia, observaciones])

    proveedores_tree.delete(*proveedores_tree.get_children())
    cursor.execute('SELECT NOMBRE, DIRECCION, CIUDAD, TELEFONO, MERCANCIAS, OBSERVACIONES FROM proveedores')
    i = 0
    for ro in cursor:
        proveedores_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5]))
        i = i + 1
    connection.commit()
    mostrar()
    continuar()


def mostrar():
    try:
        btnlgrabar['state'] = 'disabled'
        conexion = sqlite3.connect("almacen.db")
        cursor = conexion.cursor()
        registro = "SELECT * FROM proveedores;"
        cursor.execute(registro)
        producto = cursor.fetchall()
        print(producto)

    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

#TODO: esto necesita modificarse segun vaya añadiendo las variables
def continuar():
    dato = tk.messagebox.askyesno(message="¿Desea continuar?", title="Título", parent=marco)
    if dato == True:
        btnlgrabar['state'] = 'normal'
        nombreProveedor.delete(0, 'end')
        telefonoProveedor.delete(0, 'end')
        direccionProveedor.delete(0, 'end')
        ciudadProveedor.delete(0, 'end')
        mercanciasProveedor.delete(0, 'end')
        observacionesProveedor.delete("1.0", "end-1c")
    elif dato == False:
        marco.destroy()


def aniadirProveedor():
    global marco
    marco = tk.Tk()
    marco.title("Añadir Proveedor")
    marco.state('zoomed')
    marco.config(bg="#ffccff")
    marco.grid_propagate(0)
    marco.iconbitmap("gas_mask_icon.ico")

    etiqueta0 = tk.Label(marco, text="AÑADIR PROVEEDOR", bg='#ffccff', font=("Cambria 30 underline")).grid(row=0,
                                                                                                         column=1,
                                                                                                         sticky="w",
                                                                                                         padx=450,
                                                                                                         pady=30)


    etiqueta2 = tk.Label(marco, text="Nombre: ", bg="#ffccff", font=("Cambria", 20)).grid(row=1, column=0,
                                                                                                sticky="w", padx=30,
                                                                                                pady=20)
    global nombreProveedor
    nombreProveedor = tk.Entry(marco, width=50, font=("Cambria", 15))
    nombreProveedor.grid(row=1, column=1, sticky="w", padx=10, pady=10)
    nombreProveedor.bind('<Leave>', actualizarNombre)

    etiqueta3 = tk.Label(marco, text="Direccion: ", bg="#ffccff", font=("Cambria", 20)).grid(row=2, column=0,
                                                                                                sticky="w", padx=30,
                                                                                                pady=20)
    global direccionProveedor
    direccionProveedor = tk.Entry(marco, width=50, font=("Cambria", 15))
    direccionProveedor.grid(row=2, column=1, sticky="w", padx=10, pady=10)
    direccionProveedor.bind('<Leave>', actualizarDireccion)

    etiqueta4 = tk.Label(marco, text="Ciudad: ", bg="#ffccff", font=("Cambria", 20)).grid(row=3, column=0, sticky="w",
                                                                                        padx=30, pady=20)
    global ciudadProveedor
    ciudadProveedor = ttk.Combobox(marco, font=("Cambria", 15))
    ciudadProveedor['values'] = ("Madrid", "Alcala de Henares", 'Villalba', 'Galapagar', 'Valdemoro', 'Alcobendas', 'Mostoles')
    ciudadProveedor.grid(row=3, column=1, sticky="w", padx=10, pady=10)
    ciudadProveedor.bind('<<ComboboxSelected>>', actualizarCiudad)

    etiqueta5 = tk.Label(marco, text="Telefono: ", bg="#ffccff", font=("Cambria", 20)).grid(row=4, column=0,
                                                                                                      sticky="w",
                                                                                                      padx=30, pady=20)
    global telefonoProveedor
    telefonoProveedor = tk.Entry(marco, width=50, font=("Cambria", 15))
    telefonoProveedor.grid(row=4, column=1, sticky="w", padx=10, pady=10)
    telefonoProveedor.bind('<Leave>', actualizarTelefono)

    etiqueta4 = tk.Label(marco, text="Mercancias: ", bg="#ffccff", font=("Cambria", 20)).grid(row=5, column=0, sticky="w",
                                                                                          padx=30, pady=20)
    global mercanciasProveedor
    mercanciasProveedor = ttk.Combobox(marco, font=("Cambria", 15))
    mercanciasProveedor['values'] = ('Hardware', 'Software')
    mercanciasProveedor.grid(row=5, column=1, sticky="w", padx=10, pady=10)
    mercanciasProveedor.bind('<<ComboboxSelected>>', actualizarcomboMercancias)

    etiqueta6 = tk.Label(marco, text="Observaciones: ", bg="#ffccff", font=("Cambria", 20)).grid(row=6, column=0,
                                                                                             sticky="w", padx=30,
                                                                                             pady=20)
    global observacionesProveedor
    observacionesProveedor = tk.Text(marco, width=50, height=6, font=("Cambria", 15))
    barra = tk.Scrollbar(marco)
    barra.config(command=observacionesProveedor.yview, )  # orient=VERTICAL,
    observacionesProveedor["yscrollcommand"] = barra.set
    observacionesProveedor.grid(row=6, column=1, sticky="w", padx=10, pady=10)
    barra.place(x=800, y=510, height=150)
    nombreProveedor.bind('<Leave>', actualizarObservaciones)

    titClientes = tk.Label(marco, text="Proveedores", bg="#ffccff", font=("Cambria", 15)).place(x=1100, y=200)
    global proveedores_tree
    proveedores_tree = ttk.Treeview(marco)
    proveedores_tree['show'] = 'headings'
    # Definimos las columnas
    proveedores_tree['columns'] = ('Nombre', 'Direccion', 'Ciudad', 'Telefono', 'Mercancias', 'Observaciones')
    # Formateamos las columnas
    proveedores_tree.column('Nombre', width=100, anchor=tk.CENTER)
    proveedores_tree.column('Direccion', width=100, anchor=tk.CENTER)
    proveedores_tree.column('Ciudad', width=100, anchor=tk.CENTER)
    proveedores_tree.column('Telefono', width=100, anchor=tk.CENTER)
    proveedores_tree.column('Mercancias', width=100, anchor=tk.CENTER)
    proveedores_tree.column('Observaciones', width=200, anchor=tk.CENTER)
    # Titulos de columnas
    proveedores_tree.heading('Nombre', text='Nombre')
    proveedores_tree.heading('Direccion', text='Direccion')
    proveedores_tree.heading('Ciudad', text='Ciudad')
    proveedores_tree.heading('Telefono', text='Telefono')
    proveedores_tree.heading('Mercancias', text='Mercancias')
    proveedores_tree.heading('Observaciones', text='Observaciones')
    # Insert Data
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()
    cursor.execute('SELECT NOMBRE, DIRECCION, CIUDAD, TELEFONO, MERCANCIAS, OBSERVACIONES FROM proveedores')
    i = 0
    for ro in cursor:
        proveedores_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5]))
        i = i + 1
    proveedores_tree.place(x=820, y=250, height=400)

    espacio6 = tk.Label(marco, text="", bg="#ffccff").grid(row=10, column=0, sticky="w", padx=10, pady=10)
    espacio7 = tk.Label(marco, text="", bg="#ffccff").grid(row=11, column=0, sticky="w", padx=10, pady=10)

    global btnlgrabar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="GRABAR", width=10, height=2, anchor="center",
                      activebackground="blue", relief="raised",
                      borderwidth=5, font=("Cambria", 20), command=lambda: grabar())
    btnlgrabar.grid(row=8, column=1, sticky="w", padx=100, pady=10)

