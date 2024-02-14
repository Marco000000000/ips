import os

from PIL import Image, ImageDraw


def segna(token, x, y):
    im = Image.open(os.getcwd() + "/static/uploads/" + token + ".jpg")
    dr = ImageDraw.Draw(im)
    dr.ellipse((x - 7, y - 7, x + 7, y + 7), fill='red', outline='red')
    # im.show()
    im.save(os.getcwd() + "/static/uploads/" + token + "_punto.jpg")


def mappa(token, x, y):
    im = Image.open(os.getcwd() + "/static/uploads/" + token + ".jpg")
    dr = ImageDraw.Draw(im)
    dr.ellipse((x - 7, y - 7, x + 7, y + 7), fill='green', outline='green')
    # im.show()
    im.save(os.getcwd() + "/static/uploads/" + token + ".jpg")
    im.save(os.getcwd() + "/static/data/" + token + "_pnt.png")
