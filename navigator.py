import tkinter as tk
from PIL import Image, ImageTk


def do_strelka():
    global vibor
    vibor = 'стрелка'
    print(vibor)


def do_metka():
    global vibor
    vibor = 'метка'
    print(vibor)


def do_put():
    global vibor
    vibor = 'путь'
    print(vibor)


def do_delete():
    global vibor
    vibor = 'удалить'
    print(vibor)


def do_stena():
    global vibor
    vibor = 'стена'
    print(vibor)


def do_polka():
    global vibor
    vibor = 'полка'
    print(vibor)


def motion(event):
    if vibor == 'стена':
        if x_stena != -1 and y_stena != -1:
            canvas.delete('stena')
            canvas.create_rectangle(x_stena, y_stena, event.x, event.y, fill="#E5E4E2", outline="#000000", tags='stena')
            # print(tag_object)
    elif vibor == 'полка':
        if x_polka != -1 and y_polka != -1:
            canvas.delete('polka')
            canvas.create_rectangle(x_polka, y_polka, event.x, event.y, fill="#E5E4E2", outline="#000000", tags='polka')

            len_x = abs(event.x - x_polka)
            t_x = len_x // (RADIUS * 10)
            for i in range(0, t_x + 1):
                canvas.create_oval(x_polka + (i * (len_x // (t_x + 1))), event.y,
                                   x_polka + (i * (len_x // (t_x + 1))) - 2 * RADIUS, event.y + 2 * RADIUS,
                                   fill='#FF8400',
                                   tags='polka')
                canvas.create_oval(x_polka + (i * (len_x // (t_x + 1))), y_polka,
                                   x_polka + (i * (len_x // (t_x + 1))) - 2 * RADIUS, y_polka - 2 * RADIUS,
                                   fill='#FF8400',
                                   tags='polka')
            len_y = abs(event.y - y_polka)
            t_y = len_y // (RADIUS * 10)
            for i in range(1, t_y + 1):
                canvas.create_oval(x_polka, y_polka + (i * (len_y // (t_y + 1))),
                                   x_polka - 2 * RADIUS, y_polka + (i * (len_y // (t_y + 1))) + 2 * RADIUS,
                                   fill='#FF8400', tags='polka')
                canvas.create_oval(event.x, y_polka + (i * (len_y // (t_y + 1))),
                                   event.x + 2 * RADIUS, y_polka + (i * (len_y // (t_y + 1))) + 2 * RADIUS,
                                   fill='#FF8400', tags='polka')

            canvas.create_oval(event.x, y_polka,
                               event.x + 2 * RADIUS, y_polka - 2 * RADIUS, fill='#FF8400', tags='polka')
            canvas.create_oval(event.x, event.y,
                               event.x + 2 * RADIUS, event.y + 2 * RADIUS, fill='#FF8400', tags='polka')

            # print(abs(event.x-x_polka)//(RADIUS*10))
    elif vibor == 'путь':
        if x_put != -1 and y_put != -1:
            canvas.delete('line')
            if event.x < x_put and event.y < y_put:
                canvas.create_line(x_put, y_put, event.x + 2, event.y - 2, tags='line')
            else:
                canvas.create_line(x_put, y_put, event.x - 2, event.y - 2, tags='line')


def b1(event):
    global tag_object
    if vibor == 'стена':
        global x_stena, y_stena
        if x_stena == -1 and y_stena == -1:
            x_stena = event.x
            y_stena = event.y

            root.bind('<Motion>', motion)
        else:
            canvas.delete('stena')
            canvas.create_rectangle(x_stena, y_stena, event.x, event.y, fill="#D5D5D5", outline="#000000",
                                    tags=str(tag_object))
            tag_object += 1
            x_stena, y_stena = -1, -1
    elif vibor == 'метка':
        canvas.create_oval(event.x - RADIUS, event.y - RADIUS,
                           event.x + RADIUS, event.y + RADIUS, fill='#FF2400', tags=str(tag_object))
        tag_object += 1
    elif vibor == 'путь':
        global x_put, y_put
        item = event.widget.find_withtag("current")
        item_type = canvas.type(item)

        if item_type == "oval":
            if x_put == -1 and y_put == -1:
                massiv_coordinat = canvas.coords(item)
                x_put = (massiv_coordinat[0] + massiv_coordinat[2]) // 2
                y_put = (massiv_coordinat[1] + massiv_coordinat[3]) // 2
                root.bind('<Motion>', motion)
            else:

                canvas.delete('line')
                # canvas.itemconfig(event.widget.find_withtag("current"), fill="blue")
                massiv_coordinat = canvas.coords(item)
                canvas.tag_lower(canvas.create_line(x_put, y_put, (massiv_coordinat[0] + massiv_coordinat[2]) // 2,
                                                    (massiv_coordinat[1] + massiv_coordinat[3]) // 2,
                                                    tags=str(tag_object), width=3, fill='blue'))
                canvas.itemconfig(event.widget.find_withtag("current"))
                tag_object += 1
                x_put, y_put = -1, -1
    elif vibor == 'полка':
        global x_polka, y_polka
        if x_polka == -1 and y_polka == -1:
            x_polka = event.x
            y_polka = event.y
            root.bind('<Motion>', motion)
        else:

            canvas.delete('polka')

            canvas.create_rectangle(x_polka, y_polka, event.x, event.y, fill="#D5D5D5", outline="#000000",
                                    tags=str(tag_object))
            tag_object += 1

            len_x = abs(event.x - x_polka)
            t_x = len_x // (RADIUS * 10)
            for i in range(0, t_x + 1):
                canvas.create_oval(x_polka + (i * (len_x // (t_x + 1))), event.y,
                                   x_polka + (i * (len_x // (t_x + 1))) - 2 * RADIUS, event.y + 2 * RADIUS,
                                   fill='#FF2400',
                                   tags=str(tag_object))
                tag_object += 1
                canvas.create_oval(x_polka + (i * (len_x // (t_x + 1))), y_polka,
                                   x_polka + (i * (len_x // (t_x + 1))) - 2 * RADIUS, y_polka - 2 * RADIUS,
                                   fill='#FF2400',
                                   tags=str(tag_object))
                tag_object += 1
            len_y = abs(event.y - y_polka)
            t_y = len_y // (RADIUS * 10)
            for i in range(1, t_y + 1):
                canvas.create_oval(x_polka, y_polka + (i * (len_y // (t_y + 1))),
                                   x_polka - 2 * RADIUS, y_polka + (i * (len_y // (t_y + 1))) + 2 * RADIUS,
                                   fill='#FF2400', tags=str(tag_object))
                tag_object += 1
                canvas.create_oval(event.x, y_polka + (i * (len_y // (t_y + 1))),
                                   event.x + 2 * RADIUS, y_polka + (i * (len_y // (t_y + 1))) + 2 * RADIUS,
                                   fill='#FF2400', tags=str(tag_object))
                tag_object += 1

            canvas.create_oval(event.x, y_polka,
                               event.x + 2 * RADIUS, y_polka - 2 * RADIUS, fill='#FF2400', tags=str(tag_object))
            tag_object += 1
            canvas.create_oval(event.x, event.y,
                               event.x + 2 * RADIUS, event.y + 2 * RADIUS, fill='#FF2400', tags=str(tag_object))
            tag_object += 1
            x_polka, y_polka = -1, -1


    elif vibor == 'удалить':
        # res=event.widget.find_closest(event.x, event.y) # ctrl z
        canvas.delete(event.widget.find_withtag("current"))
        print(event.widget.find_withtag("current"))


vibor = 'стрелка'  # 'стрелка','стена','метка','путь','удалить'
x_stena, y_stena = -1, -1
x_put, y_put = -1, -1
x_polka, y_polka = -1, -1

tag_object = 0
root = tk.Tk()
root.geometry("800x650")

SIZE = 80
RADIUS = 5

image_strelka = ImageTk.PhotoImage(image=Image.open("стрелка.png").resize((SIZE, SIZE), Image.LANCZOS))
button_strelka = tk.Button(root, image=image_strelka, command=do_strelka)
button_strelka.place(x=10, y=10)

image_metka = ImageTk.PhotoImage(image=Image.open("метка.png").resize((SIZE, SIZE), Image.LANCZOS))
button_metka = tk.Button(root, image=image_metka, command=do_metka)
button_metka.place(x=10, y=100)

image_put = ImageTk.PhotoImage(image=Image.open("путь.png").resize((SIZE, SIZE), Image.LANCZOS))
button_put = tk.Button(root, image=image_put, command=do_put)
button_put.place(x=10, y=190)

image_stena = ImageTk.PhotoImage(image=Image.open("стена.jpg").resize((SIZE, SIZE), Image.LANCZOS))
button_stena = tk.Button(root, image=image_stena, command=do_stena)
button_stena.place(x=10, y=280)

image_polka = ImageTk.PhotoImage(image=Image.open("полка.jpg").resize((SIZE, SIZE), Image.LANCZOS))
button_polka = tk.Button(root, image=image_polka, command=do_polka)
button_polka.place(x=10, y=370)

image_delete = ImageTk.PhotoImage(image=Image.open("удалить.jpeg").resize((SIZE, SIZE), Image.LANCZOS))
button_delete = tk.Button(root, image=image_delete, command=do_delete)
button_delete.place(x=10, y=460)

canvas = tk.Canvas(bg="white", width=650, height=600)
canvas.place(x=10 + SIZE + 10, y=10)

canvas.bind('<Button-1>', b1)

root.mainloop()
