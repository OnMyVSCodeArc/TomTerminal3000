import curses


def _clamp_cursor_x(lines, cursor_y, cursor_x):
    return min(cursor_x, len(lines[cursor_y]))


def run_editor(stdscr, filename, lines, on_save):
    if not lines:
        lines.append("")

    try:
        curses.curs_set(1)
    except curses.error:
        pass

    cursor_y, cursor_x = 0, 0
    scroll_offset = 0
    status_msg = ""

    while True:
        height, width = stdscr.getmaxyx()
        content_height = max(1, height - 3)

        if cursor_y < scroll_offset:
            scroll_offset = cursor_y
        elif cursor_y >= scroll_offset + content_height:
            scroll_offset = cursor_y - content_height + 1

        stdscr.erase()

        header = f" EDITOR - {filename} "[:max(0, width - 1)]
        try:
            stdscr.addstr(0, 0, header, curses.A_REVERSE)
        except curses.error:
            pass

        for row in range(content_height):
            line_idx = scroll_offset + row
            if line_idx >= len(lines):
                break
            try:
                stdscr.addstr(row + 1, 0, lines[line_idx][:max(0, width - 1)])
            except curses.error:
                pass

        help_row = height - 1
        help_text = status_msg or "^O Save   ^X Exit & Save   Arrows/Home/End move   Backspace/Del remove"
        try:
            stdscr.addstr(help_row, 0, help_text[:max(0, width - 1)], curses.A_REVERSE)
        except curses.error:
            pass

        try:
            stdscr.move(cursor_y - scroll_offset + 1, min(cursor_x, max(0, width - 1)))
        except curses.error:
            pass

        stdscr.refresh()
        status_msg = ""

        key = stdscr.getch()

        if key in (curses.KEY_BACKSPACE, 127, 8):
            if cursor_x > 0:
                line = lines[cursor_y]
                lines[cursor_y] = line[:cursor_x - 1] + line[cursor_x:]
                cursor_x -= 1
            elif cursor_y > 0:
                prev_len = len(lines[cursor_y - 1])
                lines[cursor_y - 1] += lines[cursor_y]
                del lines[cursor_y]
                cursor_y -= 1
                cursor_x = prev_len

        elif key == curses.KEY_DC:
            line = lines[cursor_y]
            if cursor_x < len(line):
                lines[cursor_y] = line[:cursor_x] + line[cursor_x + 1:]
            elif cursor_y < len(lines) - 1:
                lines[cursor_y] += lines[cursor_y + 1]
                del lines[cursor_y + 1]

        elif key in (10, 13, curses.KEY_ENTER):
            line = lines[cursor_y]
            lines[cursor_y] = line[:cursor_x]
            lines.insert(cursor_y + 1, line[cursor_x:])
            cursor_y += 1
            cursor_x = 0

        elif key == curses.KEY_UP:
            if cursor_y > 0:
                cursor_y -= 1
                cursor_x = _clamp_cursor_x(lines, cursor_y, cursor_x)

        elif key == curses.KEY_DOWN:
            if cursor_y < len(lines) - 1:
                cursor_y += 1
                cursor_x = _clamp_cursor_x(lines, cursor_y, cursor_x)

        elif key == curses.KEY_LEFT:
            if cursor_x > 0:
                cursor_x -= 1
            elif cursor_y > 0:
                cursor_y -= 1
                cursor_x = len(lines[cursor_y])

        elif key == curses.KEY_RIGHT:
            if cursor_x < len(lines[cursor_y]):
                cursor_x += 1
            elif cursor_y < len(lines) - 1:
                cursor_y += 1
                cursor_x = 0

        elif key == curses.KEY_HOME:
            cursor_x = 0

        elif key == curses.KEY_END:
            cursor_x = len(lines[cursor_y])

        elif key == 15:  # Ctrl+O
            status_msg = on_save(lines)

        elif key == 24:  # Ctrl+X
            on_save(lines)
            break

        elif key == curses.KEY_RESIZE:
            continue

        elif key == 9:  # Tab
            line = lines[cursor_y]
            lines[cursor_y] = line[:cursor_x] + "\t" + line[cursor_x:]
            cursor_x += 1

        elif 32 <= key <= 126:
            line = lines[cursor_y]
            lines[cursor_y] = line[:cursor_x] + chr(key) + line[cursor_x:]
            cursor_x += 1
