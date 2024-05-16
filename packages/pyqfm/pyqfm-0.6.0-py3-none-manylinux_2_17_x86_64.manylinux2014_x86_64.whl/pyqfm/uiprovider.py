import curses
import time

logoList = [
    "   __ _    ________  ___  _____ ____  __ __ ",
    "  / __ \  / ____/  |/  / / ___// __ \/ //_/ ",
    " / / / / / /_  / /|_/ /  \__ \/ / / / ,<    ",
    "/ /_/ / / __/ / /  / /  ___/ / /_/ / /| |   ",
    "\___\_\/_/   /_/  /_/  /____/_____/_/ |_|   ",
]

disconnectList = [
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ",
"[DISCONNECTED]\n",
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
]

menuList = [
    "1.  Communication Setup\n",
    "------------------------------------------\n",
    "2.  System Configuration (System Parameter)\n",
    "3.  Reset System Parameter (Factory Reset)\n",
    "------------------------------------------\n",
    "4.  Enroll by scan\n",
    "5.  Identify by scan\n",
    "6.  Verify by scan\n",
    "7.  Delete template\n",
    "8.  Delete all templates\n",
    "9.  Get all user informations\n",
    "10. Read all templates\n",
    "11. Enroll by template\n",
    "12. Identify by template\n",
    "13. Scan Template\n",
    "------------------------------------------\n",
    "14. Enroll by image\n",
    "15. Identify by image\n",
    "16. Scan image\n",
    "------------------------------------------\n",
    "17. Upgrade firmware\n",
    "18. Update Patch\n",
    "19. DFU Mode\n",
    "------------------------------------------\n",
    "20. Free Scan (Continuous Identification)\n",
    "21. Read QR Code\n",
    "------------------------------------------\n",
    "22. Change Key\n",
    "23. Secure Packet Protocol\n",
    "24. Packet Trace\n",
    "25. Database Management\n",
    "26. Exit\n",
]

keyList = [
    "1. Encryption Key\n",
    "2. IV Key\n",
    "3. Secure Key\n",
    "4. Encryption Key with verification\n",
    "5. IV Key with verification\n",
    "6. Secure Key with verification\n",
    "------------------------------------------\n",
    "7. Reset Encryption Key\n",
    "8. Reset IV Key\n",
    "9. Reset Secure Key\n",
    "------------------------------------------\n",
    "10. Verify Encryption Key\n",
    "11. Verify IV Key\n",
    "------------------------------------------\n",
    "12. Key menu Exit\n",
    ]

paramList = [
    # Timeout
    "QF_SYS_TIMEOUT",
    # Template size
    "QF_SYS_TEMPLATE_SIZE",
    # Enrollment mode
    "QF_SYS_ENROLL_MODE",
    # Security level
    "QF_SYS_SECURITY_LEVEL",
    # Encryption mode
    "QF_SYS_ENCRYPTION_MODE",
    # Firmware version
    "QF_SYS_FIRMWARE_VERSION",
    # Serial number
    "QF_SYS_SERIAL_NUMBER",
    # Baudrate
    "QF_SYS_BAUDRATE",
    # Number of enrolled templates
    "QF_SYS_ENROLLED_TEMPLATES",
    # Number of available templates
    "QF_SYS_AVAILABLE_TEMPLATES",
    # Scan success
    "QF_SYS_SEND_SCAN_SUCCESS",
    # ASCII packet
    "QF_SYS_ASCII_PACKET",
    # Rotate image
    "QF_SYS_ROTATE_IMAGE",
    # Sensitivity (Deprecated since SDK v0.3.1)
    "QF_SYS_SENSITIVITY",
    # Horizontal Sensitivity
    "QF_SYS_HORIZONTAL_SENSITIVITY",
    # Image quality
    "QF_SYS_IMAGE_QUALITY",
    # Auto response
    "QF_SYS_AUTO_RESPONSE",
    # Free scan mode
    "QF_SYS_FREE_SCAN",
    # Provisional enrollment
    "QF_SYS_PROVISIONAL_ENROLL",
    # Response delay
    "QF_SYS_RESPONSE_DELAY",
    # Matching timeout
    "QF_SYS_MATCHING_TIMEOUT",
    # Build number
    "QF_SYS_BUILD_NUMBER",
    # Lighing Condition
    "QF_SYS_LIGHTING_CONDITION",
    # Freescan delay
    "QF_SYS_FREESCAN_DELAY",
    # Template type
    "QF_SYS_TEMPLATE_TYPE",
    # Fake detection
    "QF_SYS_FAKE_DETECTION",
    # Protocol interface
    "QF_SYS_PROTOCOL_INTERFACE",
    # Kernel version
    "QF_SYS_KERNEL_VERSION",
    # Packet security
    "QF_SYS_PACKET_SECURITY",
    # Mask check level
    "QF_SYS_MASK_CHECK_LEVEL",
    # User feedback
    "QF_SYS_USER_FEEDBACK",
    # Vertical sensitivity
    "QF_SYS_VERTICAL_SENSITIVITY",
    # QFace engine version
    "QF_SYS_QFACE_ENGINE_VERSION",
    # Patch version
    "QF_SYS_PATCH_VERSION",
    # Enrollment restriction
    "QF_SYS_ENROLLMENT_RESTRICTION",
]


consoleList = [
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"                                            ",
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ",
]

class UI_CursBaseDialog:
    def __init__(self, **options):
        self.maxy, self.maxx = curses.LINES, curses.COLS
        self.win = curses.newwin(
            12, 56, int((self.maxy / 2) - 6), int((self.maxx / 2) - 28)
        )
        self.win.box()
        self.y, self.x = self.win.getmaxyx()

        self.title_attr = options.get("title_attr", curses.A_BOLD | curses.A_STANDOUT)
        self.msg_attr = options.get("msg_attr", curses.A_BOLD)
        self.opt_attr = options.get("opt_attr", curses.A_BOLD)
        self.focus_attr = options.get("focus_attr", curses.A_BOLD | curses.A_STANDOUT)
        self.title = options.get("title")
        self.message = options.get("message")
        self.timeout = options.get("timeout")
        self.default = options.get("default")
        self.AskLeft = options.get("ask_left")
        self.AskRight = options.get("ask_right")

        self.items = options.get("values")

        self.focus = 0
        self.enterKey = False

        if self.items:
            self.UP = -1
            self.DOWN = 1
            self.height, self.width = self.y, self.x
            self.max_lines = 9
            self.maxlen = 40
            self.top = 0
            self.bottom = len(self.items)
            self.current = 0
            self.page = self.bottom // self.max_lines
            self.item = ""

        self.win.keypad(1)
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def top_bottom_key_event_handler(self, max):
        self.win.refresh()
        key = self.win.getch()
        if key == curses.KEY_UP and self.focus != 0:
            self.focus -= 1
        elif key == curses.KEY_DOWN and self.focus != max - 1:
            self.focus += 1
        elif key == ord("\n"):
            self.enterKey = True

        while self.enterKey != True:
            self.display()
            ch = self.win.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.KEY_LEFT:
                self.paging(self.UP)
            elif ch == curses.KEY_RIGHT:
                self.paging(self.DOWN)
            elif ch == ord("\n"):
                break

        return self.current

    def left_right_key_event_handler(self, max):
        self.win.refresh()
        key = self.win.getch()
        if key == curses.KEY_LEFT and self.focus != 0:
            self.focus -= 1
        elif key == curses.KEY_RIGHT and self.focus != max - 1:
            self.focus += 1
        elif key == ord("\n"):
            self.enterKey = True

    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""
        # next cursor position after scrolling
        next_line = self.current + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (
            (direction == self.DOWN)
            and (next_line == self.max_lines)
            and (self.top + self.max_lines < self.bottom)
        ):
            self.top += direction
            return
        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        if (
            (direction == self.DOWN)
            and (next_line < self.max_lines)
            and (self.top + next_line < self.bottom)
        ):
            self.current = next_line
            return

    def paging(self, direction):
        """Paging the window when pressing left/right arrow keys"""
        current_page = (self.top + self.current) // self.max_lines
        next_page = current_page + direction
        # The last page may have fewer items than max lines,
        # so we should adjust the current cursor position as maximum item count on last page
        if next_page == self.page:
            self.current = min(self.current, self.bottom % self.max_lines - 1)

        # Page up
        # if current page is not a first page, page up is possible
        # top position can not be negative, so if top position is going to be negative, we should set it as 0
        if (direction == self.UP) and (current_page > 0):
            self.top = max(0, self.top - self.max_lines)
            return
        # Page down
        # if current page is not a last page, page down is possible
        if (direction == self.DOWN) and (current_page < self.page):
            self.top += self.max_lines
            return

    def display(self):
        """Display the items on window"""
        self.win.erase()
        for idx, item in enumerate(self.items[self.top : self.top + self.max_lines]):
            itemlen = self.maxlen - len(item) - len(str(self.items.index(item)))

            if idx == self.current:
                self.item = item
                # Highlight the current cursor line
                self.win.addstr(
                    idx + 1,
                    9,
                    f"{item}{'-'*itemlen}{str(self.items.index(item))}",
                    curses.color_pair(2),
                )
            else:
                self.win.addstr(
                    idx + 1,
                    9,
                    f"{item}{'-'*itemlen}{str(self.items.index(item))}",
                    curses.color_pair(1),
                )
        self.win.refresh()


class UI_showMessageDialog(UI_CursBaseDialog):
    def showMessage(self):
        showTitleMsg(self)

        if self.timeout is None or (self.timeout != 0):
            self.timeout = 0.5
        if self.timeout == 0:
            rectangle(
                self.win, 8, int(self.x / 2 - 2), 2, 3, self.opt_attr | self.focus_attr
            )
            self.win.addstr(
                9, int(self.x / 2 - 1), "OK", self.opt_attr | self.focus_attr
            )
            if self.win.getch() != ord("\n"):
                self.showMessage()
        else:
            self.win.refresh()
            time.sleep(self.timeout)


class UI_askDialog(UI_CursBaseDialog):
    def askDialog(self):
        showTitleMsg(self)
        option = (self.AskLeft, self.AskRight)
        rectangle(self.win, 8, 13 - 1, 2, len(option[0]) + 1, self.opt_attr)
        rectangle(self.win, 8, 34 - 1, 2, len(option[1]) + 1, self.opt_attr)

        pos_x = [13, 34]
        while self.enterKey != True:
            if self.focus == 0:
                self.win.addstr(9, 13, option[0], self.focus_attr | self.opt_attr)
            else:
                self.win.addstr(9, 13, option[0], self.opt_attr)

            if self.focus == 1:
                self.win.addstr(9, 34, option[1], self.focus_attr | self.opt_attr)
            else:
                self.win.addstr(9, 34, option[1], self.opt_attr)
            for i in range(2):
                if i != self.focus:
                    rectangle(
                        self.win,
                        8,
                        pos_x[i] - 1,
                        2,
                        len(option[i]) + 1,
                        curses.A_NORMAL | self.opt_attr,
                    )
                else:
                    rectangle(
                        self.win,
                        8,
                        pos_x[self.focus] - 1,
                        2,
                        len(option[self.focus]) + 1,
                        self.focus_attr | self.opt_attr,
                    )
            self.left_right_key_event_handler(2)

        if self.focus == 0:
            return option[0]
        else:
            return option[1]


class UI_valueDialog(UI_CursBaseDialog):
    def ValueDialog(self):
        self.scrollui = curses.newwin(
            19, 61, int((self.maxy / 2) - 8), int((self.maxx / 2) - 29)
        )
        y, x = self.scrollui.getmaxyx()
        rectangle(self.scrollui, 0, 0, 18, 59, self.opt_attr)

        if self.title:
            self.title = f" {self.title} "
            self.scrollui.addstr(
                1,
                int(x / 2 - len(self.title) / 2),
                self.title,
                curses.A_BOLD | curses.A_STANDOUT,
            )
            self.scrollui.addstr(self.max_lines + 5, 3, self.message, curses.A_BOLD)
            self.scrollui.addstr(
                self.max_lines + 8,
                2,
                " < Left Page > Right Page  ^ Page Up _ Page Down        ",
                curses.A_BOLD | curses.A_STANDOUT,
            )
            self.scrollui.refresh()

        # showTitleMsg(self)
        while self.enterKey != True:
            self.display()
            ch = self.win.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.KEY_LEFT:
                self.paging(self.UP)
            elif ch == curses.KEY_RIGHT:
                self.paging(self.DOWN)
            elif ch == ord("\n"):
                break

        return self.item


class UI_askFileSaveDialog(UI_CursBaseDialog):
    def fileSave(self):
        showTitleMsg(self)
        option = ("Save as", "Save", "Cancel")
        space = int(self.x / 6)
        pos_x = []

        for i in option:
            pos_x.append(space)
            rectangle(self.win, 8, space - 1, 2, len(i) + 1, self.opt_attr)
            space = space + len(i) + 8

        while self.enterKey != True:
            if self.focus == 0:
                self.win.addstr(9, pos_x[0], "Save as", self.focus_attr | self.opt_attr)
            else:
                self.win.addstr(9, pos_x[0], "Save as", self.opt_attr)

            if self.focus == 1:
                self.win.addstr(9, pos_x[1], "Save", self.focus_attr | self.opt_attr)
            else:
                self.win.addstr(9, pos_x[1], "Save", self.opt_attr)

            if self.focus == 2:
                self.win.addstr(9, pos_x[2], "Cancel", self.focus_attr | self.opt_attr)

            else:
                self.win.addstr(9, pos_x[2], "Cancel", self.opt_attr)

            for i in range(len(option)):
                if i != self.focus:
                    rectangle(
                        self.win,
                        8,
                        pos_x[i] - 1,
                        2,
                        len(option[i]) + 1,
                        curses.A_NORMAL | self.opt_attr,
                    )
                else:
                    rectangle(
                        self.win,
                        8,
                        pos_x[self.focus] - 1,
                        2,
                        len(option[self.focus]) + 1,
                        self.focus_attr | self.opt_attr,
                    )

            self.left_right_key_event_handler(len(option))

        if self.focus == 0:
            curses.echo()
            curses.cbreak()
            curses.curs_set(1)
            self.win.keypad(False)
            self.win.addstr(4, 2, "Please enter save path in the following:")
            self.win.addstr(6, 2, " " * 30, curses.A_UNDERLINE)
            filepath = self.win.getstr(6, 2, curses.A_BOLD).decode("UTF-8")

        elif self.focus == 1:
            filepath = "."
        else:
            filepath = None
        return filepath


class UI_askValueDialog(UI_CursBaseDialog):
    def askValue(self):
        showTitleMsg(self)

        curses.echo()
        curses.cbreak()
        curses.curs_set(1)
        self.win.keypad(False)
        self.win.addstr(9, 2, "──" * 15)

        if self.default:
            self.win.addstr(7, 2, f"default: {self.default}")
        value = self.win.getstr(8, 2, curses.A_BOLD).decode("UTF-8")

        if value == "":
            value = self.default
        return value


class UI_ProgressBarDialog(UI_CursBaseDialog):
    def __init__(self, **options):
        super(self.__class__, self).__init__(**options)
        self.clr1 = options.get("clr1", curses.A_NORMAL)
        self.clr2 = options.get("clr2", curses.A_NORMAL)
        self.maxValue = options.get("maxValue")
        self.blockValue = 0

        showTitleMsg(self)
        self.drawProgressBarBox()
        self.win.refresh()

    def drawProgressBarBox(self):
        from curses.textpad import rectangle as rect

        self.win.attrset(self.clr1 | curses.A_BOLD)
        hight, width = 2, 50
        y, x = 7, 3
        rect(self.win, y - 1, x - 1, hight + y, width + x)

    def progress(self, currentValue):
        percentcomplete = int((100 * currentValue / self.maxValue))
        blockValue = int(percentcomplete / 2)
        maxValue = str(self.maxValue)
        currentValue = str(currentValue)

        self.win.addstr(
            9,
            int(self.x / 2 - len(maxValue)) - 2,
            "%s of %s" % (currentValue, maxValue),
        )

        for i in range(self.blockValue, blockValue):
            self.win.addstr(7, i + 3, "▋", self.clr2 | curses.A_BOLD)
            self.win.addstr(8, i + 3, "▋", self.clr2 | curses.A_NORMAL)

        if percentcomplete == 100:
            self.win.addstr(10, int(self.x / 2) - 3, "Finish", curses.A_STANDOUT)
            self.win.getch()
        self.blockValue = blockValue
        self.win.refresh()


def UI_ShowMessageDialog(**options):
    return UI_showMessageDialog(**options).showMessage()


def UI_AskValueDialog(**options):
    return UI_askValueDialog(**options).askValue()


def UI_ValueDialog(**options):
    return UI_valueDialog(**options).ValueDialog()


def UI_AskFileSaveDialog(**options):
    return UI_askFileSaveDialog(**options).fileSave()


def UI_AskDialog(**options):
    return UI_askDialog(**options).askDialog()


def UI_progressBarDialog(**options):
    return UI_ProgressBarDialog(**options).progress


def rectangle(win, begin_y, begin_x, height, width, attr):
    win.vline(begin_y, begin_x, curses.ACS_VLINE, height, attr)
    win.hline(begin_y, begin_x, curses.ACS_HLINE, width, attr)
    win.hline(height + begin_y, begin_x, curses.ACS_HLINE, width, attr)
    win.vline(begin_y, begin_x + width, curses.ACS_VLINE, height, attr)
    win.addch(begin_y, begin_x, curses.ACS_ULCORNER, attr)
    win.addch(begin_y, begin_x + width, curses.ACS_URCORNER, attr)
    win.addch(height + begin_y, begin_x, curses.ACS_LLCORNER, attr)
    win.addch(begin_y + height, begin_x + width, curses.ACS_LRCORNER, attr)
    win.refresh()


def showTitleMsg(self):
    if self.title:
        self.title = f" {self.title} "
        self.win.addstr(
            1,
            int(self.x / 2 - len(self.title) / 2),
            self.title,
            curses.A_BOLD | curses.A_STANDOUT,
        )
    for i, msg in enumerate(self.message.split("\n")):
        self.win.addstr(i + 3, 2, msg, curses.A_BOLD)


def infoGenrator(value):
    line_1 = f"Product Name  : {value['Product']}"
    line_1 = line_1 + "ㅤ"*(44-len(line_1))
    line_2 = f"F/W version   : {value['fwChar']} (v{value['major']}.{value['minor']}.{value['revision']})"
    line_2 = line_2 + "ㅤ"*(44-len(line_2))
    line_3 = f"Patch Version : {value['patchVersion']}" 
    line_3 = line_3 + "ㅤ"*(44-len(line_3))
    line_4 = f"Serial No.    : {value['serialNum']}"
    line_4 = line_4 + "ㅤ"*(44-len(line_4))
    line_5 = f"Build No.     : {value['buildHex']}"
    line_5 = line_5 + "ㅤ"*(44-len(line_5))

    UI_CONNECTED = [
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ",
    f"              {value['QF_connectType']} ({value['QF_connValue1']}, {value['QF_connValue2']})  ",
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ",
    line_1,
    line_2,
    line_3,
    line_4,
    line_5,
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ",
    ]

    return UI_CONNECTED