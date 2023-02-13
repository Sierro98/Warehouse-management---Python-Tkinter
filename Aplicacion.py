# -*- coding: utf-8 -*-
"""
@author: Alejandro Sierro Galan
"""

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import Tk, Button

from alta_cliente import aniadirCliente
from alta_proveedor import aniadirProveedor
from emitirFactura import initEmitirFacturas
# from Bajas import formbajas
# from Modifica import formmod

def saludar(texto):
    print(texto)
    if texto == 'Añadir Cliente':
        messagebox.showinfo(message=texto, title="Elejiste:")
        aniadirCliente()
    elif texto == 'Añadir Proveedor':
        messagebox.showinfo(message=texto, title="Elejiste:")
        aniadirProveedor()
    elif texto == 'Emitir Facturas':
        messagebox.showinfo(message=texto, title="Elejiste:")
        initEmitirFacturas()
    elif texto == 'Facturas Emitidas':
        messagebox.showinfo(message=texto, title="Elejiste:")
        # formbajas()
    elif texto == 'SALIR':
        messagebox.showinfo(message=texto, title="Elejiste:")
        raiz.destroy()


btnsText = ['Añadir Cliente', 'Añadir Proveedor', 'Emitir Facturas', 'Facturas emitidas', 'SALIR']
z = 0
y = 0
raiz = Tk()
raiz.title("Almacén")
raiz.iconbitmap("gas_mask_icon.ico")
raiz.state('zoomed')
marco = Frame(raiz)
marco.config(bg="#ffccff")
marco.config(width="1920", height="1080", bd="10", relief="ridge")
marco.pack()

etiqueta = Label(marco, text='Bienvenido al almacen',bg="#ffccff", font=("Cambria 40 underline")).place(x=520, y=50)
btnlista = []
for n in range(len(btnsText)):
    btnlista.append(Button(marco))

for k in range(len(btnlista)):
    btnlista[k].config(text=btnsText[k], width=17, height=1, anchor="center",
                       activebackground="purple", relief="raised",
                       borderwidth=10, font=("Cambria", 20),
                       command=lambda m=btnsText[k]: saludar(m))
    btnlista[k].place(x=20 + z, y=150)
    z += 300

imagen = Image.open("almacen_img.png")
resize_imagen = imagen.resize((1000, 500))
img = ImageTk.PhotoImage(resize_imagen)
imagen = Label(marco, image=img, bg="blue", bd="10", relief="groove").place(x=250, y=250)

raiz.mainloop()
