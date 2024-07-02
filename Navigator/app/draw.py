from math import sqrt


def draw_text(canvas, x, y, tag, show, settings, font_text, tag_object):
    canvas.delete('text')
    if show.get() == 0:
        canvas.create_text(x, y, text=font_text, tags=str(tag), fill='black', font=settings, state="hidden")
    else:
        canvas.create_text(x, y, text=font_text, tags=str(tag), fill='black', font=settings, state="normal")
    if tag != 'text':
        tag_object += 1
        font_text = ''
    canvas.scale('all', 0, 0, 1, 1)  # чтоб буквы не оставляли след
    return font_text, tag_object


def draw_setka(canvas, show, width, height, size):
    canvas.delete('setka')
    if show.get() == 1:
        for line1 in range(0, width, int(size)):
            canvas.tag_lower(canvas.create_line((line1, 0), (line1, height), fill='#DCDCDC', tags='setka'))

        for line1 in range(0, height, int(size)):
            canvas.tag_lower(canvas.create_line((0, line1), (width, line1), fill='#DCDCDC', tags='setka'))


def draw_stena(canvas, x, y, tag, color, x_new, y_new, size, global_tag):
    canvas.delete('stena')
    canvas.create_rectangle(x_new, y_new, (x // size) * size,
                            (y // size) * size, fill=color, outline="#000000", tags=tag)
    if tag != 'stena':
        global_tag += 1
    return global_tag


def draw_lineyka(canvas, x, y, x_lineyka, y_lineyka, size):
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
                                   text=f'{round(sqrt(x_1 ** 2 + y_1 ** 2) / size, 2)} м', font='Verdana 12',
                                   fill="black",
                                   tags='lineyka')
    rect_item = canvas.create_rectangle(canvas.bbox(text_item), outline="red", fill="white", tags='lineyka')
    canvas.tag_raise(text_item, rect_item)
    return x_lineyka, y_lineyka


def draw_metka(canvas, x, y, tag, color, size, radius, scale, tag_object, mas):
    canvas.delete('metka')
    q = max(size // 2, 1)
    canvas.create_oval((x // q) * q - radius * size // scale / 2,
                       (y // q) * q - radius * size // scale / 2,
                       (x // q) * q + radius * size // scale / 2,
                       (y // q) * q + radius * size // scale / 2,
                       fill=color, tags=tag)
    if tag != 'metka':
        mas[str(tag_object)] = set()
        tag_object += 1
    return tag_object, mas


def draw_polka(canvas, x, y, tag, color_rect, color_circle, x_new, y_new, size, scale, radius, tag_object, mas):
    canvas.delete('polka')
    x_left = min(x_new, (x // size) * size)
    x_right = max(x_new, (x // size) * size)
    y_up = min(y_new, (y // size) * size)
    y_down = max(y_new, (y // size) * size)
    otstup = radius * size // scale
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
            mas[str(tag_object)] = set()
            tag += 1
            tag_object += 1

        canvas.create_oval(x_left + (i * (len_x // (t_x + 1))) + otstup / 2,
                           y_up,
                           x_left + (i * (len_x // (t_x + 1))) - otstup / 2,
                           y_up - 2 * otstup / 2,
                           fill=color_circle,
                           tags=tag)
        if tag != 'polka':
            mas[str(tag_object)] = set()
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
            mas[str(tag_object)] = set()
            tag += 1
            tag_object += 1
        canvas.create_oval(x_right,
                           y_up + (i * (len_y // (t_y + 1))) - otstup / 2,
                           x_right + 2 * otstup / 2,
                           y_up + (i * (len_y // (t_y + 1))) + otstup / 2,
                           fill=color_circle, tags=tag)
        if tag != 'polka':
            mas[str(tag_object)] = set()
            tag_object += 1
            tag += 1

    canvas.create_oval(x_left, y_up,
                       x_left - 2 * otstup / 2,
                       y_up - 2 * otstup / 2, fill=color_circle,
                       tags=tag)
    if tag != 'polka':
        mas[str(tag_object)] = set()
        tag_object += 1
        tag += 1
    canvas.create_oval(x_left, y_down,
                       x_left - 2 * otstup / 2,
                       y_down + 2 * otstup / 2,
                       fill=color_circle,
                       tags=tag)
    if tag != 'polka':
        mas[str(tag_object)] = set()
        tag_object += 1
        tag += 1
    canvas.create_oval(x_right, y_up,
                       x_right + 2 * otstup / 2,
                       y_up - 2 * otstup / 2, fill=color_circle,
                       tags=tag)
    if tag != 'polka':
        mas[str(tag_object)] = set()
        tag_object += 1
        tag += 1
    canvas.create_oval(x_right, y_down,
                       x_right + 2 * otstup / 2,
                       y_down + 2 * otstup / 2,
                       fill=color_circle, tags=tag)

    if tag != 'polka':
        mas[str(tag_object)] = set()
        tag_object += 1
        tag += 1
    # print(mas)
    return tag_object, mas
