import os

if os.name == 'nt':
    # taken from https://stackoverflow.com/questions/8677627/getting-mouse-presses-on-a-console-window-for-python

    import win32con
    import win32file
    from win32console import *
    import traceback, time

    virtual_keys={}
    for k,v in win32con.__dict__.items():
        if k.startswith('VK_'):
            virtual_keys[v]=k 

    free_console=True
    try:
        AllocConsole()
    except error as exc:
        if exc.winerror!=5:
            raise
        ## only free console if one was created successfully
        free_console=False

    stdout=GetStdHandle(STD_OUTPUT_HANDLE)

    conin=PyConsoleScreenBufferType( win32file.CreateFile( "CONIN$", win32con.GENERIC_READ|win32con.GENERIC_WRITE, win32con.FILE_SHARE_READ, None, win32con.OPEN_EXISTING, 0, 0))

    conin.SetConsoleMode(ENABLE_WINDOW_INPUT | ENABLE_MOUSE_INPUT)

    newbuffer=CreateConsoleScreenBuffer()
    newbuffer.SetConsoleActiveScreenBuffer()
    newbuffer.SetConsoleTextAttribute(FOREGROUND_RED|FOREGROUND_INTENSITY
            |BACKGROUND_GREEN|BACKGROUND_INTENSITY)
    newbuffer.WriteConsole('This is a new screen buffer\n')

    newbuffer.SetConsoleTextAttribute(FOREGROUND_RED|FOREGROUND_INTENSITY
            |BACKGROUND_GREEN|BACKGROUND_INTENSITY)
    newbuffer.WriteConsole('Press some keys, click some characters with the mouse\n')

    newbuffer.SetConsoleTextAttribute(FOREGROUND_BLUE|FOREGROUND_INTENSITY
            |BACKGROUND_RED|BACKGROUND_INTENSITY)
    newbuffer.WriteConsole('Hit "Esc" key to quit\n')


    breakout=False
    while not breakout:
        input_records=conin.ReadConsoleInput(10)
        for input_record in input_records:
            if input_record.EventType==KEY_EVENT:
                if input_record.KeyDown:
                    if input_record.Char=='\0':
                        newbuffer.WriteConsole(virtual_keys.get(input_record.VirtualKeyCode, 'VirtualKeyCode: %s' %input_record.VirtualKeyCode))
                    else:
                        newbuffer.WriteConsole(input_record.Char)
                    if input_record.VirtualKeyCode==win32con.VK_ESCAPE:
                        breakout=True
                        break
            elif input_record.EventType==MOUSE_EVENT:
                if input_record.EventFlags==0:  ## 0 indicates a button event
                    if input_record.ButtonState!=0:   ## exclude button releases
                        pos=input_record.MousePosition
                        # switch the foreground and background colors of the character that was clicked
                        attr=newbuffer.ReadConsoleOutputAttribute(Length=1, ReadCoord=pos)[0]
                        new_attr=attr
                        if attr&FOREGROUND_BLUE:
                            new_attr=(new_attr&~FOREGROUND_BLUE)|BACKGROUND_BLUE
                        if attr&FOREGROUND_RED:
                            new_attr=(new_attr&~FOREGROUND_RED)|BACKGROUND_RED
                        if attr&FOREGROUND_GREEN:
                            new_attr=(new_attr&~FOREGROUND_GREEN)|BACKGROUND_GREEN

                        if attr&BACKGROUND_BLUE:
                            new_attr=(new_attr&~BACKGROUND_BLUE)|FOREGROUND_BLUE
                        if attr&BACKGROUND_RED:
                            new_attr=(new_attr&~BACKGROUND_RED)|FOREGROUND_RED
                        if attr&BACKGROUND_GREEN:
                            new_attr=(new_attr&~BACKGROUND_GREEN)|FOREGROUND_GREEN
                        newbuffer.WriteConsoleOutputAttribute((new_attr,),pos)
            else:
                newbuffer.WriteConsole(str(input_record))
        time.sleep(0.1)

    newbuffer.Close()

    if free_console:
         FreeConsole()

else:
    # taken from https://stackoverflow.com/questions/56303971/how-to-enable-mouse-movement-events-in-python-curses

    import curses

    screen = curses.initscr()
    screen.keypad(1)
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.flushinp()
    curses.noecho()
    screen.clear()

    while True:
        key = screen.getch()
        screen.clear()
        screen.addstr(0, 0, 'key: {}'.format(key))
        if key == curses.KEY_MOUSE:
            _, x, y, _, button = curses.getmouse()
            screen.addstr(1, 0, f'x, y, button = {x}, {y}, {button}')
        elif key == 27:
            break

    curses.endwin()
    curses.flushinp()

