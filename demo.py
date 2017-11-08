# Demo text and image scraping incorporated into our animation framework 
# Web Scraping optional lecture
# 15-112 Fall 2017
# Daniel Wen

import tkinter
from PIL import Image, ImageTk
from scrape import getProducts


# Resize and process our images for Tkinter
def resizeImage(image, newWidth):
    width, height = image.size
    newHeight = newWidth * height // width
    image = image.resize((newWidth, newHeight), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)

def resizeImages(data):
    for product in data.products:
        product["image"] = resizeImage(product["image"], data.itemWidth)

def init(data):
    # Get list of products
    data.products = getProducts()
    data.marginX = 30
    data.marginY = 40
    data.spacing = 20
    data.cols = 3
    data.rowHeight = 150

    data.innerWidth = (data.width - data.marginX * 2) // data.cols
    data.itemWidth = data.innerWidth - data.spacing
    resizeImages(data)

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    for i, product in enumerate(data.products):
        row = i // data.cols
        col = i % data.cols
        x = data.marginX + data.spacing // 2 + col * data.innerWidth
        y = data.marginY + row * data.rowHeight
        
        itemHeight = data.rowHeight - data.spacing
        itemWidth = data.itemWidth

        # Product image
        canvas.create_image((x, y), image=product["image"], anchor="nw")

        # Product name
        canvas.create_text(x + itemWidth // 2, y + itemHeight - 18, anchor="s",
            text=product["name"], font="Helvetica 18")
        # Product price
        canvas.create_text(x + itemWidth // 2, y + itemHeight, anchor="s",
            text=product["price"], font="Helvetica 14")


# Need to move the call to init
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(tkinter.ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    init(data)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 500)