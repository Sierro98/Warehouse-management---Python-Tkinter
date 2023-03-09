# -*- coding: utf-8 -*-
"""
@author: Alejandro Sierro Galan
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


global idFact
def pintarlogo():
    img = ImageReader("almacenIcono.png")
    c.drawImage(img, 50, h - 120, width=80, height=80)


def leerf():
    with open('Factura.txt') as f:
        for linea in f:
            lista.append(linea)
            

def ejecutar(idFactura):
    idFact = idFactura
    global lista
    lista = []
    z = 0
    global h
    global w
    w, h = A4

    global c
    c = canvas.Canvas(f'Factura{idFactura}.pdf')

    pintarlogo()

    x = 50
    c.setFont("Helvetica", 30)
    c.drawString(210, h - 100, f'FACTURA nº{idFact}')
    c.line(x, h - 130, x + 500, h - 130)

    leerf()
    c.setFont("Helvetica", 20)

    for dato in lista:
        dato = dato.rstrip()
        c.drawString(45, 620 - z, dato)
        z+=50
    c.drawString(150, 50, 'Factura generada por Alejandro Sierro Galán')

    c.showPage()
    c.save()