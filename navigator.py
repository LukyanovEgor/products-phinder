import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as fd
from tkinter import ttk


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


def draw_stena(x, y, tag, color):
    global tag_object
    canvas.delete('stena')
    canvas.create_rectangle(x_stena, y_stena, (x // SIZE_GRID) * SIZE_GRID,
                            (y // SIZE_GRID) * SIZE_GRID, fill=color, outline="#000000", tags=tag)
    if tag != 'stena':
        tag_object += 1


def draw_metka(x, y, tag, color):
    global tag_object
    canvas.delete('metka')
    q = max(SIZE_GRID // 2, 1)
    canvas.create_oval((x // q) * q - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                       (y // q) * q - RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                       (x // q) * q + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                       (y // q) * q + RADIUS * SIZE_GRID // _SIZE_SCALE / 2,
                       fill=color, tags=tag)
    if tag != 'metka':
        tag_object += 1


def draw_setka():
    canvas.delete('setka')
    for line1 in range(0, width, int(SIZE_GRID)):
        canvas.tag_lower(canvas.create_line((line1, 0), (line1, height), fill='#DCDCDC', tags='setka'))

    for line1 in range(0, height, int(SIZE_GRID)):
        canvas.tag_lower(canvas.create_line((0, line1), (width, line1), fill='#DCDCDC', tags='setka'))


def draw_polka(x, y, tag, color_rect, color_circle):
    global tag_object
    canvas.delete('polka')
    x_left = min(x_polka, (x // SIZE_GRID) * SIZE_GRID)
    x_right = max(x_polka, (x // SIZE_GRID) * SIZE_GRID)
    y_up = min(y_polka, (y // SIZE_GRID) * SIZE_GRID)
    y_down = max(y_polka, (y // SIZE_GRID) * SIZE_GRID)
    otstup = RADIUS * SIZE_GRID // _SIZE_SCALE
    canvas.create_rectangle(x_left, y_up, x_right,
                            y_down, fill=color_rect, outline="#000000",
                            tags=tag)
    if tag != 'polka':
        tag_object += 1

    len_x = abs(x_right - x_left)
    t_x = max(int(len_x // (otstup * 10)), 1)
    for i in range(1, t_x + 1):
        canvas.create_oval(x_left + (i * (len_x // (t_x + 1))) + otstup / 2,
                           y_down,
                           x_left + (i * (len_x // (t_x + 1))) - otstup / 2,
                           y_down + 2 * otstup / 2,
                           fill=color_circle,
                           tags=tag)
        if tag != 'polka':
            tag_object += 1
        canvas.create_oval(x_left + (i * (len_x // (t_x + 1))) + otstup / 2,
                           y_up,
                           x_left + (i * (len_x // (t_x + 1))) - otstup / 2,
                           y_up - 2 * otstup / 2,
                           fill=color_circle,
                           tags=tag)
        if tag != 'polka':
            tag_object += 1

    len_y = abs(y_down - y_up)
    t_y = max(int(len_y // (otstup * 10)), 1)
    for i in range(1, t_y + 1):
        canvas.create_oval(x_left,
                           y_up + (i * (len_y // (t_y + 1))) - otstup / 2,
                           x_left - 2 * otstup / 2,
                           y_up + (i * (len_y // (t_y + 1))) + otstup / 2,
                           fill=color_circle, tags=tag)
        if tag != 'polka':
            tag_object += 1
        canvas.create_oval(x_right,
                           y_up + (i * (len_y // (t_y + 1))) - otstup / 2,
                           x_right + 2 * otstup / 2,
                           y_up + (i * (len_y // (t_y + 1))) + otstup / 2,
                           fill=color_circle, tags=tag)
        if tag != 'polka':
            tag_object += 1

    canvas.create_oval(x_left, y_up,
                       x_left - 2 * otstup / 2,
                       y_up - 2 * otstup / 2, fill=color_circle,
                       tags=tag)
    if tag != 'polka':
        tag_object += 1
    canvas.create_oval(x_left, y_down,
                       x_left - 2 * otstup / 2,
                       y_down + 2 * otstup / 2,
                       fill=color_circle,
                       tags=tag)
    if tag != 'polka':
        tag_object += 1
    canvas.create_oval(x_right, y_up,
                       x_right + 2 * otstup / 2,
                       y_up - 2 * otstup / 2, fill=color_circle,
                       tags=tag)
    if tag != 'polka':
        tag_object += 1
    canvas.create_oval(x_right, y_down,
                       x_right + 2 * otstup / 2,
                       y_down + 2 * otstup / 2,
                       fill=color_circle, tags=tag)

    if tag != 'polka':
        tag_object += 1


def motion(event):
    if vibor == 'стена':
        if x_stena != -1 and y_stena != -1:
            draw_stena(event.x, event.y, 'stena', '#E5E4E2')
    elif vibor == 'полка':
        if x_polka != -1 and y_polka != -1:
            draw_polka(event.x, event.y, 'polka', "#E5E4E2", '#FF8400')
    elif vibor == 'путь':
        if x_put != -1 and y_put != -1:
            canvas.delete('line')
            if event.x < x_put and event.y < y_put:
                canvas.create_line(x_put, y_put, event.x + 2, event.y - 2, tags='line')
            else:
                canvas.create_line(x_put, y_put, event.x - 2, event.y - 2, tags='line')
    elif vibor == 'метка':
        draw_metka(event.x, event.y, 'metka', '#FF8400')
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
            draw_stena(event.x, event.y, str(tag_object), "#D5D5D5")
            x_stena, y_stena = -1, -1
    elif vibor == 'метка':
        draw_metka(event.x, event.y, str(tag_object), '#FF2400')
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
                    x1, y1, x2, y2 = canvas.coords('line')
                    massiv = [canvas.type(i) for i in canvas.find_overlapping(x1, y1, x2, y2)]
                    if not ('rectangle' in massiv):
                        canvas.delete('line')
                        # canvas.itemconfig(event.widget.find_withtag("current"), fill="blue")
                        massiv_coordinat = canvas.coords(item)
                        canvas.tag_lower(
                            canvas.create_line(x_put, y_put, (massiv_coordinat[0] + massiv_coordinat[2]) // 2,
                                               (massiv_coordinat[1] + massiv_coordinat[3]) // 2,
                                               tags=str(tag_object), width=3, fill='blue'))
                        draw_setka()
                        canvas.itemconfig(event.widget.find_withtag("current"))
                        tag_object += 1
                        x_put, y_put = -1, -1
                    else:
                        print('линия находится слишком близко к стене')
        else:
            print('слишком маленький масштаб')
    elif vibor == 'полка':
        global x_polka, y_polka
        if x_polka == -1 and y_polka == -1:
            x_polka = (event.x // SIZE_GRID) * SIZE_GRID
            y_polka = (event.y // SIZE_GRID) * SIZE_GRID
            root.bind('<Motion>', motion)
        else:
            draw_polka(event.x, event.y, str(tag_object), "#D5D5D5", '#FF2400')
            x_polka, y_polka = -1, -1
    elif vibor == 'удалить':
        # res=event.widget.find_closest(event.x, event.y) # ctrl z
        if canvas.gettags(canvas.find_closest(event.x, event.y)[0])[0] != 'setka':
            canvas.delete(event.widget.find_withtag("current"))
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
        canvas.move('all', -(event.x // SIZE_GRID) * SIZE_GRID, -(event.y // SIZE_GRID) * SIZE_GRID)
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
        canvas.scale('all', 0, 0, x_scale, y_scale)
        canvas.move('all', (event.x // SIZE_GRID) * SIZE_GRID, (event.y // SIZE_GRID) * SIZE_GRID)
        draw_setka()


def reset(tag_object_flag=True):  # сброс всех переменных
    global tag_object, vibor, moving_status, tag_object
    global x_stena, y_stena, x_put, y_put, x_polka, y_polka, last_x, last_y
    vibor = 'стрелка'  # выбор режима
    x_stena, y_stena = -1, -1
    x_put, y_put = -1, -1
    x_polka, y_polka = -1, -1
    last_x, last_y = -1, -1
    moving_status = False
    if tag_object_flag:
        tag_object = 0


def save_objects():
    file_path = fd.asksaveasfilename(defaultextension='.txt')
    with open(file_path, 'w') as file:
        file.write(str(int(SIZE_GRID)) + '\n')
        for obj in canvas.find_all():
            if canvas.gettags(obj)[0] != 'setka':
                file.write(
                    f"{canvas.type(obj)} {canvas.gettags(obj)[0]} {canvas.itemcget(obj, 'fill')} {canvas.coords(obj)}\n"
                )


def load_objects():
    global tag_object, SIZE_GRID
    file_path = fd.askopenfilename(filetypes=[('Text Files', '*.txt')])
    with open(file_path, 'r') as file:
        SIZE_GRID = int(file.readline().replace('\n', ''))
        canvas.delete('all')
        draw_setka()
        reset()
        for line2 in file:
            obj_type = line2.split()[0]
            obj_tag = line2.split()[1]
            obj_color = line2.split()[2]
            coords = ' '.join(map(str, line2.split()[3:]))
            tag_object = max(int(obj_tag), tag_object)
            if obj_type == 'line':
                eval(f'canvas.create_{obj_type}({eval(coords)},fill="{obj_color}",tags="{obj_tag}",width=3)')
            else:
                eval(f'canvas.create_{obj_type}({eval(coords)},fill="{obj_color}",tags="{obj_tag}")')
        tag_object = tag_object + 1


def loading_connect_dots(progress_bar):
    for widget in root.winfo_children():
        if widget.winfo_class() == 'Button':
            widget["state"] = "disabled"
    global tag_object
    reset(tag_object_flag=False)
    mas = []
    for obj in canvas.find_all():
        if canvas.type(obj) == 'oval' and canvas.gettags(obj)[0] != 'metka':
            mas_coord = canvas.coords(obj)
            mas.append([canvas.gettags(obj)[0], (mas_coord[0] + mas_coord[2]) // 2, (mas_coord[1] + mas_coord[3]) // 2])
    canvas.delete('setka')

    for x in range(len(mas) - 1):
        progress_bar['value'] = x / len(mas) * 100
        root.update()
        for y in range(len(mas)):
            canvas.tag_lower(canvas.create_line(mas[x][1], mas[x][2], mas[y][1], mas[y][2], tags='line', fill='blue'))
            x1, y1, x2, y2 = canvas.coords('line')
            massiv = [canvas.type(i) for i in canvas.find_overlapping(x1, y1, x2, y2)]
            if not ('rectangle' in massiv):
                canvas.delete('line')
                canvas.tag_lower(
                    canvas.create_line(mas[x][1], mas[x][2], mas[y][1], mas[y][2],
                                       tags=str(tag_object), width=3, fill='blue'))
                tag_object += 1
    progress_bar['value'] = 100
    draw_setka()
    for widget in root.winfo_children():
        if widget.winfo_class() == 'Button':
            widget["state"] = "normal"


def connect_dots():
    progress = ttk.Progressbar(root, length=300, mode='determinate')
    progress.place(x=width - 200, y=height + 20)
    progress['maximum'] = 100
    loading_connect_dots(progress)
    progress.destroy()


vibor = 'стрелка'  # выбор режима
x_stena, y_stena = -1, -1
x_put, y_put = -1, -1
x_polka, y_polka = -1, -1
last_x, last_y = -1, -1
moving_status = False
tag_object = 0

root = tk.Tk()
root.title('навигатор')
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

menu = tk.Menu()

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Сохранить как", command=save_objects)
file_menu.add_command(label="Загрузить", command=load_objects)
file_menu.add_separator()
file_menu.add_command(label="Выйти", command=lambda: exit())
menu.add_cascade(label="Файл", menu=file_menu)

settings_menu = tk.Menu(menu, tearoff=0)
settings_menu.add_command(label="Подключение БД")
settings_menu.add_command(label="Подключение телеграм бота")
settings_menu.add_command(label="Соединение всех меток", command=connect_dots)
settings_menu.add_command(label="Поиск")
menu.add_cascade(label="Настройки", menu=settings_menu)

vid_menu = tk.Menu(menu, tearoff=0)
vid_menu.add_command(label="Размер")
vid_menu.add_command(label="Отображение сетки")
vid_menu.add_command(label="Отображение текста")
menu.add_cascade(label="Вид", menu=vid_menu)

tool_menu = tk.Menu(menu, tearoff=0)
tool_menu.add_command(label="Стена")
tool_menu.add_command(label="Полка")
tool_menu.add_command(label="Метка")
tool_menu.add_command(label="Путь")
tool_menu.add_command(label="Текст")
tool_menu.add_command(label="Линейка")
tool_menu.add_separator()
tool_menu.add_command(label="Перемещение")
tool_menu.add_command(label="Масштабирование")
menu.add_cascade(label="Инструменты", menu=tool_menu)

information_menu = tk.Menu(menu, tearoff=0)
information_menu.add_command(label="О нас")
information_menu.add_command(label="Как пользоваться")
menu.add_cascade(label="О приложении", menu=information_menu)

root.config(menu=menu)

width = 650
height = 600
canvas = tk.Canvas(bg="white", width=width, height=height)
canvas.place(x=10 + SIZE + 10, y=10)

draw_setka()

canvas.bind('<Button-1>', on_press)
canvas.bind("<MouseWheel>", scale_all)

root.mainloop()
