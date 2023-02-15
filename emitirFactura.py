import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import Tk, Button

def actualizarComboCliente(event):
    clienteIndex = nombreCliente.current()

def actualizarComboProveedor(event):
    proveedorIndex = nombreProveedor.current()

def actualizarProducto(event):
    productoIndex = producto.get()

def actualizarCantidadProducto(event):
    cantidad = cantProducto.get()

def actualizarPrecioProducto(event):
    precio = precioProducto.get()

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
    cblist = list()
    for row in cursor.execute('SELECT NOMBRE FROM clientes'):
        cblist.append(row)
    nombreCliente['values'] = (cblist)
    nombreCliente.place(x=100, y=300)
    nombreCliente.bind('<<ComboboxSelected>>', actualizarComboCliente)

    titProducto = tk.Label(marco, text="Indique el producto:", bg='#ffccff', font=('Cambria', 20)).place(x=470, y=350)
    global producto
    producto = tk.Entry(marco, font=('Cambria', 20))
    producto.place(x=470, y=400)
    producto.bind('<Leave>', actualizarProducto)

    titCantProducto = tk.Label(marco, text='Cantidad deseada:', bg='#ffccff', font=('Cambria', 20)).place(x=470, y=490)
    global cantProducto
    cantProducto = tk.Spinbox(marco, font=('Cambria', 20), width=19, from_=0, to=100)
    cantProducto.place(x=470, y=550)
    cantProducto.bind('<Leave>', actualizarCantidadProducto)

    titPrecioProducto = tk.Label(marco, text="Precio del Producto:", bg='#ffccff', font=('Cambria', 20)).place(x=470, y=620)
    global precioProducto
    precioProducto= tk.Spinbox(marco, font=('Cambria', 20), width=19, from_=0, to=10000)
    precioProducto.place(x=470, y=670)
    precioProducto.bind('<Leave>', actualizarPrecioProducto)

    titProveedor = tk.Label(marco, text="Seleccione al proveedor: ", bg="#ffccff", font=("Cambria", 20)).place(x=900, y=250)
    global nombreProveedor
    nombreProveedor = ttk.Combobox(marco, font=("Cambria", 15))
    cblist = list()
    for row in cursor.execute('SELECT NOMBRE FROM proveedores'):
        cblist.append(row)
    nombreProveedor['values'] = (cblist)
    nombreProveedor.place(x=900, y=300)
    nombreProveedor.bind('<<ComboboxSelected>>', actualizarComboProveedor)

    global btnlgrabar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="EMITIR", width=10, height=1, anchor="center",
                      activebackground="blue", relief="raised",
                      borderwidth=5, font=("Cambria", 20), command=lambda: grabar())
    btnlgrabar.place(x=530, y=800)

