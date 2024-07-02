import tkinter as tk
import tkinter.filedialog
import subprocess


def telegram_bot(root, configuration):
    def choose_file(path=''):
        if path == '':
            file_path = tk.filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        else:
            file_path = path
        file_path_label.config(text="Файл: " + file_path)
        configuration['telegram_bot'] = file_path
        file_content_text.configure(state=tk.NORMAL)
        try:
            with open(configuration['telegram_bot'], 'r', encoding='utf-8') as file:
                file_content = file.read()
                file_content_text.delete("1.0", tk.END)
                file_content_text.insert(tk.END, file_content)
        except Exception as ex:
            file_content_text.delete("1.0", tk.END)
            file_content_text.insert(tk.END, "Не удалось открыть файл\n")
            file_content_text.insert(tk.END, str(ex))
        file_content_text.configure(state=tk.DISABLED)

    def run_file():
        if configuration['telegram_bot']:
            subprocess.Popen(["python", configuration['telegram_bot']])
        else:
            file_path_label.config(text="Не выбран файл")

    telegram_bot_window = tk.Toplevel(root)
    telegram_bot_window.grab_set()
    telegram_bot_window.title("Телеграмм бот")
    telegram_bot_window.geometry('700x700')

    choose_button = tk.Button(telegram_bot_window, text="Выберите файл", command=choose_file)
    choose_button.place(x=10, y=20)

    file_path_label = tk.Label(telegram_bot_window, text="Файл: None")
    file_path_label.place(x=150, y=20)

    file_content_text = tk.Text(telegram_bot_window, height=30, width=80, state=tk.DISABLED)
    file_content_text.place(x=10, y=100)

    vertical_scrollbar = tk.Scrollbar(telegram_bot_window, command=file_content_text.yview)
    vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    file_content_text.config(yscrollcommand=vertical_scrollbar.set)

    run_button = tk.Button(telegram_bot_window, text="Запустить код", command=run_file)
    run_button.place(x=550, y=600)

    choose_file(path=configuration['telegram_bot'])

    telegram_bot_window.mainloop()
    telegram_bot_window.wait_window()
    return configuration
