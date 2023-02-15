# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 18:29:24 2022

@author: Alejandro Sierro Galan
"""

from tkinter import Tk, Button
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter.messagebox import *

def registros(where):
    connection = sqlite3.connect('base.db')
    cursor = connection.cursor()
    
    btnconsul['state'] = 'disabled'
    
    global ventana_nueva1
    ventana_nueva1 = tk.Toplevel()
    ventana_nueva1.geometry("1200x800")
    ventana_nueva1.title("Resultados de la BÃºsqueda")
    ventana_nueva1['bg']='#fb0'
    s=ttk.Style()
    s.theme_use('clam')
    s.configure('Treeview', rowheight=40)
    tabla = ttk.Treeview(ventana_nueva1, columns=("col1", "col2", "col3"))
    tabla.column("#0", width=120)
    tabla.column("col1", width=120, anchor="center")
    tabla.column("col2", width=500, anchor="center")
    tabla.column("col3", width=120, anchor="center")
    tabla.heading("#0", text="CÃDIGO", anchor="center")
    tabla.heading("col1", text="DENOMINACIÃN", anchor="center")
    tabla.heading("col2", text="DESCRIPCIÃN", anchor="center")
    tabla.heading("col3", text="CONSUMIBLE", anchor="center")
    
    registro = "select * from productos where 1 = 1" + where
    cursor.execute(registro)
    producto = cursor.fetchall()
       
    for (CODIGO,DENOMINACION,DESCRIPCION,CONSUMIBLE) in producto:
        
        tabla.insert('',tk.END,text=CODIGO,values=(DENOMINACION,DESCRIPCION,CONSUMIBLE))
        btnseguir = Button(ventana_nueva1)
        btnseguir.config(text="SALIR", width=10, height=2, anchor="center",
                 activebackground="blue", relief="raised", 
                 borderwidth=5, font =("Bahnschrift",11), command=lambda: continuar())
    btnseguir.place(x=350, y=500)
    tabla.pack()    

def continuar():
    ventana_nueva1.destroy()
    dato=tk.messagebox.askyesno(message="Â¿Desea continuar?", title="TÃ­tulo", parent=marco)
    if dato == True:
        btnconsul['state'] = 'normal'
        codpro.delete(0, 'end')
        denominacion.delete(0, 'end')
        descripcion.delete("1.0","end-1c")
        combobo.delete(0, 'end')
    elif dato ==  False:
        marco.destroy()


def actualizarcombo(event):
    index = combobo.current()
    
def actualizarcodigo(event):
    codigo = codpro.get()
    
def actualizardeno(event):
    denomina = denominacion.get()
    
def actualizardesc(event):
    descrip = descripcion.get("1.0","end-1c")
    

def buscar():
     connection = sqlite3.connect('base.db')
     cursor = connection.cursor()
     consumible=""
     codigo = codpro.get()
     denomina = denominacion.get()
     descrip = descripcion.get("1.0","end-1c")  
     index = combobo.current()
     if index == 0:
         consumible = "Perecedero"
     elif index == 1:
         consumible = "No Perecedero"
     
     where=""
     if len(codigo)>0 :
       where=where+" AND CODIGO='"+ codigo +"' "
     if len(denomina)>0 :
       where=where+" AND DENOMINACION='"+ denomina +"' "
     if len(descrip)>0 :
       where=where+" AND DESCRIPCION='"+ descrip +"' "
     if len(consumible)>0 :
       where=where+" AND CONSUMIBLE='"+ consumible +"' "
     registros(where)
     
          



def formconsul():
    global marco
    marco = tk.Tk()
    marco.title("Consultar Productos")
    marco.state('zoomed')
    marco.config(bg="pink")
    marco.grid_propagate(0)
    marco.iconbitmap("angelnegro.ico")
    
    etiqueta0=tk.Label(marco, text="                      CONSULTAR PRODUCTOS                      ", bg="white", font =("Bahnschrift",12)).grid(row=0, column=1, sticky="w", padx=10, pady=10)
    
    espacio1=tk.Label(marco, text="", bg="pink").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    espacio2=tk.Label(marco, text="", bg="pink").grid(row=2, column=0, sticky="w", padx=10, pady=10)
    espacio3=tk.Label(marco, text="", bg="pink").grid(row=3, column=0, sticky="w", padx=10, pady=10)
    espacio4=tk.Label(marco, text="", bg="pink").grid(row=4, column=0, sticky="w", padx=10, pady=10)
    etiqueta1=tk.Label(marco, text="CÃ³digo de producto", bg="white", font =("Bahnschrift",12)).grid(row=5, column=0, sticky="w", padx=10, pady=10)
    
    global codpro
    codpro=ttk.Entry(marco)
    codpro.grid(row=5, column=1, sticky="w", padx=10, pady=10)
    codpro.bind('<Leave>', actualizarcodigo)
    
    etiqueta2=tk.Label(marco, text="DenominaciÃ³n", bg="white", font =("Bahnschrift",12)).grid(row=6, column=0, sticky="w", padx=10, pady=10)
    
    global denominacion
    denominacion=tk.Entry(marco, width=100)
    denominacion.grid(row=6, column=1, sticky="w", padx=10, pady=10)
    denominacion.bind('<Leave>', actualizardeno)
    
    etiqueta3=tk.Label(marco,text="DescripciÃ³n", bg="white", font =("Bahnschrift",12)).grid(row=7, column=0, sticky="w", padx=10, pady=10)
    
    global descripcion
    descripcion=tk.Text(marco, width=100, height=6)
    barra = tk.Scrollbar(marco)#, orient=VERTICAL,
    barra.config(command=descripcion.yview, )
    descripcion["yscrollcommand"] = barra.set
    descripcion.grid(row=7, column=1, sticky="w", padx=10, pady=10)
    barra.grid(row=7, column=2, sticky="nsew")
    denominacion.bind('<Leave>', actualizardesc)
    
    etiqueta4=tk.Label(marco,text="Durabilidad", bg="white", font =("Bahnschrift",12)).grid(row=8, column=0, sticky="w", padx=10, pady=10)
    
    global combobo
    combobo=ttk.Combobox(marco)
    combobo['values'] = ("Perecedro", "No Perecedero")
    combobo.grid(row=8, column=1, sticky="w", padx=10, pady=10)
    combobo.bind('<<ComboboxSelected>>', actualizarcombo)
    
    espacio5=tk.Label(marco, text="", bg="pink").grid(row=9, column=0, sticky="w", padx=10, pady=10)
    espacio6=tk.Label(marco, text="", bg="pink").grid(row=10, column=0, sticky="w", padx=10, pady=10)
    espacio7=tk.Label(marco, text="", bg="pink").grid(row=11, column=0, sticky="w", padx=10, pady=10)
    espacio8=tk.Label(marco, text="", bg="pink").grid(row=12, column=0, sticky="w", padx=10, pady=10)
    
    global btnconsul
    btnconsul = Button(marco)
    btnconsul.config(text="CONSULTAR", width=10, height=2, anchor="center",
                 activebackground="blue", relief="raised", 
                 borderwidth=5, font =("Bahnschrift",11), command=lambda: buscar())
    btnconsul.grid(row=13, column=1, sticky="w", padx=100, pady=100)
    