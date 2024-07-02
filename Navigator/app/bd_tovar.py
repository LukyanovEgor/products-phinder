import tkinter as tk
import tkinter.filedialog as fd
from tkinter import ttk


def bd_tovara(root, configuration):
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
            configuration['bd_tovar'] = file_path
            tree.delete(*tree.get_children())
            for line in file:
                data = line.strip().split()
                tree.insert("", tk.END, values=data)

    def save_file():
        file = open(configuration['bd_tovar'], 'w')
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

    browse_file(configuration['bd_tovar'])

    window_bd_tovar.mainloop()
    window_bd_tovar.wait_window()
    return configuration
