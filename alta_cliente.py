# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 18:29:24 2022

@author: a0b0m
"""


import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter.messagebox import *
from tkinter import Tk, Button


def actualizarcombo(event):
    index = ciudad.current()
    
def actualizarNombre(event):
    nombre = nombreCliente.get()

def actualizarTelefono(event):
    telefonoCliente = telefono.get()
    
def actualizardesc(event):
    descrip = descripcion.get("1.0","end-1c")
    
   

def grabar():
     connection = sqlite3.connect('almacen.db')
     cursor = connection.cursor()
  
     nombre = nombreCliente.get()
     telefonoCliente = telefono.get()
     descrip = descripcion.get("1.0","end-1c")  
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
     elif index == 5:
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
     cursor.execute(registro, [nombre, ciudadCliente,  telefonoCliente, descrip])
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
    
    dato=tk.messagebox.askyesno(message="¿Desea continuar?", title="Título", parent=marco)
    if dato == True:
        btnlgrabar['state'] = 'normal'
        nombreCliente.delete(0, 'end')
        telefono.delete(0, 'end')
        descripcion.delete("1.0","end-1c")
        ciudad.delete(0, 'end')
    elif dato ==  False:
        marco.destroy()
    

def aniadirCliente():
    global marco
    marco = tk.Tk()
    marco.title("Añadir Cliente")
    marco.state('zoomed')
    marco.config(bg="#ffccff")
    marco.grid_propagate(0)
    marco.iconbitmap("gas_mask_icon.ico")
    
    etiqueta0=tk.Label(marco, text="AÑADIR CLIENTE", bg='#ffccff', font =("Cambria 30 underline")).grid(row=0, column=1, sticky="w", padx=450, pady=30)
    
    espacio1=tk.Label(marco, text="", bg="#ffccff").grid(row=1, column=1, sticky="w", padx=10, pady=10)
    espacio2=tk.Label(marco, text="", bg="#ffccff").grid(row=2, column=1, sticky="w", padx=10, pady=10)
    espacio3=tk.Label(marco, text="", bg="#ffccff").grid(row=3, column=1, sticky="w", padx=10, pady=10)
    espacio4=tk.Label(marco, text="", bg="#ffccff").grid(row=4, column=1, sticky="w", padx=10, pady=10)
    
    etiqueta2=tk.Label(marco, text="Nombre Cliente", bg="#ffccff", font =("Cambria",20)).grid(row=6, column=0, sticky="w", padx=30, pady=20)
    global nombreCliente
    nombreCliente=tk.Entry(marco, width=100, font=("Cambria", 15))
    nombreCliente.grid(row=6, column=1, sticky="w", padx=10, pady=10)
    nombreCliente.bind('<Leave>', actualizarNombre)

    etiqueta3 = tk.Label(marco, text="Ciudad", bg="#ffccff", font=("Cambria", 20)).grid(row=7, column=0, sticky="w", padx=30, pady=20)
    global ciudad
    ciudad = ttk.Combobox(marco, font=("Cambria", 15))
    ciudad['values'] = ("Madrid", "Alcala de Henares", 'Villalba', 'Galapagar', 'Valdemoro', 'Alcobendas', 'Mostoles')
    ciudad.grid(row=7, column=1, sticky="w", padx=10, pady=10)
    ciudad.bind('<<ComboboxSelected>>', actualizarcombo)

    etiqueta4 = tk.Label(marco, text="Telefono del cliente", bg="#ffccff", font=("Cambria", 20)).grid(row=8, column=0, sticky="w", padx=30, pady=20)
    global telefono
    telefono = tk.Entry(marco, width=50, font=("Cambria", 15))
    telefono.grid(row=8, column=1, sticky="w", padx=10, pady=10)
    telefono.bind('<Leave>', actualizarTelefono)
        
    etiqueta5=tk.Label(marco,text="Descripción", bg="#ffccff", font =("Cambria",20)).grid(row=9, column=0, sticky="w", padx=30, pady=20)
    global descripcion
    descripcion=tk.Text(marco, width=100, height=6, font=("Cambria", 15))
    barra = tk.Scrollbar(marco)
    barra.config(command=descripcion.yview, )# orient=VERTICAL,
    descripcion["yscrollcommand"] = barra.set
    descripcion.grid(row=9, column=1, sticky="w", padx=10, pady=10)
    barra.grid(row=9, column=2, sticky="nsew")
    nombreCliente.bind('<Leave>', actualizardesc)

    espacio6=tk.Label(marco, text="", bg="#ffccff").grid(row=10, column=0, sticky="w", padx=10, pady=10)
    espacio7=tk.Label(marco, text="", bg="#ffccff").grid(row=11, column=0, sticky="w", padx=10, pady=10)
    espacio8=tk.Label(marco, text="", bg="#ffccff").grid(row=12, column=0, sticky="w", padx=10, pady=10)
    
    global btnlgrabar
    btnlgrabar = Button(marco)
    btnlgrabar.config(text="GRABAR", width=10, height=2, anchor="center",
                 activebackground="blue", relief="raised", 
                 borderwidth=5, font =("Cambria",20), command=lambda: grabar())
    btnlgrabar.grid(row=13, column=1, sticky="w", padx=100, pady=10)
    
    