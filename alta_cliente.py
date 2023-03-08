# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 18:29:24 2022

@author: Alejandro Sierro Galan
"""

import tkinter as tk
from tkinter import ttk, W
import sqlite3
from tkinter.messagebox import *
from tkinter import Tk, Button

def actualizarTabla():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    clientes_tree.delete(*clientes_tree.get_children())
    cursor.execute('SELECT CODIGO, NOMBRE, CIUDAD, TELEFONO, DESCRIPCION FROM clientes')
    i = 0
    for ro in cursor:
        clientes_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2], ro[3], ro[4]))
        i = i + 1

    cursor.close()
    connection.close()

def onSelected(event):
    limpiarCampos()
    for selItem in clientes_tree.selection():
        item = clientes_tree.item(selItem)
        codigo, nombre, ciu, telef, des = item["values"][0:5]
        global codigoSelected
        codigoSelected = int(codigo)
        nombreCliente.insert(0, nombre)
        telefono.insert(0, telef)
        descripcion.insert("1.0", des)
        ciudad.insert(0, ciu)

def limpiarCampos():
    nombreCliente.delete(0, 'end')
    telefono.delete(0, 'end')
    descripcion.delete("1.0", "end-1c")
    ciudad.delete(0, 'end')

def modificar():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    nombre = nombreCliente.get()
    telefonoCliente = telefono.get()
    descrip = descripcion.get("1.0", "end-1c")
    index = ciudad.current()
    if index == 0:
        ciudadCliente = "Madrid"
    elif index == 1:
        ciudadCliente = "Alcala de Henares"
    elif index == 2:
        ciudadCliente = "Villalba"
    elif index == 3:
        ciudadCliente = "Galapagar"
    elif index == 4:
        ciudadCliente = "Valdemoro"
    elif index == 5:
        ciudadCliente = "Alcobendas"
    elif index == 6:
        ciudadCliente = "Mostoles"

    update = 'UPDATE clientes SET NOMBRE = ?, CIUDAD = ?, TELEFONO = ?, DESCRIPCION = ? WHERE CODIGO = ?'

    cursor.execute(update, [nombre, ciudadCliente, telefonoCliente, descrip, codigoSelected])
    connection.commit()
    actualizarTabla()
    cursor.close()
    connection.close()
def borrar():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    borrar = 'DELETE FROM clientes WHERE CODIGO = ?'
    cursor.execute(borrar, [codigoSelected])
    connection.commit()
    actualizarTabla()
    cursor.close()
    connection.close()

def actualizarcombo(event):
    index = ciudad.current()


def actualizarNombre(event):
    nombre = nombreCliente.get()


def actualizarTelefono(event):
    telefonoCliente = telefono.get()


def actualizardesc(event):
    descrip = descripcion.get("1.0", "end-1c")


def grabar():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()

    nombre = nombreCliente.get()
    telefonoCliente = telefono.get()
    descrip = descripcion.get("1.0", "end-1c")
    index = ciudad.current()
    if index == 0:
        ciudadCliente = "Madrid"
    elif index == 1:
        ciudadCliente = "Alcala de Henares"
    elif index == 2:
        ciudadCliente = "Villalba"
    elif index == 3:
        ciudadCliente = "Galapagar"
    elif index == 4:
        ciudadCliente = "Valdemoro"
    elif index == 5:
        ciudadCliente = "Alcobendas"
    elif index == 6:
        ciudadCliente = "Mostoles"

    try:
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS clientes (
                            CODIGO INTEGER PRIMARY KEY AUTOINCREMENT,
                            NOMBRE VARCHAR(40) NOT NULL,
                            CIUDAD VARCHAR(40) NOT NULL,
                            TELEFONO INT NOT NULL,
                            DESCRIPCION TEXT NOT NULL)
                   
                        ''')
        print("Tabla creada correctamente")
    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

    registro = "INSERT INTO clientes (NOMBRE, CIUDAD, TELEFONO, DESCRIPCION) VALUES(?, ?, ?, ?)"
    cursor.execute(registro, [nombre, ciudadCliente, telefonoCliente, descrip])

    clientes_tree.delete(*clientes_tree.get_children())
    cursor.execute('SELECT CODIGO, NOMBRE, CIUDAD, TELEFONO, DESCRIPCION FROM clientes')
    i = 0
    for ro in cursor:
        clientes_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2], ro[3], ro[4]))
        i = i + 1

    connection.commit()
    mostrar()
    continuar()


def mostrar():
    try:
        btnlgrabar['state'] = 'disabled'
        conexion = sqlite3.connect("almacen.db")
        cursor = conexion.cursor()
        registro = "SELECT * FROM clientes;"
        cursor.execute(registro)
        producto = cursor.fetchall()
        print(producto)

    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)


def continuar():
    dato = tk.messagebox.askyesno(message="¿Desea continuar?", title="Título", parent=marco)
    if dato == True:
        btnlgrabar['state'] = 'normal'
        limpiarCampos()
    elif dato == False:
        marco.destroy()


def aniadirCliente():
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()
    try:
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS clientes (
                            CODIGO INTEGER PRIMARY KEY AUTOINCREMENT,
                            NOMBRE VARCHAR(40) NOT NULL,
                            CIUDAD VARCHAR(40) NOT NULL,
                            TELEFONO INT NOT NULL,
                            DESCRIPCION TEXT NOT NULL)

                        ''')
        print("Tabla creada correctamente")
    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

    connection.commit()
    cursor.close()
    connection.close()

    global marco
    marco = tk.Tk()
    marco.title("Añadir Cliente")
    marco.state('zoomed')
    marco.config(bg="#ffccff")
    marco.grid_propagate(0)
    marco.iconbitmap("gas_mask_icon.ico")

    etiqueta0 = tk.Label(marco, text="AÑADIR CLIENTE", bg='#ffccff', font=("Cambria 30 underline")).grid(row=0,
                                                                                                         column=1,
                                                                                                         sticky="w",
                                                                                                         padx=450,
                                                                                                         pady=30)

    espacio1 = tk.Label(marco, text="", bg="#ffccff").grid(row=1, column=1, sticky="w", padx=10, pady=10)
    espacio2 = tk.Label(marco, text="", bg="#ffccff").grid(row=2, column=1, sticky="w", padx=10, pady=10)

    etiqueta2 = tk.Label(marco, text="Nombre Cliente", bg="#ffccff", font=("Cambria", 20)).grid(row=4, column=0,
                                                                                                sticky="w", padx=30,
                                                                                                pady=20)
    global nombreCliente
    nombreCliente = tk.Entry(marco, width=50, font=("Cambria", 15))
    nombreCliente.grid(row=4, column=1, sticky="w", padx=10, pady=10)
    nombreCliente.bind('<Leave>', actualizarNombre)

    etiqueta3 = tk.Label(marco, text="Ciudad", bg="#ffccff", font=("Cambria", 20)).grid(row=5, column=0, sticky="w",
                                                                                        padx=30, pady=20)
    global ciudad
    ciudad = ttk.Combobox(marco, width=50, font=("Cambria", 15))
    ciudad['values'] = ("Madrid", "Alcala de Henares", 'Villalba', 'Galapagar', 'Valdemoro', 'Alcobendas', 'Mostoles')
    ciudad.grid(row=5, column=1, sticky="w", padx=10, pady=10)
    ciudad.bind('<<ComboboxSelected>>', actualizarcombo)

    etiqueta4 = tk.Label(marco, text="Telefono del cliente", bg="#ffccff", font=("Cambria", 20)).grid(row=6, column=0,
                                                                                                      sticky="w",
                                                                                                      padx=30, pady=20)
    global telefono
    telefono = tk.Entry(marco, width=50, font=("Cambria", 15))
    telefono.grid(row=6, column=1, sticky="w", padx=10, pady=10)
    telefono.bind('<Leave>', actualizarTelefono)

    etiqueta5 = tk.Label(marco, text="Descripción", bg="#ffccff", font=("Cambria", 20)).grid(row=7, column=0,
                                                                                             sticky="w", padx=30,
                                                                                             pady=20)
    global descripcion
    descripcion = tk.Text(marco, width=50, height=6, font=("Cambria", 15))
    barra = tk.Scrollbar(marco)
    barra.config(command=descripcion.yview)  # orient=VERTICAL,
    descripcion["yscrollcommand"] = barra.set
    descripcion.grid(row=7, column=1, sticky="w", pady=10)
    barra.place(x=850, y=470, height=150)
    nombreCliente.bind('<Leave>', actualizardesc)

    titClientes = tk.Label(marco, text="Clientes", bg="#ffccff", font=("Cambria", 15)).place(x=1150, y=200)
    global clientes_tree
    clientes_tree = ttk.Treeview(marco)
    clientes_tree['show'] = 'headings'
    #Definimos las columnas
    clientes_tree['columns'] = ('Codigo', 'Nombre', 'Ciudad', 'Telefono', 'Descripcion')
    #Formateamos las columnas
    clientes_tree.column('Codigo', width=50, anchor=tk.CENTER)
    clientes_tree.column('Nombre', width=100, anchor=tk.CENTER)
    clientes_tree.column('Ciudad', width=150, anchor=tk.CENTER)
    clientes_tree.column('Telefono', width=100, anchor=tk.CENTER)
    clientes_tree.column('Descripcion', width=200, anchor=tk.CENTER)
    #Titulos de columnas
    clientes_tree.heading('Codigo', text='Codigo')
    clientes_tree.heading('Nombre', text='Nombre')
    clientes_tree.heading('Ciudad', text='Ciudad')
    clientes_tree.heading('Telefono', text='Telefono')
    clientes_tree.heading('Descripcion', text='Descripcion')
    #Insert Data
    connection = sqlite3.connect('almacen.db')
    cursor = connection.cursor()
    cursor.execute('SELECT CODIGO, NOMBRE, CIUDAD, TELEFONO, DESCRIPCION FROM clientes')
    i=0
    for ro in cursor:
        clientes_tree.insert('', i, text='', values=(ro[0], ro[1], ro[2], ro[3], ro[4]))
        i = i + 1
    clientes_tree.bind("<<TreeviewSelect>>", onSelected)
    clientes_tree.place(x=900, y=250, height=400)
    espacio6 = tk.Label(marco, text="", bg="#ffccff").grid(row=10, column=0, sticky="w", padx=10, pady=10)


    global btnlgrabar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="GRABAR", width=10, height=2, anchor="center",
                      activebackground="blue", relief="raised",
                      borderwidth=5, font=("Cambria", 20), command=lambda: grabar())
    btnlgrabar.grid(row=10, column=1, sticky="w", padx=100, pady=10)

    global btnModificar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="MODIFICAR", width=10, height=2, anchor="center",
                      activebackground="blue", relief="raised",
                      borderwidth=5, font=("Cambria", 20), command=lambda: modificar())
    btnlgrabar.place(x=200, y=600)

    global btnBorrar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="BORRAR", width=10, height=2, anchor="center",
                      activebackground="blue", relief="raised",
                      borderwidth=5, font=("Cambria", 20), command=lambda: borrar())
    btnlgrabar.place(x=590, y=600)
