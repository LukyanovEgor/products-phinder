import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as fd
from tkinter import ttk
from math import sqrt


def reset(tag_object_flag=True, clear_canvas=False):  # сброс всех переменных
    global tag_object, vibor, moving_status, tag_object
    global x_stena, y_stena, x_put, y_put, x_polka, y_polka, last_x, last_y
    x_stena, y_stena = -1, -1
    x_put, y_put = -1, -1
    x_polka, y_polka = -1, -1
    last_x, last_y = -1, -1
    moving_status = False
    if tag_object_flag:
        tag_object = 0
    if clear_canvas:
        global MASSIV_CONNECT
        canvas.delete('all')
        MASSIV_CONNECT = {}
        tag_object = 0
        draw_setka()

    canvas.delete('metka')
    canvas.delete('polka')
    canvas.delete('line')
    canvas.delete('stena')
    canvas.delete('lineyka')
    canvas.delete('lineyka111')


def do_vibor(stroka):
    reset(tag_object_flag=False)
    global vibor
    vibor = stroka
    if vibor == 'метка':
        canvas.bind('<Motion>', motion)
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
        MASSIV_CONNECT[str(tag_object)] = set()
        tag_object += 1


def draw_setka():
    canvas.delete('setka')
    if setka_show.get() == 1:
        for line1 in range(0, width, int(SIZE_GRID)):
            canvas.tag_lower(canvas.create_line((line1, 0), (line1, height), fill='#DCDCDC', tags='setka'))

        for line1 in range(0, height, int(SIZE_GRID)):
            canvas.tag_lower(canvas.create_line((0, line1), (width, line1), fill='#DCDCDC', tags='setka'))


def draw_polka(x, y, tag, color_rect, color_circle):
    global tag_object, MASSIV_CONNECT
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
        tag = int(tag) + 1

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
            MASSIV_CONNECT[str(tag_object)] = set()
            tag += 1
            tag_object += 1

        canvas.create_oval(x_left + (i * (len_x // (t_x + 1))) + otstup / 2,
                           y_up,
                           x_left + (i * (len_x // (t_x + 1))) - otstup / 2,
                           y_up - 2 * otstup / 2,
                           fill=color_circle,
                           tags=tag)
        if tag != 'polka':
            MASSIV_CONNECT[str(tag_object)] = set()
            tag += 1
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
            MASSIV_CONNECT[str(tag_object)] = set()
            tag += 1
            tag_object += 1
        canvas.create_oval(x_right,
                           y_up + (i * (len_y // (t_y + 1))) - otstup / 2,
                           x_right + 2 * otstup / 2,
                           y_up + (i * (len_y // (t_y + 1))) + otstup / 2,
                           fill=color_circle, tags=tag)
        if tag != 'polka':
            MASSIV_CONNECT[str(tag_object)] = set()
            tag_object += 1
            tag += 1

    canvas.create_oval(x_left, y_up,
                       x_left - 2 * otstup / 2,
                       y_up - 2 * otstup / 2, fill=color_circle,
                       tags=tag)
    if tag != 'polka':
        MASSIV_CONNECT[str(tag_object)] = set()
        tag_object += 1
        tag += 1
    canvas.create_oval(x_left, y_down,
                       x_left - 2 * otstup / 2,
                       y_down + 2 * otstup / 2,
                       fill=color_circle,
                       tags=tag)
    if tag != 'polka':
        MASSIV_CONNECT[str(tag_object)] = set()
        tag_object += 1
        tag += 1
    canvas.create_oval(x_right, y_up,
                       x_right + 2 * otstup / 2,
                       y_up - 2 * otstup / 2, fill=color_circle,
                       tags=tag)
    if tag != 'polka':
        MASSIV_CONNECT[str(tag_object)] = set()
        tag_object += 1
        tag += 1
    canvas.create_oval(x_right, y_down,
                       x_right + 2 * otstup / 2,
                       y_down + 2 * otstup / 2,
                       fill=color_circle, tags=tag)

    if tag != 'polka':
        MASSIV_CONNECT[str(tag_object)] = set()
        tag_object += 1
        tag += 1
    print(MASSIV_CONNECT)


def draw_lineyka(x, y):
    global x_lineyka, y_lineyka
    canvas.delete('lineyka')
    for obj in canvas.find_all():
        if canvas.gettags(obj)[0] == 'lineyka111':
            x1, y1, x2, y2 = canvas.coords(obj)
            x_lineyka = (x1 + x2) // 2
            y_lineyka = (y1 + y2) // 2
    canvas.create_line(x_lineyka, y_lineyka, x, y, tags='lineyka')
    x_1 = max(x_lineyka, x) - min(x_lineyka, x)
    y_1 = max(y_lineyka, y) - min(y_lineyka, y)

    text_item = canvas.create_text((x_lineyka + x) // 2, (y_lineyka + y) // 2 - 6,
                                   text=f'{round(sqrt(x_1 ** 2 + y_1 ** 2) / SIZE_GRID, 2)} м', font='Verdana 12',
                                   fill="black",
                                   tags='lineyka')
    rect_item = canvas.create_rectangle(canvas.bbox(text_item), outline="red", fill="white", tags='lineyka')
    canvas.tag_raise(text_item, rect_item)


def motion(event):
    if vibor == 'стена':
        if x_stena != -1 and y_stena != -1:
            draw_stena(event.x, event.y, 'stena', '#E5E4E2')
    elif vibor == 'полка':
        if x_polka != -1 and y_polka != -1:
            draw_polka(event.x, event.y, 'polka', "#E5E4E2", '#FF8400')
    elif vibor == 'путь':
        global x_put, y_put
        if x_put != -1 and y_put != -1:
            canvas.delete('line')
            for obj in canvas.find_all():
                if canvas.gettags(obj)[0] == start_coordinat_tag:
                    x1, y1, x2, y2 = canvas.coords(obj)
                    x_put = (x1 + x2) // 2
                    y_put = (y1 + y2) // 2
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
    elif vibor == 'линейка':
        global x_lineyka, y_lineyka
        if x_lineyka != -1 and y_lineyka != -1:
            draw_lineyka(event.x, event.y)


def delete_connected_point(tag):
    global MASSIV_CONNECT
    if canvas.type(tag) == 'oval':
        oval_x1, oval_y1, oval_x2, oval_y2 = canvas.coords(tag)
        for obj in canvas.find_all():
            if canvas.type(obj) == 'line' and canvas.gettags(obj)[0] != 'setka':
                x1, y1, x2, y2 = canvas.coords(obj)
                if ((oval_x1 + oval_x2) / 2 == x1 and (oval_y1 + oval_y2) / 2 == y1) or (
                        (oval_x1 + oval_x2) / 2 == x2 and (oval_y1 + oval_y2) / 2 == y2):
                    canvas.delete(obj)
        print(canvas.gettags(tag)[0])
        for value in MASSIV_CONNECT[canvas.gettags(tag)[0]]:
            MASSIV_CONNECT[value].discard(canvas.gettags(tag)[0])
        del MASSIV_CONNECT[canvas.gettags(tag)[0]]
    if canvas.type(tag) == 'line':
        line_x1, line_y1, line_x2, line_y2 = canvas.coords(tag)
        tag_oval = []
        for obj in canvas.find_all():
            if canvas.type(obj) == 'oval':
                x1, y1, x2, y2 = canvas.coords(obj)
                if ((x1 + x2) / 2 == line_x1 and (y1 + y2) / 2 == line_y1) or (
                        (x1 + x2) / 2 == line_x2 and (y1 + y2) / 2 == line_y2):
                    tag_oval.append(canvas.gettags(obj)[0])
        MASSIV_CONNECT[tag_oval[0]].discard(tag_oval[1])
        MASSIV_CONNECT[tag_oval[1]].discard(tag_oval[0])
    print(MASSIV_CONNECT)
    canvas.delete(tag)


def on_press_left(event):
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
        if item_type == "oval":
            global MASSIV_CONNECT, start_coordinat_tag
            if x_put == -1 and y_put == -1:
                start_coordinat_tag = canvas.gettags(item)[0]
                massiv_coordinat = canvas.coords(item)
                x_put = (massiv_coordinat[0] + massiv_coordinat[2]) // 2
                y_put = (massiv_coordinat[1] + massiv_coordinat[3]) // 2
                root.bind('<Motion>', motion)
            else:
                x1, y1, x2, y2 = canvas.coords('line')
                massiv = [canvas.type(i) for i in canvas.find_overlapping(x1, y1, x2, y2)]
                if not ('rectangle' in massiv) and start_coordinat_tag != canvas.gettags(item)[0]:
                    canvas.delete('line')
                    # canvas.itemconfig(event.widget.find_withtag("current"), fill="blue")
                    massiv_coordinat = canvas.coords(item)
                    canvas.tag_lower(
                        canvas.create_line(x_put, y_put, (massiv_coordinat[0] + massiv_coordinat[2]) / 2,
                                           (massiv_coordinat[1] + massiv_coordinat[3]) / 2,
                                           tags=str(tag_object), width=3, fill='blue'))
                    draw_setka()
                    canvas.itemconfig(event.widget.find_withtag("current"))
                    MASSIV_CONNECT[start_coordinat_tag].add(canvas.gettags(item)[0])
                    MASSIV_CONNECT[canvas.gettags(item)[0]].add(start_coordinat_tag)
                    print(MASSIV_CONNECT)

                    tag_object += 1
                    x_put, y_put = -1, -1
                else:
                    print('линия находится слишком близко к стене')
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
            delete_connected_point(event.widget.find_withtag("current"))
    elif vibor == 'перемещение':
        global last_x, last_y, moving_status
        last_x = event.x
        last_y = event.y
        moving_status = not moving_status
        canvas.bind('<Motion>', motion)
    elif vibor == 'линейка':
        global x_lineyka, y_lineyka
        if x_lineyka == -1 and y_lineyka == -1:
            x_lineyka = event.x
            y_lineyka = event.y
            canvas.create_oval(event.x, event.y, event.x + 1, event.y + 1, fill='black', tags='lineyka111')
            root.bind('<Motion>', motion)
        else:
            canvas.delete('lineyka')
            canvas.delete('lineyka111')
            x_lineyka, y_lineyka = -1, -1


def on_press_right(event):
    global information_menu_status
    information_menu_status = not information_menu_status
    item = event.widget.find_withtag("current")
    item_type = canvas.type(item)
    m = tk.Menu(root, tearoff=0)
    if information_menu_status:
        if (item_type != "line" or canvas.gettags(item)[0] != "setka") and len(canvas.gettags(item)) > 0:
            m.add_command(label=f'переместить')
            m.add_command(label=f'удалить', command=lambda: delete_connected_point(item))
            m.add_separator()
            m.add_command(label=f'индекс элемента={canvas.gettags(item)[0]}')
            m.add_command(label=f'координаты элемента={canvas.coords(item)}')
            if item_type == "oval" and canvas.gettags(item)[0] != "metka":
                m.add_command(label=f'связан с={MASSIV_CONNECT[canvas.gettags(item)[0]]}')

        else:
            m.add_command(label="Копировать")
            m.add_command(label="Вставить")
            m.add_separator()
            m.add_command(label="Переименовать")
        m.tk_popup(event.x_root, event.y_root)
    else:
        m.grab_release()


def scale_all(event):
    global SIZE_GRID
    x_scale = 2 if event.delta > 0 else 0.5
    y_scale = 2 if event.delta > 0 else 0.5
    if 128 >= SIZE_GRID * x_scale >= 1 and scale_status:
        canvas.move('all', -(event.x // SIZE_GRID) * SIZE_GRID, -(event.y // SIZE_GRID) * SIZE_GRID)
        SIZE_GRID *= x_scale
        global x_stena, y_stena
        if x_stena != -1 and y_stena != -1:
            x_stena = x_stena * x_scale
            y_stena = y_stena * y_scale
        global x_polka, y_polka
        if x_polka != -1 and y_polka != -1:
            x_polka = x_polka * x_scale
            y_polka = y_polka * y_scale
        canvas.scale('all', 0, 0, x_scale, y_scale)
        canvas.move('all', (event.x // SIZE_GRID) * SIZE_GRID, (event.y // SIZE_GRID) * SIZE_GRID)
        draw_setka()
        if x_lineyka != -1 and y_lineyka != -1:
            draw_lineyka(event.x, event.y)


def save_objects():
    file_path = fd.asksaveasfilename(defaultextension='.txt')
    reset(tag_object_flag=False)
    with open(file_path, 'w') as file:
        file.write(str(int(SIZE_GRID)) + '\n')
        canvas.delete('setka')
        mas = canvas.find_all()
        file.write(str(len(mas)) + '\n')
        for obj in mas:
            if canvas.gettags(obj)[0] != 'setka':
                file.write(
                    f"{canvas.type(obj)} {canvas.gettags(obj)[0]} {canvas.itemcget(obj, 'fill')} {canvas.coords(obj)}\n"
                )
        draw_setka()
        file.write(str(len(MASSIV_CONNECT)) + '\n')
        for i in MASSIV_CONNECT:
            file.write(f'{i} {" ".join(MASSIV_CONNECT[i])}\n')


def load_objects(path=''):
    global tag_object, SIZE_GRID, MASSIV_CONNECT
    if path == '':
        file_path = fd.askopenfilename(filetypes=[('Text Files', '*.txt')])
    else:
        file_path = path
    with open(file_path, 'r') as file:
        SIZE_GRID = int(file.readline().replace('\n', ''))
        canvas.delete('all')
        draw_setka()
        reset()
        n = int(file.readline())
        for _ in range(n):
            line = file.readline().split()
            obj_type = line[0]
            obj_tag = line[1]
            obj_color = line[2]
            coords = ' '.join(map(str, line[3:]))
            tag_object = max(int(obj_tag), tag_object)
            if obj_type == 'line':
                eval(f'canvas.create_{obj_type}({eval(coords)},fill="{obj_color}",tags="{obj_tag}",width=3)')
            else:
                eval(f'canvas.create_{obj_type}({eval(coords)},fill="{obj_color}",tags="{obj_tag}")')
        tag_object = tag_object + 1
        n = int(file.readline())
        for _ in range(n):
            line = file.readline().split()
            ind = line[0]
            value = line[1:]
            MASSIV_CONNECT[ind] = set(value)


def connect_dots():
    def loading_connect_dots(progress_bar):
        for widget in root.winfo_children():
            if widget.winfo_class() == 'Button':
                widget["state"] = "disabled"
        global tag_object, scale_status
        scale_status = False

        reset(tag_object_flag=False)
        mas = []
        for obj in canvas.find_all():
            if canvas.type(obj) == 'oval' and canvas.gettags(obj)[0] != 'metka':
                mas_coord = canvas.coords(obj)
                mas.append(
                    [canvas.gettags(obj)[0], (mas_coord[0] + mas_coord[2]) // 2, (mas_coord[1] + mas_coord[3]) // 2])
        canvas.delete('setka')
        do_vibor('стрелка')
        for x in range(len(mas) - 1):
            progress_bar['value'] = x / len(mas) * 100
            root.update()
            for y in range(x + 1, len(mas)):
                canvas.tag_lower(
                    canvas.create_line(mas[x][1], mas[x][2], mas[y][1], mas[y][2], tags='line', fill='blue'))
                x1, y1, x2, y2 = canvas.coords('line')
                massiv = [canvas.type(i) for i in canvas.find_overlapping(x1, y1, x2, y2)]
                if not ('rectangle' in massiv):
                    global MASSIV_CONNECT
                    canvas.delete('line')
                    canvas.tag_lower(
                        canvas.create_line(mas[x][1], mas[x][2], mas[y][1], mas[y][2],
                                           tags=str(tag_object), width=3, fill='blue'))
                    MASSIV_CONNECT[mas[x][0]].add(mas[y][0])
                    MASSIV_CONNECT[mas[y][0]].add(mas[x][0])
                    tag_object += 1
        progress_bar['value'] = 100
        draw_setka()
        for widget in root.winfo_children():
            if widget.winfo_class() == 'Button':
                widget["state"] = "normal"
        scale_status = True

    progress = ttk.Progressbar(root, length=300, mode='determinate')
    progress.place(x=width - 200, y=height + 20)
    progress['maximum'] = 100
    loading_connect_dots(progress)
    progress.destroy()
    canvas.delete('line')


def bd_tovara():
    reset(tag_object_flag=False)

    def delete_row():
        selected_item = tree.selection()
        for i in selected_item:
            tree.delete(i)

    def add_row():
        id_product = entry_id.get()
        shelf_number = entry_shelf.get()
        shelf = entry_shelf_type.get()
        date = entry_date.get()

        tree.insert("", tk.END, values=(id_product, shelf_number, shelf, date))

    def browse_file(path=''):
        if path == '':
            file_path = tk.filedialog.askopenfilename()
        else:
            file_path = path
        with open(file_path) as file:
            CONFIGURATION['bd_tovar'] = file_path
            tree.delete(*tree.get_children())
            for line in file:
                data = line.strip().split()
                tree.insert("", tk.END, values=data)

    def save_file():
        file = open(CONFIGURATION['bd_tovar'], 'w')
        for item in tree.get_children():
            file.write(' '.join(list(map(str, tree.item(item)["values"]))) + '\n')

    window_bd_tovar = tk.Toplevel(root)
    window_bd_tovar.title("БД товара")
    window_bd_tovar.grab_set()

    tree = ttk.Treeview(window_bd_tovar, columns=("ID Product", "Shelf Number", "Shelf", "Date"), show="headings")
    tree.heading("ID Product", text="ID")
    tree.heading("Shelf Number", text="Номер метки")
    tree.heading("Shelf", text="Полка")
    tree.heading("Date", text="Дата")
    tree.pack()

    btn_frame = tk.Frame(window_bd_tovar)
    btn_frame.pack()

    button_add = tk.Button(btn_frame, text="Добавить строчку", command=add_row)
    button_add.pack(side=tk.LEFT)

    button_del = tk.Button(btn_frame, text="Удалить строчку", command=delete_row)
    button_del.pack(side=tk.LEFT)

    button_browse = tk.Button(btn_frame, text="Выбрать файл", command=browse_file)
    button_browse.pack(side=tk.LEFT)

    button_browse = tk.Button(btn_frame, text="Сохранить файл", command=save_file)
    button_browse.pack(side=tk.LEFT)

    entry_frame = tk.Frame(window_bd_tovar)
    entry_frame.pack()

    entry_id = tk.Entry(entry_frame, width=10)
    entry_id.pack(side=tk.LEFT)
    label_id = tk.Label(entry_frame, text="ID")
    label_id.pack(side=tk.LEFT)

    entry_shelf = tk.Entry(entry_frame, width=10)
    entry_shelf.pack(side=tk.LEFT)
    label_shelf = tk.Label(entry_frame, text="Номер метки")
    label_shelf.pack(side=tk.LEFT)

    entry_shelf_type = tk.Entry(entry_frame, width=10)
    entry_shelf_type.pack(side=tk.LEFT)
    label_shelf_type = tk.Label(entry_frame, text="Полка")
    label_shelf_type.pack(side=tk.LEFT)

    entry_date = tk.Entry(entry_frame, width=10)
    entry_date.pack(side=tk.LEFT)
    label_date = tk.Label(entry_frame, text="Дата")
    label_date.pack(side=tk.LEFT)

    browse_file(CONFIGURATION['bd_tovar'])

    window_bd_tovar.mainloop()
    window_bd_tovar.wait_window()


def find_tovar():
    def remove_selected_items():
        selected_indices = listbox.curselection()
        for index in selected_indices:
            listbox.delete(index)

    def add_index():
        index = index_entry.get()
        if index:
            listbox.insert(tk.END, index)
            index_entry.delete(0, tk.END)

    def draw_path():
        print('нужно сделать отрисовку пути на карте')

    window_find_tovar = tk.Toplevel(root)
    window_find_tovar.title("Поиск товара")
    window_find_tovar.geometry("500x300")
    window_find_tovar.grab_set()

    index_label = tk.Label(window_find_tovar, text="Введите код товара")
    index_label.place(x=10, y=10)

    index_entry = tk.Entry(window_find_tovar)
    index_entry.place(x=10, y=50)

    add_button = tk.Button(window_find_tovar, text="Добавить", command=add_index)
    add_button.place(x=10, y=100)
    remove_button = tk.Button(window_find_tovar, text="Удалить", command=remove_selected_items)
    remove_button.place(x=10, y=130)

    find_button = tk.Button(window_find_tovar, text="Построить маршрут", command=draw_path)
    find_button.place(x=10, y=250)

    listbox = tk.Listbox(window_find_tovar, width=40, height=15)
    listbox.place(x=200, y=10)

    window_find_tovar.mainloop()
    window_find_tovar.wait_window()


root = tk.Tk()
root.title('навигатор')
root.geometry("800x650")

vibor = 'стрелка'  # выбор режима
x_stena, y_stena = -1, -1
x_put, y_put = -1, -1
x_polka, y_polka = -1, -1
x_lineyka, y_lineyka = -1, -1
last_x, last_y = -1, -1
moving_status = False
scale_status = True
information_menu_status = False
tag_object = 0
start_coordinat_tag = ''
setka_show = tk.BooleanVar()
setka_show.set(True)

_SIZE_SCALE = 8
SIZE = 80
RADIUS = _SIZE_SCALE
SIZE_GRID = _SIZE_SCALE

MASSIV_CONNECT = {}
CONFIGURATION = {
    'file_open': "C:/Users/Пасечниковы/Desktop/new_format.txt",
    'bd_tovar': "C:/Users/Пасечниковы/Desktop/сборщик/memory — копия.txt"
}

image_strelka = ImageTk.PhotoImage(image=Image.open("image_navigator/стрелка.png").resize((SIZE, SIZE), Image.LANCZOS))
button_strelka = tk.Button(root, image=image_strelka, command=lambda: do_vibor('стрелка'))
button_strelka.place(x=10, y=10)

image_metka = ImageTk.PhotoImage(image=Image.open("image_navigator/метка.png").resize((SIZE, SIZE), Image.LANCZOS))
button_metka = tk.Button(root, image=image_metka, command=lambda: do_vibor('метка'))
button_metka.place(x=10, y=100)

image_put = ImageTk.PhotoImage(image=Image.open("image_navigator/путь.png").resize((SIZE, SIZE), Image.LANCZOS))
button_put = tk.Button(root, image=image_put, command=lambda: do_vibor('путь'))
button_put.place(x=10, y=190)

image_stena = ImageTk.PhotoImage(image=Image.open("image_navigator/стена.jpg").resize((SIZE, SIZE), Image.LANCZOS))
button_stena = tk.Button(root, image=image_stena, command=lambda: do_vibor('стена'))
button_stena.place(x=10, y=280)

image_polka = ImageTk.PhotoImage(image=Image.open("image_navigator/полка.jpg").resize((SIZE, SIZE), Image.LANCZOS))
button_polka = tk.Button(root, image=image_polka, command=lambda: do_vibor('полка'))
button_polka.place(x=10, y=370)

image_move = ImageTk.PhotoImage(image=Image.open("image_navigator/перемещение.png").resize((SIZE, SIZE), Image.LANCZOS))
button_move = tk.Button(root, image=image_move, command=lambda: do_vibor('перемещение'))
button_move.place(x=10, y=460)

image_delete = ImageTk.PhotoImage(image=Image.open("image_navigator/удалить.jpeg").resize((SIZE, SIZE), Image.LANCZOS))
button_delete = tk.Button(root, image=image_delete, command=lambda: do_vibor('удалить'))
button_delete.place(x=10, y=550)

menu = tk.Menu()

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Сохранить как", command=save_objects)
file_menu.add_command(label="Загрузить", command=load_objects)
file_menu.add_separator()
file_menu.add_command(label="Очистить экран", command=lambda: reset(clear_canvas=True))
file_menu.add_command(label="Выйти", command=lambda: exit())
menu.add_cascade(label="Файл", menu=file_menu)

settings_menu = tk.Menu(menu, tearoff=0)
settings_menu.add_command(label="Подключение БД товара", command=bd_tovara)
settings_menu.add_command(label="Подключение телеграм бота")
settings_menu.add_command(label="Соединение всех меток", command=connect_dots)
settings_menu.add_command(label="Поиск товара", command=find_tovar)
menu.add_cascade(label="Настройки", menu=settings_menu)

vid_menu = tk.Menu(menu, tearoff=0)
vid_menu.add_checkbutton(label="Отображение сетки", onvalue=1, offvalue=0, variable=setka_show, command=draw_setka)
vid_menu.add_command(label="Отображение текста")
menu.add_cascade(label="Вид", menu=vid_menu)

tool_menu = tk.Menu(menu, tearoff=0)
tool_menu.add_command(label="Стена", command=lambda: do_vibor('стена'))
tool_menu.add_command(label="Полка", command=lambda: do_vibor('полка'))
tool_menu.add_command(label="Метка", command=lambda: do_vibor('метка'))
tool_menu.add_command(label="Путь", command=lambda: do_vibor('путь'))
tool_menu.add_command(label="Текст")
tool_menu.add_command(label="Линейка", command=lambda: do_vibor('линейка'))
tool_menu.add_separator()
tool_menu.add_command(label="Перемещение", command=lambda: do_vibor('перемещение'))
tool_menu.add_command(label="Удаление", command=lambda: do_vibor('удалить'))
menu.add_cascade(label="Инструменты", menu=tool_menu)

information_menu = tk.Menu(menu, tearoff=0)
information_menu.add_command(label="Как пользоваться")
menu.add_cascade(label="О приложении", menu=information_menu)

root.config(menu=menu)

width = 650
height = 600
canvas = tk.Canvas(bg="white", width=width, height=height)
canvas.place(x=10 + SIZE + 10, y=10)
load_objects(CONFIGURATION['file_open'])
draw_setka()

canvas.bind('<Button-1>', on_press_left)
canvas.bind("<MouseWheel>", scale_all)
canvas.bind('<Button-3>', on_press_right)

root.mainloop()
