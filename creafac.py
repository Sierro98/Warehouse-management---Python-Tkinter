# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 18:27:51 2023

@author: Alejandro Sierro Galan
"""
# conda install -c anaconda reportlab

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def pintarlogo():
    img = ImageReader("logo.png")
    c.drawImage(img, 0, h - 90, width=80, height=80)


def pintarcabecera():
    x = 50
    y = h - 100
    c.line(x, y, x + 500, y)
    c.drawString(200, h - 50, "FACTURA")
    c.line(x, y+100, x + 500, y+100)


def leerf(f):
    with open('Factura.txt') as f:
        for linea in f:
            lista.append(linea)
            


lista = []
z = 0
global h
global w
w, h = A4
margsup = 210
entrecols = 15

c = canvas.Canvas("Factura.pdf")

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