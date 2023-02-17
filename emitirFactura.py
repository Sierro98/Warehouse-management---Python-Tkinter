import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import Tk, Button
from creafac import ejecutar

def actualizarComboCliente(event):
    clienteIndex = nombreCliente.current()

def actualizarProducto(event):
    productoIndex = producto.current()

def actualizarCantidadProducto(event):
    cantidad = cantProducto.get()

def actualizarPrecioProducto(event):
    precio = precioProducto.get()


def grabar():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    clienteIndex = nombreCliente.current()
    productoIndex = producto.current()
    cantidad = cantProducto.get()
    precio = precioProducto.get()
    j=0
    for i in cblistCliente:
        if clienteIndex == j:
            nombreClient = cblistCliente[j][0]
        j = j + 1
    print(nombreClient)
    j=0
    for i in cblistProducto:
        if productoIndex == j:
            nombreProd = cblistProducto[j][0]
        j = j +1
    try:
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS facturas (
                           CODIGO INTEGER PRIMARY KEY AUTOINCREMENT,
                           NOMBRECLIENTE VARCHAR(50) NOT NULL,
                           NOMBRE VARCHAR(50) NOT NULL,
                           CANTIDAD INT NOT NULL,
                           PRECIO INT NOT NULL)
                       ''')
        print("Tabla creada correctamente")
    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

    registro = "INSERT INTO facturas (NOMBRECLIENTE, NOMBRE, CANTIDAD, PRECIO)" \
               " VALUES(?, ?, ?, ?)"
    cursor.execute(registro, [nombreClient, nombreProd, cantidad, precio])

    getCantidad = 'SELECT CANTIDAD FROM productos WHERE NOMBRE = ?'
    cursor.execute(getCantidad, [nombreProd])
    cant = cursor.fetchall()[0]
    cantidadActual: int = cant[0] - int(cantidad)

    update = 'UPDATE productos SET CANTIDAD = ? WHERE NOMBRE = ?'
    cursor.execute(update, [cantidadActual, nombreProd])

    productos_tree.delete(*productos_tree.get_children())
    cursor.execute('SELECT NOMBREPROVEEDOR, NOMBRE, CANTIDAD, DESCRIPCION FROM productos')
    i = 0
    for ro in cursor:
        productos_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2], ro[3]))
        i = i + 1

    codigoquery = 'SELECT CODIGO FROM facturas WHERE NOMBRE = ?'
    cursor.execute(codigoquery, [nombreProd])
    cod = cursor.fetchall()[0]
    f = open("Factura.txt", 'w')
    f.write(f'{nombreClient}\n{cod[0]} {nombreProd} {cantidad} {precio}\u20ac')
    f.close()
    ejecutar()

    connection.commit()
    mostrar()
    continuar()

def mostrar():
    try:
        btnlgrabar['state'] = 'disabled'
        conexion = sqlite3.connect("almacen.db")
        cursor = conexion.cursor()
        registro = "SELECT * FROM facturas;"
        cursor.execute(registro)
        producto = cursor.fetchall()
        print(producto)

    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

def continuar():
    dato = tk.messagebox.askyesno(message="¿Desea continuar?", title="Título", parent=marco)
    if dato == True:
        btnlgrabar['state'] = 'normal'
        nombreCliente.delete(0, 'end')
        producto.delete(0, 'end')
        cantProducto.delete(0, 'end')
        precioProducto.delete(0, 'end')
    elif dato == False:
        marco.destroy()


def initEmitirFacturas():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()
    global marco
    marco = tk.Tk()
    marco.title("Emitir Factura")
    marco.state('zoomed')
    marco.config(bg="#ffccff")
    marco.iconbitmap("gas_mask_icon.ico")

    title = tk.Label(marco, text="Emitir Factura", bg='#ffccff', font=("Cambria 30 underline")).place(x=520, y=50)

    tit_cliente = tk.Label(marco, text="Seleccione al cliente: ", bg="#ffccff", font=("Cambria", 20)).place(x=100, y=250)
    global nombreCliente
    nombreCliente = ttk.Combobox(marco, font=("Cambria", 15))
    global cblistCliente
    cblistCliente = list()
    for row in cursor.execute('SELECT NOMBRE FROM clientes'):
        cblistCliente.append(row)
    nombreCliente['values'] = (cblistCliente)
    nombreCliente.place(x=100, y=300)
    nombreCliente.bind('<<ComboboxSelected>>', actualizarComboCliente)

    titProducto = tk.Label(marco, text="Indique el producto:", bg='#ffccff', font=('Cambria', 20)).place(x=470, y=250)
    global producto
    producto = ttk.Combobox(marco, font=('Cambria', 15))
    global cblistProducto
    cblistProducto = list()
    for row in cursor.execute('SELECT NOMBRE FROM productos'):
        cblistProducto.append(row)
    producto['values'] = (cblistProducto)
    producto.place(x=470, y=300)
    producto.bind('<<ComboboxSelected>>', actualizarProducto)

    titCantProducto = tk.Label(marco, text='Cantidad deseada:', bg='#ffccff', font=('Cambria', 20)).place(x=470, y=390)
    global cantProducto
    cantProducto = tk.Spinbox(marco, font=('Cambria', 20), width=19, from_=0, to=100)
    cantProducto.place(x=470, y=450)
    cantProducto.bind('<Leave>', actualizarCantidadProducto)

    titPrecioProducto = tk.Label(marco, text="Precio del Producto:", bg='#ffccff', font=('Cambria', 20)).place(x=470, y=520)
    global precioProducto
    precioProducto= tk.Spinbox(marco, font=('Cambria', 20), width=19, from_=0, to=10000)
    precioProducto.place(x=470, y=570)
    precioProducto.bind('<Leave>', actualizarPrecioProducto)

    titClientes = tk.Label(marco, text="Productos", bg="#ffccff", font=("Cambria", 15)).place(x=1200, y=200)
    global productos_tree
    productos_tree = ttk.Treeview(marco)
    productos_tree['show'] = 'headings'
    # Definimos las columnas
    productos_tree['columns'] = ('NombreProducto', 'NombreProveedor', 'Cantidad', 'Descripcion')
    # Formateamos las columnas
    productos_tree.column('NombreProducto', width=100, anchor=tk.CENTER)
    productos_tree.column('NombreProveedor', width=100, anchor=tk.CENTER)
    productos_tree.column('Cantidad', width=100, anchor=tk.CENTER)
    productos_tree.column('Descripcion', width=200, anchor=tk.CENTER)
    # Titulos de columnas
    productos_tree.heading('NombreProducto', text='Nombre Proveedor')
    productos_tree.heading('NombreProveedor', text='Nombre Producto')
    productos_tree.heading('Cantidad', text='Cantidad')
    productos_tree.heading('Descripcion', text='Descripcion')
    # Insert Data
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()
    cursor.execute('SELECT NOMBREPROVEEDOR, NOMBRE, CANTIDAD, DESCRIPCION FROM productos')
    i = 0
    for ro in cursor:
        productos_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2], ro[3]))
        i = i + 1
    productos_tree.place(x=1000, y=250, height=400)

    global btnlgrabar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="EMITIR", width=10, height=1, anchor="center",
                      activebackground="blue", relief="raised",
                      borderwidth=5, font=("Cambria", 20), command=lambda: grabar())
    btnlgrabar.place(x=530, y=680)

