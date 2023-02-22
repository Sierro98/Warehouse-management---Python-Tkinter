import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Button


def initFacturasEmitidas():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()
    global marco
    marco = tk.Tk()
    marco.title("Lista de Facturas")
    marco.state('zoomed')
    marco.config(bg="#ffccff")
    marco.iconbitmap("gas_mask_icon.ico")

    title = tk.Label(marco, text="Facturas Emitidas", bg='#ffccff', font=("Cambria 30 underline")).place(x=560, y=50)

    # Tabla de Facturas
    global facturas_tree
    facturas_tree = ttk.Treeview(marco)
    facturas_tree['show'] = 'headings'
    # Definimos las columnas
    facturas_tree['columns'] = ('CodigoFactura', 'NombreCliente', 'Nombre', 'Cantidad', 'Precio', 'PrecioTotal')
    # Formateamos las columnas
    facturas_tree.column('CodigoFactura', width=100, anchor=tk.CENTER)
    facturas_tree.column('NombreCliente', width=200, anchor=tk.CENTER)
    facturas_tree.column('Nombre', width=200, anchor=tk.CENTER)
    facturas_tree.column('Cantidad', width=100, anchor=tk.CENTER)
    facturas_tree.column('Precio', width=100, anchor=tk.CENTER)
    facturas_tree.column('PrecioTotal', width=100, anchor=tk.CENTER)
    # Titulos de columnas
    facturas_tree.heading('CodigoFactura', text='Codigo')
    facturas_tree.heading('NombreCliente', text='Nombre Cliente')
    facturas_tree.heading('Nombre', text='Nombre Producto')
    facturas_tree.heading('Cantidad', text='Cantidad')
    facturas_tree.heading('Precio', text='Precio')
    facturas_tree.heading('PrecioTotal', text='Precio Total')
    # Insert Data
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()
    cursor.execute('SELECT CODIGO, NOMBRECLIENTE, NOMBRE, CANTIDAD, PRECIO FROM facturas')
    i = 0
    for ro in cursor:
        total = ro[3] * ro[4]
        facturas_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2], ro[3], ro[4], total))
        i = i + 1
    facturas_tree.place(x=370, y=150, height=400)
