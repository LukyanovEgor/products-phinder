import tkinter as tk


def find_tovar(wid, height, canvas3, page_3):
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
        print('нужно сделать отрисовку пути на новой карте')

    def vbr_point():
        print('нужно сделать выбор точки')

    def hide_setting():
        if hide_button['text'] == '<':
            canvas3.pack_configure(padx=0)
            canvas.place(x=-wid, y=0)
            hide_button['text'] = ">"
            hide_button.place(x=0 + 3, y=10)
        else:
            canvas3.pack_configure(padx=wid)
            canvas.place(x=0, y=0)
            hide_button['text'] = "<"
            hide_button.place(x=wid + 3, y=10)

    def load_tovar():
        print('сделать загрузку из файла')

    canvas = tk.Canvas(page_3, width=wid, height=height)
    canvas.place(x=0, y=0)

    index_label = tk.Label(canvas, text="Введите код товара")
    index_label.place(x=10, y=10)

    index_entry = tk.Entry(canvas)
    index_entry.place(x=10, y=50)

    add_button = tk.Button(canvas, text="Добавить", command=add_index)
    add_button.place(x=10, y=100)
    remove_button = tk.Button(canvas, text="Удалить", command=remove_selected_items)
    remove_button.place(x=10, y=130)
    load_button = tk.Button(canvas, text="Загрузить", command=load_tovar)
    load_button.place(x=10, y=130)

    find_button = tk.Button(canvas, text="Построить маршрут", command=draw_path)
    find_button.place(x=10, y=250)

    start_point_button = tk.Button(canvas, text="Выбрать начальную точку", command=vbr_point)
    start_point_button.place(x=10, y=300)

    finish_point_button = tk.Button(canvas, text="Выбрать финишную точку", command=vbr_point)
    finish_point_button.place(x=10, y=330)

    hide_button = tk.Button(page_3, text="<", height=5, width=2, command=hide_setting)
    hide_button.place(x=wid + 3, y=10)

    listbox = tk.Listbox(canvas, width=40, height=15)
    listbox.place(x=200, y=10)
