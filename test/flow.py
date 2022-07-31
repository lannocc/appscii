

prints = [
    "This is some text that will be flowed. Each entry in this array represents where a newline is manually entered. So here we go...",
    "Another line.",
    "",
    "A blank line should be above and below me. But this entry should flow into multiple lines. So here we have some more text just to be sure it's long enough.",
    "",
    "The End.",
]


def flow(cols, rows, words=False, align=-1, up=0):
    print()
    print(f'flow({cols},{rows},{words},{align},{up}):')
    print('=== BEGIN TEXT ===')

    lines = [ ]

    for entry in prints:
        while len(entry) > cols:
            chunk = entry[:cols]

            if words and entry[cols] != ' ' and chunk[-1] != ' ' \
                    and ' ' in chunk:
                idx = chunk.rindex(' ')
                chunk = entry[:idx]
                entry = entry[idx+1:]

            else:
                entry = entry[cols:]

            lines.append(chunk)

        lines.append(entry)

    while len(lines) < rows:
        lines.append('')

    if up > 0:
        extra = len(lines) - rows
        if up > extra: up = extra
        showing = lines[-(rows+extra):-up]

    elif up < 0:
        showing = lines[:rows]

    else:
        showing = lines[-rows:]

    rleft = True

    for line in showing:
        if align < 0: # left
            print(line)

        elif align > 0: # right
            print(' ' * (cols - len(line)) + line)

        else: # center
            diff = cols - len(line)
            if diff:
                left = ' ' * (diff // 2)
                right = left
                if diff % 2:
                    if rleft: left += ' '
                    else: right += ' '
                    rleft = not rleft

                print(left + line + right)

            else:
                print(line)

    print('=== END TEXT ===')
    print()


flow(41, 9)
flow(41, 9, words=True, align=0, up=2)
#flow(9, 42, words=True)

