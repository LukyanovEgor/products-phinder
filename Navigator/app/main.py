import tkinter as tk
import tkinter.filedialog as fd
from tkinter import ttk
from PIL import Image, ImageTk

from Navigator.app.draw import draw_text, draw_setka, draw_stena, draw_polka, draw_metka, draw_lineyka
from Navigator.app.settings_text import do_vibor_text, hide_text
from Navigator.app.delete_connected_point import delete_connected_point
from Navigator.app.find_tovar import find_tovar
from Navigator.app.telegram_bot import telegram_bot
from Navigator.app.bd_tovar import bd_tovara


def reset(canvas, tag_object_flag=True, clear_canvas=False):  # сброс всех переменных
    global tag_object, vibor, moving_status, tag_object
    global x_stena, y_stena, x_put, y_put, x_polka, y_polka, last_x, last_y, x_lineyka, y_lineyka, x_text, y_text
    x_stena, y_stena = -1, -1
    x_put, y_put = -1, -1
    x_polka, y_polka = -1, -1
    last_x, last_y = -1, -1
    x_lineyka, y_lineyka = -1, -1
    x_text, y_text = -1, -1
    moving_status = False
    if tag_object_flag:
        tag_object = 0
    if clear_canvas:
        global MASSIV_CONNECT
        canvas.delete('all')
        MASSIV_CONNECT = {}
        tag_object = 0
        draw_setka(canvas, setka_show, width, height, SIZE_GRID)

    canvas.delete('metka')
    canvas.delete('polka')
    canvas.delete('line')
    canvas.delete('stena')
    canvas.delete('lineyka')
    canvas.delete('lineyka111')
    canvas.delete('text')


def do_vibor(stroka):
    reset(canvas1, tag_object_flag=False)
    global vibor
    vibor = stroka
    if vibor == 'метка':
        canvas1.bind('<Motion>', lambda event: motion(event, canvas1))
    print(vibor)


def motion(event, canvas):
    global tag_object, MASSIV_CONNECT
    if vibor == 'стена':
        if x_stena != -1 and y_stena != -1:
            tag_object = draw_stena(canvas, event.x, event.y, 'stena', '#E5E4E2', x_stena, y_stena, SIZE_GRID,
                                    tag_object)
    elif vibor == 'полка':
        if x_polka != -1 and y_polka != -1:
            tag_object, MASSIV_CONNECT = draw_polka(canvas, event.x, event.y, 'polka', "#E5E4E2", '#FF8400', x_polka,
                                                    y_polka, SIZE_GRID, _SIZE_SCALE, RADIUS, tag_object, MASSIV_CONNECT)
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
        tag_object, MASSIV_CONNECT = draw_metka(canvas, event.x, event.y, 'metka', '#FF8400', SIZE_GRID, RADIUS,
                                                _SIZE_SCALE, tag_object, MASSIV_CONNECT)
    elif vibor == 'перемещение':
        if moving_status:
            global last_x, last_y
            for obj in canvas.find_all():
                if canvas.gettags(obj)[0] != 'setka':
                    canvas.move(obj, (event.x - last_x) * SIZE_GRID // 2, (event.y - last_y) * SIZE_GRID // 2)
            last_x = event.x
            last_y = event.y
            canvas.scale('all', 0, 0, 1, 1)  # чтоб буквы не оставляли след
        else:
            return
    elif vibor == 'линейка':
        global x_lineyka, y_lineyka
        if x_lineyka != -1 and y_lineyka != -1:
            x_lineyka, y_lineyka = draw_lineyka(canvas, event.x, event.y, x_lineyka, y_lineyka, SIZE_GRID)
    elif vibor == 'текст':
        global x_text, y_text
        if x_text != -1 and y_text != -1:
            global font_text
            font_text, tag_object = draw_text(canvas, event.x, event.y, 'text', text_show, font_settings, font_text,
                                              tag_object)


def on_press_left(event, canvas):
    global tag_object, MASSIV_CONNECT
    if vibor == 'стена':
        global x_stena, y_stena
        if x_stena == -1 and y_stena == -1:
            x_stena = (event.x // SIZE_GRID) * SIZE_GRID
            y_stena = (event.y // SIZE_GRID) * SIZE_GRID
            canvas1.bind('<Motion>', lambda events: motion(events, canvas1))
        else:
            tag_object = draw_stena(canvas, event.x, event.y, str(tag_object), "#D5D5D5", x_stena, y_stena, SIZE_GRID,
                                    tag_object)
            x_stena, y_stena = -1, -1
    elif vibor == 'метка':
        tag_object, MASSIV_CONNECT = draw_metka(canvas, event.x, event.y, str(tag_object), '#FF2400', SIZE_GRID, RADIUS,
                                                _SIZE_SCALE, tag_object, MASSIV_CONNECT)
    elif vibor == 'путь':
        global x_put, y_put
        item = event.widget.find_withtag("current")
        item_type = canvas.type(item)
        if item_type == "oval":
            global start_coordinat_tag
            if x_put == -1 and y_put == -1:
                start_coordinat_tag = canvas.gettags(item)[0]
                massiv_coordinat = canvas.coords(item)
                x_put = (massiv_coordinat[0] + massiv_coordinat[2]) // 2
                y_put = (massiv_coordinat[1] + massiv_coordinat[3]) // 2
                canvas1.bind('<Motion>', lambda events: motion(events, canvas1))
            else:
                x1, y1, x2, y2 = canvas.coords('line')
                massiv = [canvas.type(i) for i in canvas.find_overlapping(x1, y1, x2, y2)]
                if not ('rectangle' in massiv) and start_coordinat_tag != canvas.gettags(item)[0]:
                    canvas.delete('line')
                    massiv_coordinat = canvas.coords(item)
                    canvas.tag_lower(
                        canvas.create_line(x_put, y_put, (massiv_coordinat[0] + massiv_coordinat[2]) / 2,
                                           (massiv_coordinat[1] + massiv_coordinat[3]) / 2,
                                           tags=str(tag_object), width=3, fill='blue'))
                    draw_setka(canvas, setka_show, width, height, SIZE_GRID)
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
            canvas1.bind('<Motion>', lambda events: motion(events, canvas1))
        else:
            tag_object, MASSIV_CONNECT = draw_polka(canvas, event.x, event.y, str(tag_object), "#D5D5D5", '#FF2400',
                                                    x_polka, y_polka, SIZE_GRID, _SIZE_SCALE, RADIUS, tag_object,
                                                    MASSIV_CONNECT)
            x_polka, y_polka = -1, -1
    elif vibor == 'удалить':
        # res=event.widget.find_closest(event.x, event.y) # ctrl z
        if canvas.gettags(canvas.find_closest(event.x, event.y)[0])[0] != 'setka':
            MASSIV_CONNECT = delete_connected_point(canvas, event.widget.find_withtag("current"), MASSIV_CONNECT)
    elif vibor == 'перемещение':
        global last_x, last_y, moving_status
        last_x = event.x
        last_y = event.y
        moving_status = not moving_status
        canvas.bind('<Motion>', lambda events: motion(events, canvas1))
    elif vibor == 'линейка':
        global x_lineyka, y_lineyka
        if x_lineyka == -1 and y_lineyka == -1:
            x_lineyka = event.x
            y_lineyka = event.y
            canvas.create_oval(event.x, event.y, event.x + 1, event.y + 1, fill='black', tags='lineyka111')
            canvas1.bind('<Motion>', lambda events: motion(events, canvas1))
        else:
            canvas.delete('lineyka')
            canvas.delete('lineyka111')
            x_lineyka, y_lineyka = -1, -1
    elif vibor == 'текст':
        global x_text, y_text, font_text, font_settings
        if x_text == -1 and y_text == -1:
            x_text = 0
            y_text = 0
            canvas1.bind('<Motion>', lambda events: motion(events, canvas1))
            global font_settings
            font_settings, font_text = do_vibor_text(root, font_settings, font_text)
        else:
            font_text, tag_object = draw_text(canvas, event.x, event.y, str(tag_object), text_show, font_settings,
                                              font_text, tag_object)
            x_text, y_text = -1, -1


def on_press_right(event, canvas):
    def update_massiv_connect(can, ite, mas1):
        global MASSIV_CONNECT
        MASSIV_CONNECT = delete_connected_point(can, ite, mas1)

    global information_menu_status, MASSIV_CONNECT
    information_menu_status = not information_menu_status
    item = event.widget.find_withtag("current")
    item_type = canvas.type(item)
    m = tk.Menu(root, tearoff=0)
    if information_menu_status:
        if (item_type != "line" or canvas.gettags(item)[0] != "setka") and len(canvas.gettags(item)) > 0:
            m.add_command(label=f'изменить')
            m.add_command(label=f'переместить')
            m.add_command(label=f'удалить', command=lambda: update_massiv_connect(canvas, item, MASSIV_CONNECT))
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


def scale_all(event, canvas, nap=None):  # сделать масштабирование текста меньше 32
    global SIZE_GRID
    x_scale = 2 if event.delta > 0 or nap else 0.5
    y_scale = 2 if event.delta > 0 or nap else 0.5
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
        draw_setka(canvas, setka_show, width, height, SIZE_GRID)
        for obj in canvas.find_all():
            if canvas.type(obj) == 'text':
                massiv = canvas.itemconfigure(obj, 'font')[-1].split()
                for i in range(len(massiv) - 1, -1, -1):
                    try:
                        font_size = int(massiv[i]) * x_scale
                        print(massiv)
                        canvas.itemconfigure(obj, font=canvas.itemconfigure(obj, 'font')[-1].replace(
                            massiv[i], str(round(font_size))))
                        break
                    except Exception as ex:
                        print(ex)
                        pass
        global x_lineyka, y_lineyka
        if x_lineyka != -1 and y_lineyka != -1:
            x_lineyka, y_lineyka = draw_lineyka(canvas, event.x, event.y, x_lineyka, y_lineyka, SIZE_GRID)


def save_objects():
    file_path = fd.asksaveasfilename(defaultextension='.txt')
    reset(canvas1, tag_object_flag=False)
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(int(SIZE_GRID)) + '\n')
            canvas1.delete('setka')
            mas = canvas1.find_all()
            file.write(str(len(mas)) + '\n')
            for obj in mas:
                if canvas1.gettags(obj)[0] != 'setka':
                    if canvas1.type(obj) != 'text':
                        file.write(
                            f"{canvas1.type(obj)} {canvas1.gettags(obj)[0]} {canvas1.itemcget(obj, 'fill')} "
                            f"{canvas1.coords(obj)}\n"
                        )
                    else:
                        file.write(
                            f"{canvas1.type(obj)} {canvas1.gettags(obj)[0]} "
                            f"{canvas1.itemconfig(obj)['text'][-1].replace(' ', '_')} "
                            f"{canvas1.itemcget(obj, 'font')} {canvas1.coords(obj)}\n"
                        )
            draw_setka(canvas1, setka_show, width, height, SIZE_GRID)
            file.write(str(len(MASSIV_CONNECT)) + '\n')
            for i in MASSIV_CONNECT:
                file.write(f'{i} {" ".join(MASSIV_CONNECT[i])}\n')


def load_objects(path=''):
    global tag_object, SIZE_GRID, MASSIV_CONNECT
    if path == '':
        file_path = fd.askopenfilename(filetypes=[('Text Files', '*.txt')])
    else:
        file_path = path
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            SIZE_GRID = int(file.readline().replace('\n', ''))
            canvas1.delete('all')
            draw_setka(canvas1, setka_show, width, height, SIZE_GRID)
            reset(canvas1)
            n = int(file.readline())
            for _ in range(n):
                line = file.readline().split()
                obj_type = line[0]
                obj_tag = line[1]
                obj_color = line[2]
                coords = ' '.join(map(str, line[3:]))
                tag_object = max(int(obj_tag), tag_object)
                if obj_type == 'line':
                    eval(f'canvas1.create_line({eval(coords)},fill="{obj_color}",tags="{obj_tag}",width=3)')
                elif obj_type == 'text':
                    mas = coords.split('[')
                    eval(
                        f'canvas1.create_text({"[" + mas[-1]}, font= "{mas[0]}", text="{obj_color.replace("_", " ")}",'
                        f'tags="{obj_tag}")')
                else:
                    eval(f'canvas1.create_{obj_type}({eval(coords)},fill="{obj_color}",tags="{obj_tag}")')
            tag_object = tag_object + 1
            n = int(file.readline())
            for _ in range(n):
                line = file.readline().split()
                ind = line[0]
                value = line[1:]
                MASSIV_CONNECT[ind] = set(value)
            if memory_selected_tab == 1:  # для обновления информации на одном из экранов
                copy_canvas(canvas1, canvas2, 'заполнение бд')
            elif memory_selected_tab == 2:
                copy_canvas(canvas1, canvas3, 'поиск товара')


def connect_dots(canvas):
    def loading_connect_dots(progress_bar):
        for widget in root.winfo_children():
            if widget.winfo_class() == 'Button':
                widget["state"] = "disabled"
        global tag_object, scale_status
        scale_status = False

        reset(canvas, tag_object_flag=False)
        mas = []
        for obj in canvas.find_all():
            if canvas.type(obj) == 'oval' and canvas.gettags(obj)[0] != 'metka':
                mas_coord = canvas.coords(obj)
                mas.append(
                    [canvas.gettags(obj)[0], (mas_coord[0] + mas_coord[2]) // 2,
                     (mas_coord[1] + mas_coord[3]) // 2])
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
        draw_setka(canvas, setka_show, width, height, SIZE_GRID)
        for widget in root.winfo_children():
            if widget.winfo_class() == 'Button':
                widget["state"] = "normal"
        scale_status = True

    progress = ttk.Progressbar(root, length=300, mode='determinate')
    progress.place(x=10, y=height + 25)
    progress['maximum'] = 100
    loading_connect_dots(progress)
    progress.destroy()
    canvas.delete('line')


def copy_canvas(source_canvas, target_canvas, type_copy=''):
    if source_canvas != target_canvas:
        target_canvas.delete("all")
    reset(source_canvas, tag_object_flag=False)
    for item in source_canvas.find_all():
        coords = source_canvas.coords(item)
        item_type = source_canvas.type(item)
        options = source_canvas.itemconfig(item)
        tags = source_canvas.gettags(item)
        if item_type == "rectangle":
            target_canvas.create_rectangle(coords, fill=options["fill"][-1], tags=tags)
        elif item_type == "oval":
            target_canvas.create_oval(coords, fill=options["fill"][-1], tags=tags)
            if type_copy == 'заполнение бд':
                x1, y1, x2, y2 = coords
                target_canvas.create_text((x1 + x2) / 2, y1 + SIZE_GRID // 2, text=tags, fill='black',
                                          font='Verdana 32 bold')
        elif item_type == "line" and tags[0] != 'setka':
            if type_copy == 'редактирование':
                target_canvas.create_line(coords, fill='blue', width=3, tags=tags)
            else:
                target_canvas.create_line(coords, fill='#D0D0D0', width=1, tags=tags)
        elif item_type == "text":
            if type_copy == 'заполнение бд' and str(tags) == '()':
                target_canvas.create_text(coords, text=options["text"][-1], fill=options["fill"][-1], tags=tags)
            elif str(tags) != '()':
                font_config = source_canvas.itemcget(item, "font")
                target_canvas.create_text(
                    coords,
                    text=options["text"][-1],
                    font=font_config,
                    fill=options["fill"][-1],
                    tags=tags,
                    state=options['state'][-1]
                )
    draw_setka(target_canvas, setka_show, width, height, SIZE_GRID)


def on_tab_changed(event):
    selected_tab = event.widget.index("current")
    global memory_selected_tab
    if selected_tab == 0 and memory_selected_tab in (1, 2):
        eval(f"copy_canvas(canvas{memory_selected_tab + 1}, canvas1, 'редактирование')")
    elif selected_tab == 1 and memory_selected_tab == 0:
        copy_canvas(canvas1, canvas2, 'заполнение бд')
    elif selected_tab == 2 and memory_selected_tab == 0:
        copy_canvas(canvas1, canvas3, 'поиск товара')
    elif selected_tab == 2 and memory_selected_tab == 1:
        copy_canvas(canvas2, canvas3, 'поиск товара')
        copy_canvas(canvas2, canvas1, 'редактирование')
    elif selected_tab == 1 and memory_selected_tab == 2:
        copy_canvas(canvas3, canvas2, 'заполнение бд')
        copy_canvas(canvas3, canvas1, 'редактирование')

    memory_selected_tab = selected_tab


root = tk.Tk()
root.title('навигатор')
root.geometry("1300x650")

vibor = 'стрелка'  # выбор режима
x_stena, y_stena = -1, -1
x_put, y_put = -1, -1
x_polka, y_polka = -1, -1
x_lineyka, y_lineyka = -1, -1
x_text, y_text = -1, -1
last_x, last_y = -1, -1
font_settings = r'@Arial\ Unicode\ MS 10 normal roman'
font_text = 'текст'
moving_status = False
scale_status = True
information_menu_status = False
tag_object = 0
start_coordinat_tag = ''
setka_show = tk.BooleanVar()
setka_show.set(True)
text_show = tk.BooleanVar()
text_show.set(True)

_SIZE_SCALE = 8
SIZE = 40
RADIUS = _SIZE_SCALE
SIZE_GRID = _SIZE_SCALE
memory_selected_tab = 0

MASSIV_CONNECT = {}
CONFIGURATION = {
    'file_open': "../DATE/new_format.txt",
    'bd_tovar': "../DATE/bd_tovar.txt",
    'telegram_bot': "../DATE/telegram.py"
}

menu = tk.Menu()

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Сохранить как", command=save_objects)
file_menu.add_command(label="Загрузить", command=load_objects)
file_menu.add_separator()
file_menu.add_command(label="Очистить экран",
                      command=lambda: eval(f'reset(canvas{memory_selected_tab + 1}, clear_canvas=True)'))
file_menu.add_command(label="Выйти", command=lambda: exit())
menu.add_cascade(label="Файл", menu=file_menu)

settings_menu = tk.Menu(menu, tearoff=0)
settings_menu.add_command(label="Подключение БД товара", command=lambda: bd_tovara(root, CONFIGURATION))
settings_menu.add_command(label="Подключение телеграм бота", command=lambda: telegram_bot(root, CONFIGURATION))
settings_menu.add_command(label="Соединение всех меток", command=lambda: connect_dots(canvas1))
menu.add_cascade(label="Настройки", menu=settings_menu)

vid_menu = tk.Menu(menu, tearoff=0)
vid_menu.add_checkbutton(label="Отображение сетки", onvalue=1, offvalue=0,
                         variable=setka_show,
                         command=lambda: draw_setka(eval(f'canvas{memory_selected_tab + 1}'), setka_show, width, height,
                                                    SIZE_GRID))
vid_menu.add_checkbutton(label="Отображение текста", onvalue=1, offvalue=0, variable=text_show,
                         command=lambda: hide_text(eval(f'canvas{memory_selected_tab + 1}'), text_show))
menu.add_cascade(label="Вид", menu=vid_menu)

tool_menu = tk.Menu(menu, tearoff=0)
tool_menu.add_command(label="Стрелка", command=lambda: do_vibor('стрелка'))
tool_menu.add_command(label="Стена", command=lambda: do_vibor('стена'))
tool_menu.add_command(label="Полка", command=lambda: do_vibor('полка'))
tool_menu.add_command(label="Метка", command=lambda: do_vibor('метка'))
tool_menu.add_command(label="Путь", command=lambda: do_vibor('путь'))
tool_menu.add_command(label="Текст", command=lambda: do_vibor('текст'))
tool_menu.add_command(label="Линейка", command=lambda: do_vibor('линейка'))
tool_menu.add_separator()
tool_menu.add_command(label="Перемещение", command=lambda: do_vibor('перемещение'))
tool_menu.add_command(label="Удаление", command=lambda: do_vibor('удалить'))
menu.add_cascade(label="Инструменты", menu=tool_menu)

information_menu = tk.Menu(menu, tearoff=0)
information_menu.add_command(label="Как пользоваться")
menu.add_cascade(label="О приложении", menu=information_menu)

root.config(menu=menu)

width = 1800
height = 600
notebook = ttk.Notebook(root, width=width, height=height)

notebook.place(x=0, y=0)
page_1 = tk.Frame(notebook)
canvas1 = tk.Canvas(page_1, bg="white", width=width, height=height)
canvas1.pack(fill="both", expand=True)
notebook.add(page_1, text="Редактирование")

image_strelka = ImageTk.PhotoImage(
    image=Image.open("../image_navigator/стрелка.png").resize((SIZE, SIZE), Image.LANCZOS))
button_strelka = tk.Button(page_1, image=image_strelka, command=lambda: do_vibor('стрелка'))
button_strelka.place(x=10, y=0)

image_metka = ImageTk.PhotoImage(image=Image.open("../image_navigator/метка.png").resize((SIZE, SIZE), Image.LANCZOS))
button_metka = tk.Button(page_1, image=image_metka, command=lambda: do_vibor('метка'))
button_metka.place(x=10, y=1 * (SIZE + 10) + SIZE // 2)

image_put = ImageTk.PhotoImage(image=Image.open("../image_navigator/путь.png").resize((SIZE, SIZE), Image.LANCZOS))
button_put = tk.Button(page_1, image=image_put, command=lambda: do_vibor('путь'))
button_put.place(x=10, y=2 * (SIZE + 10) + SIZE // 2)

image_stena = ImageTk.PhotoImage(image=Image.open("../image_navigator/стена.jpg").resize((SIZE, SIZE), Image.LANCZOS))
button_stena = tk.Button(page_1, image=image_stena, command=lambda: do_vibor('стена'))
button_stena.place(x=10, y=3 * (SIZE + 10) + SIZE // 2)

image_polka = ImageTk.PhotoImage(image=Image.open("../image_navigator/полка.jpg").resize((SIZE, SIZE), Image.LANCZOS))
button_polka = tk.Button(page_1, image=image_polka, command=lambda: do_vibor('полка'))
button_polka.place(x=10, y=4 * (SIZE + 10) + SIZE // 2)

image_move = ImageTk.PhotoImage(
    image=Image.open("../image_navigator/перемещение.png").resize((SIZE, SIZE), Image.LANCZOS))
button_move = tk.Button(page_1, image=image_move, command=lambda: do_vibor('перемещение'))
button_move.place(x=10, y=5 * (SIZE + 10) + SIZE // 2)

image_delete = ImageTk.PhotoImage(
    image=Image.open("../image_navigator/удалить.jpeg").resize((SIZE, SIZE), Image.LANCZOS))
button_delete = tk.Button(page_1, image=image_delete, command=lambda: do_vibor('удалить'))
button_delete.place(x=10, y=6 * (SIZE + 10) + SIZE // 2)

image_lineyka = ImageTk.PhotoImage(
    image=Image.open("../image_navigator/линейка.jpg").resize((SIZE, SIZE), Image.LANCZOS))
button_lineyka = tk.Button(page_1, image=image_lineyka, command=lambda: do_vibor('линейка'))
button_lineyka.place(x=10, y=7 * (SIZE + 10) + SIZE // 2)

image_text = ImageTk.PhotoImage(image=Image.open("../image_navigator/текст.png").resize((SIZE, SIZE), Image.LANCZOS))
button_text = tk.Button(page_1, image=image_text, command=lambda: do_vibor('текст'))
button_text.place(x=10, y=8 * (SIZE + 10) + SIZE // 2)

page_2 = tk.Frame(notebook)
canvas2 = tk.Canvas(page_2, bg="white", width=width, height=height)
canvas2.pack(fill="both", expand=True)
notebook.add(page_2, text="Заполнение БД")

page_3 = tk.Frame(notebook)
width_settings = 500
canvas3 = tk.Canvas(page_3, bg="white", width=width, height=height)
canvas3.pack(fill="both", expand=True, padx=width_settings)
notebook.add(page_3, text="Поиск товара")
find_tovar(width_settings, height, canvas3, page_3)

load_objects(CONFIGURATION['file_open'])
draw_setka(canvas1, setka_show, width, height, SIZE_GRID)

canvas1.bind('<Button-1>', lambda event: on_press_left(event, canvas1))
canvas1.bind('<Button-4>', lambda event: scale_all(event, canvas1, False))
canvas1.bind('<Button-5>', lambda event: scale_all(event, canvas1, True))
canvas1.bind("<MouseWheel>", lambda event: scale_all(event, canvas1))
canvas1.bind('<Button-3>', lambda event: on_press_right(event, canvas1))

canvas2.bind('<Button-4>', lambda event: scale_all(event, canvas2, False))
canvas2.bind('<Button-5>', lambda event: scale_all(event, canvas2, True))
canvas2.bind("<MouseWheel>", lambda event: scale_all(event, canvas2))

canvas3.bind('<Button-4>', lambda event: scale_all(event, canvas3, False))
canvas3.bind('<Button-5>', lambda event: scale_all(event, canvas3, True))
canvas3.bind("<MouseWheel>", lambda event: scale_all(event, canvas3))

notebook.bind("<<NotebookTabChanged>>", lambda event: on_tab_changed(event))

root.mainloop()
