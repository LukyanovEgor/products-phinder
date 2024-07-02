def delete_connected_point(canvas, tag, mas):
    if canvas.type(tag) == 'oval':
        oval_x1, oval_y1, oval_x2, oval_y2 = canvas.coords(tag)
        for obj in canvas.find_all():
            if canvas.type(obj) == 'line' and canvas.gettags(obj)[0] != 'setka':
                x1, y1, x2, y2 = canvas.coords(obj)
                if ((oval_x1 + oval_x2) / 2 == x1 and (oval_y1 + oval_y2) / 2 == y1) or (
                        (oval_x1 + oval_x2) / 2 == x2 and (oval_y1 + oval_y2) / 2 == y2):
                    canvas.delete(obj)
        for value in mas[canvas.gettags(tag)[0]]:
            mas[value].discard(canvas.gettags(tag)[0])
        del mas[canvas.gettags(tag)[0]]
    if canvas.type(tag) == 'line':
        line_x1, line_y1, line_x2, line_y2 = canvas.coords(tag)
        tag_oval = []
        for obj in canvas.find_all():
            if canvas.type(obj) == 'oval':
                x1, y1, x2, y2 = canvas.coords(obj)
                if ((x1 + x2) / 2 == line_x1 and (y1 + y2) / 2 == line_y1) or (
                        (x1 + x2) / 2 == line_x2 and (y1 + y2) / 2 == line_y2):
                    tag_oval.append(canvas.gettags(obj)[0])
        mas[tag_oval[0]].discard(tag_oval[1])
        mas[tag_oval[1]].discard(tag_oval[0])
    print(mas)
    canvas.delete(tag)
    return mas

