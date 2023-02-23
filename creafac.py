# -*- coding: utf-8 -*-
"""
@author: Alejandro Sierro Galan
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def pintarlogo():
    img = ImageReader("almacenIcono.png")
    c.drawImage(img, 50, h - 90, width=80, height=80)


def pintarcabecera():
    x = 50
    y = h - 100
    c.line(x, y, x + 500, y)
    c.drawString(280, h - 50, "FACTURA")
    c.line(x, y+100, x + 500, y+100)


def leerf(f):
    with open('Factura.txt') as f:
        for linea in f:
            lista.append(linea)
            

def ejecutar(idFactura):
    global lista
    lista = []
    z = 0
    global h
    global w
    w, h = A4
    margsup = 210
    entrecols = 15

    global c
    c = canvas.Canvas(f'Factura{idFactura}.pdf')

    pintarlogo()
    pintarcabecera()
    nomarch = "Factura.txt"
    leerf(nomarch)
    c.setFont("Helvetica", 10)
    for dato in lista:
        xlist = [10, 200]    #comienzo y final de cada lineo horizontal de la tabla
        ylist = [h - margsup - i*entrecols for i in range(len(lista) + 1)]
        c.grid(xlist, ylist)

    for dato in lista:
        dato = dato.rstrip()
        c.drawString(12, 620 - z, dato)
        z+=15


    c.showPage()
    c.save()