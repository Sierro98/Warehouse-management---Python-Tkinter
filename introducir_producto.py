import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import Tk, Button


def actualizarTabla():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()
    productos_tree.delete(*productos_tree.get_children())
    cursor.execute('SELECT CODIGO, NOMBREPROVEEDOR, NOMBRE, CANTIDAD, DESCRIPCION FROM productos')
    i = 0
    for ro in cursor:
        productos_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2], ro[3], ro[4]))
        i = i + 1

    cursor.close()
    connection.close()

def onSelected(event):
    limpiarCampos()
    for selItem in productos_tree.selection():
        item = productos_tree.item(selItem)
        cod, nomProv, nom, cant, desc = item["values"][0:5]
        global codigoSelected
        codigoSelected = int(cod)
        nombreProducto.insert(0, nom)
        cantProducto.insert(0, cant)
        descripcionProducto.insert("1.0", desc)
        nombreProveedor.insert(0, nomProv)

def limpiarCampos():
    nombreProveedor.delete(0, 'end')
    nombreProducto.delete(0, 'end')
    descripcionProducto.delete("1.0", "end-1c")
    cantProducto.delete(0, 'end')

def modificar():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    proveedorIndex = nombreProveedor.current()
    nombre = nombreProducto.get()
    cantidad = cantProducto.get()
    descripcion = descripcionProducto.get("1.0", "end-1c")
    j = 0
    for i in cblist:
        if proveedorIndex == j:
            nombreProv = cblist[j][0]
        j = j + 1

    update = 'UPDATE productos SET NOMBREPROVEEDOR = ?, NOMBRE = ?, CANTIDAD = ?, DESCRIPCION = ? ' \
             'WHERE CODIGO = ?'

    cursor.execute(update, [nombreProv, nombre, cantidad, descripcion, codigoSelected])
    connection.commit()
    actualizarTabla()
    cursor.close()
    connection.close()
def borrar():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    borrar = 'DELETE FROM productos WHERE CODIGO = ?'
    cursor.execute(borrar, [codigoSelected])
    connection.commit()
    actualizarTabla()
    cursor.close()
    connection.close()



def actualizarNombreProducto(event):
    nombreProd = nombreProducto.get()

def actualizarComboProveedor(event):
    proveedorIndex = nombreProveedor.get()

def actualizarCantidad(event):
    cantidad = cantProducto.get()

def actualizarDescripcion(event):
    descripcion = descripcionProducto.get("1.0", "end-1c")

def grabar():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    proveedorIndex = nombreProveedor.current()
    nombre = nombreProducto.get()
    cantidad = cantProducto.get()
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
                           CANTIDAD INT NOT NULL,
                           DESCRIPCION TEXT NOT NULL)
                       ''')
        print("Tabla creada correctamente")
    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

    registro = "INSERT INTO productos (NOMBREPROVEEDOR, NOMBRE, CANTIDAD, DESCRIPCION)" \
               " VALUES(?, ?, ?, ?)"
    cursor.execute(registro, [nombreProv, nombre, cantidad, descripcion])

    connection.commit()
    actualizarTabla()
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
        cantProducto.delete(0, 'end')
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

    titCantProducto = tk.Label(marco, text='Cantidad inicial:', bg='#ffccff', font=('Cambria', 20)).grid(row=6, column=0, sticky='w', pady=20)
    global cantProducto
    cantProducto = tk.Spinbox(marco, font=('Cambria', 20), width=19, from_=0, to=100)
    cantProducto.grid(row=6, column=1, sticky='w')
    cantProducto.bind('<Leave>', actualizarCantidad)


    etiqueta6 = tk.Label(marco, text="Descripcion: ", bg="#ffccff", font=("Cambria", 20)).grid(row=7, column=0,
                                                                                             sticky="w", padx=30,
                                                                                             pady=20)
    global descripcionProducto
    descripcionProducto = tk.Text(marco, width=50, height=6, font=("Cambria", 15))
    barra = tk.Scrollbar(marco)
    barra.config(command=descripcionProducto.yview, )  # orient=VERTICAL,
    descripcionProducto["yscrollcommand"] = barra.set
    descripcionProducto.grid(row=7, column=1, sticky="w", pady=10)
    barra.grid(row=7, column=2, sticky='nsw')
    descripcionProducto.bind('<Leave>', actualizarDescripcion)

    titClientes = tk.Label(marco, text="Productos", bg="#ffccff", font=("Cambria", 15)).place(x=1200, y=200)
    global productos_tree
    productos_tree = ttk.Treeview(marco)
    productos_tree['show'] = 'headings'
    # Definimos las columnas
    productos_tree['columns'] = ('Codigo', 'NombreProducto', 'NombreProveedor', 'Cantidad', 'Descripcion')
    # Formateamos las columnas
    productos_tree.column('Codigo', width=50, anchor=tk.CENTER)
    productos_tree.column('NombreProducto', width=100, anchor=tk.CENTER)
    productos_tree.column('NombreProveedor', width=100, anchor=tk.CENTER)
    productos_tree.column('Cantidad', width=100, anchor=tk.CENTER)
    productos_tree.column('Descripcion', width=200, anchor=tk.CENTER)
    # Titulos de columnas
    productos_tree.heading("Codigo", text="Codigo")
    productos_tree.heading('NombreProducto', text='Nombre Proveedor')
    productos_tree.heading('NombreProveedor', text='Nombre Producto')
    productos_tree.heading('Cantidad', text='Cantidad')
    productos_tree.heading('Descripcion', text='Descripcion')
    # Insert Data
    actualizarTabla()
    productos_tree.bind("<<TreeviewSelect>>", onSelected)
    productos_tree.place(x=900, y=250, height=400)

    espacio6 = tk.Label(marco, text="", bg="#ffccff").grid(row=10, column=0, sticky="w", padx=10, pady=10)
    espacio7 = tk.Label(marco, text="", bg="#ffccff").grid(row=11, column=0, sticky="w", padx=10, pady=10)

    global btnlgrabar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="GRABAR", width=10, height=2, anchor="center",
                      activebackground="blue", relief="raised",
                      borderwidth=5, font=("Cambria", 20), command=lambda: grabar())
    btnlgrabar.place(x=350, y=675)

    global btnModificar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="MODIFICAR", width=10, height=2, anchor="center",
                      activebackground="blue", relief="raised",
                      borderwidth=5, font=("Cambria", 20), command=lambda: modificar())
    btnlgrabar.place(x=160, y=675)

    global btnBorrar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="BORRAR", width=10, height=2, anchor="center",
                      activebackground="blue", relief="raised",
                      borderwidth=5, font=("Cambria", 20), command=lambda: borrar())
    btnlgrabar.place(x=540, y=675)