import tkinter as tk
import tkfontchooser


def do_vibor_text(root, font_settings, font_text):
    popup = tk.Toplevel(root)
    popup.title("Ввод текста")
    popup.grab_set()

    tk.Label(popup, text="Введите ваш текст:").pack(pady=5)

    entry = tk.Entry(popup)
    entry.pack(pady=5)

    def settings_text():
        nonlocal font_settings
        font = tkfontchooser.askfont()
        if font:
            font['family'] = font['family'].replace(' ', r'\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
            if font['underline']:
                font_str += ' underline'
            if font['overstrike']:
                font_str += ' overstrike'
            font_settings = font_str

    def do_text():
        nonlocal font_text
        user_text = entry.get()
        if user_text:
            font_text = user_text.replace('_', " ")
            entry.delete(0, tk.END)
            popup.destroy()

    button1 = tk.Button(popup, text="Настройки", command=settings_text)
    button1.pack(pady=5)
    button2 = tk.Button(popup, text="Готово", command=do_text)
    button2.pack(pady=5)

    popup.wait_window()
    return font_settings, font_text


def hide_text(canvas, show):
    if show.get() == 0:
        for obj in canvas.find_all():
            if canvas.type(obj) == 'text' and canvas.gettags(obj)[0] != 'lineyka':
                canvas.itemconfigure(obj, state="hidden")
                canvas.scale('all', 0, 0, 1, 1)  # чтоб буквы не оставляли след
    else:
        for obj in canvas.find_all():
            if canvas.type(obj) == 'text':
                canvas.itemconfigure(obj, state="normal")
