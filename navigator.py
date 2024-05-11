import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as fd


def do_vibor(stroka):
    global vibor, x_polka, y_polka, x_stena, y_stena, x_put, y_put
    vibor = stroka
    if vibor == 'метка':
        canvas.bind('<Motion>', motion)
    x_stena, y_stena = -1, -1
    x_put, y_put = -1, -1
    x_polka, y_polka = -1, -1
    canvas.delete('metka')
    canvas.delete('polka')
    canvas.delete('line')
    canvas.delete('stena')
    print(vibor)


def motion(event):
    if vibor == 'стена':
        if x_stena != -1 and y_stena != -1:
            canvas.delete('stena')
            canvas.create_rectangle(x_stena, y_stena, (event.x // SIZE_GRID) * SIZE_GRID,
                                    (event.y // SIZE_GRID) * SIZE_GRID, fill="#E5E4E2", outline="#000000", tags='stena')
            # print(tag_object)
    elif vibor == 'полка':
        if x_polka != -1 and y_polka != -1:
            if event.x > x_polka and event.y > y_polka:  # присвоить 4 переменным координаты(min,max по x,y) и считать всё с ними
                canvas.delete('polka')
                canvas.create_rectangle(x_polka, y_polka, (event.x // SIZE_GRID) * SIZE_GRID,
                                        (event.y // SIZE_GRID) * SIZE_GRID, fill="#E5E4E2", outline="#000000",
                                        tags='polka')

                len_x = abs((event.x // SIZE_GRID) * SIZE_GRID - x_polka)
                t_x = max(int(len_x // (RADIUS * SIZE_GRID // _SIZE_SCALE * 10)), 1)
                for i in range(1, t_x + 1):
                    canvas.create_oval(x_polka + (i * (len_x // (t_x + 1))) + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       (event.y // SIZE_GRID) * SIZE_GRID,
                                       x_polka + (i * (len_x // (t_x + 1))) - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       (event.y // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       fill='#FF8400',
                                       tags='polka')
                    canvas.create_oval(x_polka + (i * (len_x // (t_x + 1))) + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       y_polka,
                                       x_polka + (i * (len_x // (t_x + 1))) - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       y_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       fill='#FF8400',
                                       tags='polka')
                len_y = abs((event.y // SIZE_GRID) * SIZE_GRID - y_polka)
                t_y = max(int(len_y // (RADIUS * SIZE_GRID // _SIZE_SCALE * 10)), 1)
                for i in range(1, t_y + 1):
                    canvas.create_oval(x_polka,
                                       y_polka + (i * (len_y // (t_y + 1))) - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       x_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       y_polka + (i * (len_y // (t_y + 1))) + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       fill='#FF8400', tags='polka')
                    canvas.create_oval((event.x // SIZE_GRID) * SIZE_GRID,
                                       y_polka + (i * (len_y // (t_y + 1))) - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       (event.x // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       y_polka + (i * (len_y // (t_y + 1))) + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       fill='#FF8400', tags='polka')

                canvas.create_oval(x_polka, y_polka,
                                   x_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   y_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2, fill='#FF8400', tags='polka')

                canvas.create_oval(x_polka, (event.y // SIZE_GRID) * SIZE_GRID,
                                   x_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   (event.y // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   fill='#FF8400',
                                   tags='polka')
                canvas.create_oval((event.x // SIZE_GRID) * SIZE_GRID, y_polka,
                                   (event.x // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   y_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2, fill='#FF8400',
                                   tags='polka')
                canvas.create_oval((event.x // SIZE_GRID) * SIZE_GRID, (event.y // SIZE_GRID) * SIZE_GRID,
                                   (event.x // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   (event.y // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   fill='#FF8400', tags='polka')
    elif vibor == 'путь':
        if x_put != -1 and y_put != -1:
            canvas.delete('line')
            if event.x < x_put and event.y < y_put:
                canvas.create_line(x_put, y_put, event.x + 2, event.y - 2, tags='line')
            else:
                canvas.create_line(x_put, y_put, event.x - 2, event.y - 2, tags='line')
    elif vibor == 'метка':
        canvas.delete('metka')
        q = max(SIZE_GRID // 2, 1)
        canvas.create_oval((event.x // q) * q - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                           (event.y // q) * q - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                           (event.x // q) * q + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                           (event.y // q) * q + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                           fill='#FF8400', tags='metka')
    elif vibor == 'перемещение':
        if moving_status:
            global last_x, last_y
            for obj in canvas.find_all():
                if canvas.gettags(obj)[0] != 'setka':
                    canvas.move(obj, (event.x - last_x) * SIZE_GRID // 2, (event.y - last_y) * SIZE_GRID // 2)
            last_x = event.x
            last_y = event.y
        else:
            return


def on_press(event):
    global tag_object
    if vibor == 'стена':
        global x_stena, y_stena
        if x_stena == -1 and y_stena == -1:
            x_stena = (event.x // SIZE_GRID) * SIZE_GRID
            y_stena = (event.y // SIZE_GRID) * SIZE_GRID

            root.bind('<Motion>', motion)
        else:
            canvas.delete('stena')
            canvas.create_rectangle(x_stena, y_stena, (event.x // SIZE_GRID) * SIZE_GRID,
                                    (event.y // SIZE_GRID) * SIZE_GRID, fill="#D5D5D5", outline="#000000",
                                    tags=str(tag_object))
            tag_object += 1
            x_stena, y_stena = -1, -1
    elif vibor == 'метка':
        canvas.delete('metka')
        q = max(SIZE_GRID // 2, 1)
        canvas.create_oval((event.x // q) * q - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                           (event.y // q) * q - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                           (event.x // q) * q + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                           (event.y // q) * q + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                           fill='#FF2400', tags=str(tag_object))
        tag_object += 1
    elif vibor == 'путь':
        global x_put, y_put
        item = event.widget.find_withtag("current")
        item_type = canvas.type(item)
        if SIZE_GRID > 1:
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
                    canvas.delete('setka')
                    for line1 in range(0, width, int(SIZE_GRID)):
                        canvas.tag_lower(canvas.create_line((line1, 0), (line1, height), fill='#DCDCDC', tags='setka'))

                    for line1 in range(0, height, int(SIZE_GRID)):
                        canvas.tag_lower(canvas.create_line((0, line1), (width, line1), fill='#DCDCDC', tags='setka'))

                    canvas.itemconfig(event.widget.find_withtag("current"))
                    tag_object += 1
                    x_put, y_put = -1, -1
        else:
            print('слишком маленький масштаб')
    elif vibor == 'полка':
        global x_polka, y_polka
        if x_polka == -1 and y_polka == -1:
            x_polka = (event.x // SIZE_GRID) * SIZE_GRID
            y_polka = (event.y // SIZE_GRID) * SIZE_GRID
            root.bind('<Motion>', motion)
        else:
            if event.x > x_polka and event.y > y_polka:

                canvas.delete('polka')

                canvas.create_rectangle(x_polka, y_polka, (event.x // SIZE_GRID) * SIZE_GRID,
                                        (event.y // SIZE_GRID) * SIZE_GRID, fill="#D5D5D5", outline="#000000",
                                        tags=str(tag_object))
                tag_object += 1

                len_x = abs((event.x // SIZE_GRID) * SIZE_GRID - x_polka)
                t_x = max(int(len_x // (RADIUS * SIZE_GRID // _SIZE_SCALE * 10)), 1)
                for i in range(1, t_x + 1):
                    canvas.create_oval(x_polka + (i * (len_x // (t_x + 1))) + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       (event.y // SIZE_GRID) * SIZE_GRID,
                                       x_polka + (i * (len_x // (t_x + 1))) - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       (event.y // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       fill='#FF2400',
                                       tags=str(tag_object))
                    tag_object += 1
                    canvas.create_oval(x_polka + (i * (len_x // (t_x + 1))) + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       y_polka,
                                       x_polka + (i * (len_x // (t_x + 1))) - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       y_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       fill='#FF2400',
                                       tags=str(tag_object))
                    tag_object += 1

                len_y = abs((event.y // SIZE_GRID) * SIZE_GRID - y_polka)
                t_y = max(int(len_y // (RADIUS * SIZE_GRID // _SIZE_SCALE * 10)), 1)
                for i in range(1, t_y + 1):
                    canvas.create_oval(x_polka,
                                       y_polka + (i * (len_y // (t_y + 1))) - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       x_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       y_polka + (i * (len_y // (t_y + 1))) + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       fill='#FF2400', tags=str(tag_object))
                    tag_object += 1
                    canvas.create_oval((event.x // SIZE_GRID) * SIZE_GRID,
                                       y_polka + (i * (len_y // (t_y + 1))) - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       (event.x // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       y_polka + (i * (len_y // (t_y + 1))) + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                       fill='#FF2400', tags=str(tag_object))
                    tag_object += 1

                canvas.create_oval(x_polka, y_polka,
                                   x_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   y_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2, fill='#FF2400',
                                   tags=str(tag_object))
                tag_object += 1
                canvas.create_oval(x_polka, (event.y // SIZE_GRID) * SIZE_GRID,
                                   x_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   (event.y // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   fill='#FF2400',
                                   tags=str(tag_object))
                tag_object += 1
                canvas.create_oval((event.x // SIZE_GRID) * SIZE_GRID, y_polka,
                                   (event.x // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   y_polka - 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2, fill='#FF2400',
                                   tags=str(tag_object))
                tag_object += 1
                canvas.create_oval((event.x // SIZE_GRID) * SIZE_GRID, (event.y // SIZE_GRID) * SIZE_GRID,
                                   (event.x // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   (event.y // SIZE_GRID) * SIZE_GRID + 2 * RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                                   fill='#FF2400', tags=str(tag_object))
                tag_object += 1
                x_polka, y_polka = -1, -1
    elif vibor == 'удалить':
        # res=event.widget.find_closest(event.x, event.y) # ctrl z
        if canvas.gettags(canvas.find_closest(event.x, event.y)[0])[0] != 'setka':
            canvas.delete(event.widget.find_withtag("current"))
        print(event.widget.find_withtag("current"))
    elif vibor == 'перемещение':
        global last_x, last_y, moving_status
        last_x = event.x
        last_y = event.y
        moving_status = not moving_status
        canvas.bind('<Motion>', motion)


def scale_all(event):
    global SIZE_GRID
    x_scale = 2 if event.delta > 0 else 0.5
    y_scale = 2 if event.delta > 0 else 0.5
    if 128 >= SIZE_GRID * x_scale >= 1:
        SIZE_GRID *= x_scale
        global x_stena, y_stena
        if x_stena != -1 and y_stena != -1:
            x_stena = x_stena * x_scale
            y_stena = y_stena * y_scale
        global x_put, y_put
        if x_put != -1 and y_put != -1:
            x_put = x_put * x_scale
            y_put = y_put * y_scale
        global x_polka, y_polka
        if x_polka != -1 and y_polka != -1:
            x_polka = x_polka * x_scale
            y_polka = y_polka * y_scale

        canvas.delete('setka')
        canvas.scale('all', 0, 0, x_scale, y_scale)
        for line1 in range(0, width, int(SIZE_GRID)):
            canvas.tag_lower(canvas.create_line((line1, 0), (line1, height), fill='#DCDCDC', tags='setka'))

        for line1 in range(0, height, int(SIZE_GRID)):
            canvas.tag_lower(canvas.create_line((0, line1), (width, line1), fill='#DCDCDC', tags='setka'))


def save_objects():
    file_path = fd.asksaveasfilename(defaultextension='.txt')
    with open(file_path, 'w') as file:
        file.write(str(SIZE_GRID) + '\n')
        for obj in canvas.find_all():
            if canvas.gettags(obj)[0] != 'setka':
                file.write(
                    f"{canvas.type(obj)} {canvas.gettags(obj)[0]} {canvas.itemcget(obj, 'fill')} {canvas.coords(obj)}\n")


def load_objects():
    global tag_object, SIZE_GRID
    file_path = fd.askopenfilename(filetypes=[('Text Files', '*.txt')])
    with open(file_path, 'r') as file:
        SIZE_GRID = int(file.readline())
        canvas.delete('all')
        for line1 in range(0, width, int(SIZE_GRID)):
            canvas.tag_lower(canvas.create_line((line1, 0), (line1, height), fill='#DCDCDC', tags='setka'))
        for line1 in range(0, height, int(SIZE_GRID)):
            canvas.tag_lower(canvas.create_line((0, line1), (width, line1), fill='#DCDCDC', tags='setka'))

        for line2 in file:
            obj_type = line2.split()[0]
            obj_tag = line2.split()[1]
            obj_color = line2.split()[2]
            coords = ' '.join(map(str, line2.split()[3:]))
            tag_object = int(obj_tag) + 1
            eval(f'canvas.create_{obj_type}({eval(coords)},fill="{obj_color}",tags="{obj_tag}")')


vibor = 'стрелка'  # выбор режима
x_stena, y_stena = -1, -1
x_put, y_put = -1, -1
x_polka, y_polka = -1, -1
last_x, last_y = -1, -1
moving_status = False

tag_object = 0
root = tk.Tk()
root.geometry("800x650")

_SIZE_SCALE = 8
SIZE = 80
RADIUS = _SIZE_SCALE
SIZE_GRID = _SIZE_SCALE

image_strelka = ImageTk.PhotoImage(image=Image.open("стрелка.png").resize((SIZE, SIZE), Image.LANCZOS))
button_strelka = tk.Button(root, image=image_strelka, command=lambda: do_vibor('стрелка'))
button_strelka.place(x=10, y=10)

image_metka = ImageTk.PhotoImage(image=Image.open("метка.png").resize((SIZE, SIZE), Image.LANCZOS))
button_metka = tk.Button(root, image=image_metka, command=lambda: do_vibor('метка'))
button_metka.place(x=10, y=100)

image_put = ImageTk.PhotoImage(image=Image.open("путь.png").resize((SIZE, SIZE), Image.LANCZOS))
button_put = tk.Button(root, image=image_put, command=lambda: do_vibor('путь'))
button_put.place(x=10, y=190)

image_stena = ImageTk.PhotoImage(image=Image.open("стена.jpg").resize((SIZE, SIZE), Image.LANCZOS))
button_stena = tk.Button(root, image=image_stena, command=lambda: do_vibor('стена'))
button_stena.place(x=10, y=280)

image_polka = ImageTk.PhotoImage(image=Image.open("полка.jpg").resize((SIZE, SIZE), Image.LANCZOS))
button_polka = tk.Button(root, image=image_polka, command=lambda: do_vibor('полка'))
button_polka.place(x=10, y=370)

image_move = ImageTk.PhotoImage(image=Image.open("перемещение.png").resize((SIZE, SIZE), Image.LANCZOS))
button_move = tk.Button(root, image=image_move, command=lambda: do_vibor('перемещение'))
button_move.place(x=10, y=460)

image_delete = ImageTk.PhotoImage(image=Image.open("удалить.jpeg").resize((SIZE, SIZE), Image.LANCZOS))
button_delete = tk.Button(root, image=image_delete, command=lambda: do_vibor('удалить'))
button_delete.place(x=10, y=550)

save_button = tk.Button(root, text='Сохранить', command=save_objects)
save_button.place(x=400, y=620)

load_button = tk.Button(root, text='Загрузить', command=load_objects)
load_button.place(x=500, y=620)

width = 650
height = 600
canvas = tk.Canvas(bg="white", width=width, height=height)
canvas.place(x=10 + SIZE + 10, y=10)

for line in range(0, width, SIZE_GRID):
    canvas.create_line((line, 0), (line, height), fill='#DCDCDC', tags='setka')

for line in range(0, height, SIZE_GRID):
    canvas.create_line((0, line), (width, line), fill='#DCDCDC', tags='setka')

canvas.bind('<Button-1>', on_press)
canvas.bind("<MouseWheel>", scale_all)

root.mainloop()
