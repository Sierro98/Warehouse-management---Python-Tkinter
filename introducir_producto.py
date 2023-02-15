import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import Tk, Button


def actualizarNombreProducto(event):
    nombreProd = nombreProducto.get()

def actualizarComboProveedor(event):
    proveedorIndex = nombreProveedor.get()

def actualizarDescripcion(event):
    descripcion = descripcionProducto.get("1.0", "end-1c")

def grabar():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    proveedorIndex = nombreProveedor.current()
    nombre = nombreProducto.get()
    descripcion = descripcionProducto.get("1.0","end-1c")
    j=0
    for i in cblist:
        if proveedorIndex == j:
            nombreProv = cblist[j][0]
        j = j + 1

    try:
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS productos (
                           CODIGO INTEGER PRIMARY KEY AUTOINCREMENT,
                           NOMBREPROVEEDOR VARCHAR(40) NOT NULL,
                           NOMBRE VARCHAR(100) NOT NULL,
                           DESCRIPCION TEXT NOT NULL)
                       ''')
        print("Tabla creada correctamente")
    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

    registro = "INSERT INTO productos (NOMBREPROVEEDOR, NOMBRE, DESCRIPCION)" \
               " VALUES(?, ?, ?)"
    cursor.execute(registro, [nombreProv, nombre, descripcion])

    productos_tree.delete(*productos_tree.get_children())
    cursor.execute('SELECT NOMBREPROVEEDOR, NOMBRE, DESCRIPCION FROM productos')
    i = 0
    for ro in cursor:
        productos_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2]))
        i = i + 1
    connection.commit()
    mostrar()
    continuar()

def mostrar():
    try:
        btnlgrabar['state'] = 'disabled'
        conexion = sqlite3.connect("almacen.db")
        cursor = conexion.cursor()
        registro = "SELECT * FROM productos;"
        cursor.execute(registro)
        producto = cursor.fetchall()
        print(producto)

    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

def continuar():
    dato = tk.messagebox.askyesno(message="¿Desea continuar?", title="Título", parent=marco)
    if dato == True:
        btnlgrabar['state'] = 'normal'
        nombreProducto.delete(0, 'end')
        nombreProveedor.delete(0, 'end')
        descripcionProducto.delete("1.0", "end-1c")
    elif dato == False:
        marco.destroy()


def aniadirProducto():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    try:
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS productos (
                           CODIGO INTEGER PRIMARY KEY AUTOINCREMENT,
                           NOMBREPROVEEDOR VARCHAR(40) NOT NULL,
                           NOMBRE VARCHAR(100) NOT NULL,
                           DESCRIPCION TEXT NOT NULL)
                       ''')
        print("Tabla creada correctamente")
    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)
    global marco
    marco = tk.Tk()
    marco.title("Añadir Producto")
    marco.state('zoomed')
    marco.config(bg="#ffccff")
    marco.grid_propagate(0)
    marco.iconbitmap("gas_mask_icon.ico")

    etiqueta0 = tk.Label(marco, text="AÑADIR PRODUCTO", bg='#ffccff', font=("Cambria 30 underline")).grid(row=0,
                                                                                                         column=1,
                                                                                                         sticky="w",
                                                                                                         padx=450,
                                                                                                         pady=30)

    espacio1 = tk.Label(marco, text="", bg="#ffccff").grid(row=1, column=1, sticky="w", padx=10, pady=10)
    espacio2 = tk.Label(marco, text="", bg="#ffccff").grid(row=2, column=1, sticky="w", padx=10, pady=10)

    etiqueta2 = tk.Label(marco, text="Nombre Producto: ", bg="#ffccff", font=("Cambria", 20)).grid(row=4, column=0,
                                                                                          sticky="w", padx=30,
                                                                                          pady=20)
    global nombreProducto
    nombreProducto = tk.Entry(marco, width=50, font=("Cambria", 15))
    nombreProducto.grid(row=4, column=1, sticky="w", padx=10, pady=10)
    nombreProducto.bind('<Leave>', actualizarNombreProducto)

    etiqueta2 = tk.Label(marco, text="Nombre Proveedor: ", bg="#ffccff", font=("Cambria", 20)).grid(row=5, column=0,
                                                                                                sticky="w",
                                                                                                pady=20)
    global nombreProveedor
    global current_var
    current_var = tk.StringVar()

    nombreProveedor = ttk.Combobox(marco, textvariable=current_var, font=("Cambria", 15))
    global cblist
    cblist= list()
    for row in cursor.execute('SELECT NOMBRE FROM proveedores'):
        cblist.append(row)
    nombreProveedor['values'] = (cblist)
    nombreProveedor.grid(row=5, column=1, sticky='w')
    nombreProveedor.bind('<<ComboboxSelected>>', actualizarComboProveedor)
    cursor.close()


    etiqueta6 = tk.Label(marco, text="Descripcion: ", bg="#ffccff", font=("Cambria", 20)).grid(row=6, column=0,
                                                                                             sticky="w", padx=30,
                                                                                             pady=20)
    global descripcionProducto
    descripcionProducto = tk.Text(marco, width=50, height=6, font=("Cambria", 15))
    barra = tk.Scrollbar(marco)
    barra.config(command=descripcionProducto.yview, )  # orient=VERTICAL,
    descripcionProducto["yscrollcommand"] = barra.set
    descripcionProducto.grid(row=6, column=1, sticky="w", pady=10)
    barra.grid(row=6, column=2, sticky='nsw')
    descripcionProducto.bind('<Leave>', actualizarDescripcion)

    titClientes = tk.Label(marco, text="Proveedores", bg="#ffccff", font=("Cambria", 15)).grid(row=3, column=3, sticky='w')
    global productos_tree
    productos_tree = ttk.Treeview(marco)
    productos_tree['show'] = 'headings'
    # Definimos las columnas
    productos_tree['columns'] = ('NombreProducto', 'NombreProveedor', 'Descripcion')
    # Formateamos las columnas
    productos_tree.column('NombreProducto', width=100, anchor=tk.CENTER)
    productos_tree.column('NombreProveedor', width=100, anchor=tk.CENTER)
    productos_tree.column('Descripcion', width=200, anchor=tk.CENTER)
    # Titulos de columnas
    productos_tree.heading('NombreProducto', text='Nombre Proveedor')
    productos_tree.heading('NombreProveedor', text='Nombre Producto')
    productos_tree.heading('Descripcion', text='Descripcion')
    # Insert Data
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()
    cursor.execute('SELECT NOMBREPROVEEDOR, NOMBRE, DESCRIPCION FROM productos')
    i = 0
    for ro in cursor:
        productos_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2]))
        i = i + 1
    productos_tree.place(x=1000, y=250, height=400)

    espacio6 = tk.Label(marco, text="", bg="#ffccff").grid(row=10, column=0, sticky="w", padx=10, pady=10)
    espacio7 = tk.Label(marco, text="", bg="#ffccff").grid(row=11, column=0, sticky="w", padx=10, pady=10)

    global btnlgrabar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="GRABAR", width=10, height=2, anchor="center",
                      activebackground="blue", relief="raised",
                      borderwidth=5, font=("Cambria", 20), command=lambda: grabar())
    btnlgrabar.grid(row=8, column=1, sticky="w", padx=100, pady=10)