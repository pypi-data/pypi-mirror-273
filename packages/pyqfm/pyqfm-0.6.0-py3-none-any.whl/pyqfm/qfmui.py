import time
import ctypes
import curses
import pyqfm
from . import uiprovider
#import uiprovider

module = pyqfm.Module()
DEMO_RELEASE_DATE = "2024/05/14"

class UI_main:
    def __init__(self):
        # Module Status Values init
        self.QF_connectType = None
        self.QF_connValue1 = None
        self.QF_connValue2 = None
        self.QF_connectStatus = False
        self.QF_freeScan = False
        self.QF_packetTrace = False
        self.QF_secureMode = False 
        self.QF_keyMenu = False

        # UI Status Values init
        self.UI_consoleMaxLine = 13
        self.UI_consoleLine = 1
        self.UI_currentRow = 0

        # UI (Curses) init
        self.stdscr = curses.initscr()
        self.stdscr.clear()
        self.stdscr.keypad(True)
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

        if curses.has_colors():
            curses.start_color()

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

        # First things first, make sure we have enough room!
        if curses.COLS <= 88 or curses.LINES <= 26:
            raise Exception ("This terminal window is too small")

        self.maxy, self.maxx = curses.LINES, curses.COLS

        self.UI_Logo = curses.newwin(0, 0, 0, 1)
        self.UI_SDKInfo = curses.newwin(0, 0, 6, 1)
        self.UI_Info = curses.newwin(0, 0, 8, 1)
        self.UI_Menu = curses.newwin(0, 0, 1, 45)
        self.UI_Console = curses.newwin(0, 0, 18, 1)


    def UI_addList(self, windowObj, charToPut, inAttr=0):
        lineCount = 0
        for line in charToPut:
            windowObj.addstr(lineCount, 0, charToPut[lineCount], inAttr)
            lineCount = 1 + lineCount
        windowObj.refresh()

    def UI_addLine(self, y, x, text):
        self.stdscr.addstr(y, x, text)
        self.stdscr.refresh()

    def UI_printConsole(self, msg):
        if self.UI_consoleMaxLine >= self.UI_consoleLine:
            uiprovider.consoleList[self.UI_consoleLine] = str(msg)+" "*(44-len(str(msg)))
            #UI_CONSOLE[current_line] = str(current_line)+" "+str(msg)+" "*(44-len(str(msg)))
            self.UI_consoleLine = self.UI_consoleLine + 1
        else:
            for i in range(1, self.UI_consoleMaxLine):
                uiprovider.consoleList[i] = uiprovider.consoleList[i + 1]
            uiprovider.consoleList[self.UI_consoleLine - 1] = str(msg)+" "*(44-len(str(msg)))
            #UI_CONSOLE[current_line] = str(current_line)+" "+str(msg)+" "*(44-len(str(msg)))

    def UI_infoRefresh(self):
        self.UI_addList(self.UI_Logo, uiprovider.logoList, curses.A_BOLD | curses.color_pair(1))
        #self.UI_Logo.refresh()
        self.UI_addList(
            self.UI_SDKInfo,
            [
                f"QFM SDK Version : {module.QF_GetSDKVersionString()}",
                f"Relese Date : {DEMO_RELEASE_DATE}",
            ],
            curses.A_BOLD | curses.color_pair(2),
        )
        #self.UI_SDKInfo.refresh()
        # Disconnect Info print
        if self.QF_connectStatus == False:
            self.UI_addList(self.UI_Info, uiprovider.disconnectList, curses.A_BOLD | curses.color_pair(2))
            self.UI_Info.refresh()
            self.UI_Menu.refresh()
        # Connected Info print
        elif self.QF_connectStatus == True:
            ret, major, miner, revision = module.QF_GetFirmwareVersion()
            ret, patchVersion = module.QF_GetPatchVersion()
            ret, serialNum = module.QF_GetSysParameter(pyqfm.QF_SYS_SERIAL_NUMBER)
            ret, fwVersion = module.QF_GetSysParameter(pyqfm.QF_SYS_FIRMWARE_VERSION)

            fwChar = chr(fwVersion >> 24 & 0xff)
            fwChar = fwChar + chr(fwVersion >> 16 & 0xff)
            fwChar = fwChar + chr(fwVersion >> 8 & 0xff)
            fwChar = fwChar + chr(fwVersion & 0xff)

            ret, buildNum = module.QF_GetSysParameter(pyqfm.QF_SYS_BUILD_NUMBER)
            buildHex = str(hex(buildNum))[2:10]

            QF_moduleValues = {"QF_connectType": self.QF_connectType, "QF_connValue1": self.QF_connValue1, "QF_connValue2": self.QF_connValue2,\
                                "Product": module.QF_GetModuleString2(), "fwChar": fwChar, "major": major, "minor":miner, "revision":revision,\
                                "patchVersion":patchVersion, "serialNum":serialNum, "buildHex":buildHex}
            
            UI_CONNECTED = uiprovider.infoGenrator(QF_moduleValues)

            self.UI_addList(self.UI_Info, UI_CONNECTED, curses.A_BOLD | curses.color_pair(2))
            self.UI_Info.addstr(1, 0, "[CONNECTED]", curses.A_BOLD | curses.color_pair(3))
            self.UI_Info.addstr(1, 12, "◉", curses.A_BLINK)
            self.UI_Info.addstr(9, 0, "[MONITOR]                                    ", curses.A_BOLD | curses.color_pair(1))
            
            self.UI_addList(self.UI_Console, uiprovider.consoleList, curses.A_BOLD | curses.color_pair(2))
            self.UI_Console.refresh()
            self.UI_Info.refresh()
            self.UI_Menu.refresh()

    def SendPacketCallback(self, arg):
        if self.QF_packetTrace:
            self.UI_printConsole(f"SEND:{ctypes.string_at(arg,pyqfm.QF_PACKET_LEN).hex().upper()}")

    def ReceivePacketCallback(self, arg):
        if self.QF_packetTrace:
            self.UI_printConsole(f"RECV:{ctypes.string_at(arg,pyqfm.QF_PACKET_LEN).hex().upper()}")

    def UserFeedbackDataCallback(self, feedbackData, userdata):
        if self.QF_freeScan:
            if feedbackData.fields & pyqfm.USER_FEEDBACK_TYPE_MESSAGE_CODE:
                feedback = feedbackData.messageCode
                if feedback == pyqfm.QF_USER_FEEDBACK_LOOK_AT_THE_CAMERA_CORRECTLY:
                    self.UI_printConsole("Look at the camera correctly")
                elif feedback == pyqfm.QF_USER_FEEDBACK_TURN_YOUR_HEAD_RIGHT:
                    # turn your head right
                    self.UI_printConsole("Turn your head right")
                elif feedback == pyqfm.QF_USER_FEEDBACK_TURN_YOUR_HEAD_LEFT:
                    # turn your head left
                    self.UI_printConsole("Turn your head left")
                elif feedback == pyqfm.QF_USER_FEEDBACK_TURN_YOUR_HEAD_UP:
                    # turn your head up
                    self.UI_printConsole("Turn your head up")
                elif feedback == pyqfm.QF_USER_FEEDBACK_TURN_YOUR_HEAD_DOWN:
                    # turn your head down
                    self.UI_printConsole("Turn your head down")
                elif feedback == pyqfm.QF_USER_FEEDBACK_MOVE_FORWARD:
                    # move forward
                    self.UI_printConsole("Move forward")
                elif feedback == pyqfm.QF_USER_FEEDBACK_MOVE_BACKWARD:
                    # move backward
                    self.UI_printConsole("Move backward")
                elif feedback == pyqfm.QF_USER_FEEDBACK_OUT_OF_ENROLLMENT_AREA:
                    # out of enrollment area
                    self.UI_printConsole("Out of enrollment area")
                elif feedback == pyqfm.QF_USER_FEEDBACK_FACE_NOT_DETECTED:
                    self.UI_printConsole("Face not detected")
            elif feedbackData.fields & pyqfm.USER_FEEDBACK_TYPE_HEAD_POSITION:
                self.UI_printConsole(f"{feedbackData.headPosition.topLeftX,feedbackData.headPosition.topLeftY, feedbackData.headPosition.bottomRightX,feedbackData.headPosition.bottomRightY}")

    def QF_freeScanEnable(self):
        module.QF_SetUserFeedbackDataCallback(self.UserFeedbackDataCallback)
        res = module.QF_InitSysParameter()
        res = module.QF_SetSysParameter(pyqfm.QF_SYS_FREESCAN_DELAY, 0x30)
        res = module.QF_SetSysParameter(pyqfm.QF_SYS_FREE_SCAN, 0x31)
        res = module.QF_SetSysParameter(pyqfm.QF_SYS_USER_FEEDBACK, 0x31)
        res, value = module.QF_GetSysParameter(pyqfm.QF_SYS_USER_FEEDBACK)

    def QF_freeScanDisable(self):
        res = module.QF_InitSysParameter()
        res = module.QF_SetSysParameter(pyqfm.QF_SYS_FREESCAN_DELAY, 0x30)
        res = module.QF_SetSysParameter(pyqfm.QF_SYS_FREE_SCAN, 0x31)
        res = module.QF_SetSysParameter(pyqfm.QF_SYS_USER_FEEDBACK, 0x31)
        res, value = module.QF_GetSysParameter(pyqfm.QF_SYS_USER_FEEDBACK)

    def QF_changeKey(self, option):
        MODULE_KEY_SIZE = 32

        currentKey = [0] * MODULE_KEY_SIZE
        newKey = [0] * MODULE_KEY_SIZE
        currentKeyinputString = [0] * (MODULE_KEY_SIZE)
        newKeyinputString = [0] * (MODULE_KEY_SIZE)
        optionString = ""

        if option == pyqfm.QF_KEY_OPTION_SET_ENCRYPTION_KEY:
            optionString = "encryption"
        
        elif option == pyqfm.QF_KEY_OPTION_SET_INITIALIZATION_VECTOR:
            optionString = "iv"

        elif option == pyqfm.QF_KEY_OPTION_SET_SECURE_KEY:
            optionString = "secure"

        elif option == pyqfm.QF_KEY_OPTION_SET_ENCRYPTION_KEY_WITH_VERIFICATION:
            optionString = "encryption"

        elif option == pyqfm.QF_KEY_OPTION_SET_INITIALIZATION_VECTOR_WITH_VERIFICATION:
            optionString = "iv"

        elif option == pyqfm.QF_KEY_OPTION_SET_SECURE_KEY_WITH_VERIFICATION:
            optionString = "secure"
        else:
            uiprovider.UI_ShowMessageDialog(title="Error", message=f"Invalid option", timeout=0)
            return
        

        if (option == pyqfm.QF_KEY_OPTION_SET_ENCRYPTION_KEY_WITH_VERIFICATION) or \
            (option == pyqfm.QF_KEY_OPTION_SET_INITIALIZATION_VECTOR_WITH_VERIFICATION) or \
            (option == pyqfm.QF_KEY_OPTION_SET_SECURE_KEY_WITH_VERIFICATION):
            _userInput = uiprovider.UI_AskValueDialog(
                title="Current key", message=f"Please enter the current {optionString} key up to 32 bytes\nstring\nIf you want to use the default key, press enter\nkey only.", timeout=0, default=""
            )
            try:
                userInput = _userInput
                userInput = userInput.encode('utf-8').hex()
                currentKeyinputString[:len(userInput)] = map(int, userInput)
            except ValueError as e:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"invaild key", timeout=0)
                return

            if len(currentKeyinputString) > 32:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"invaild key length", timeout=0)
                return
            
            if len(currentKeyinputString) > 0:
                currentKeylength = min(len(currentKey), len(currentKeyinputString))
                currentKey[:currentKeylength] = currentKeyinputString[:currentKeylength]

            uiprovider.UI_ShowMessageDialog(title="Change Key", message=f"currentKey {optionString} key (String) : {_userInput}\ncurrentKey {optionString} key (HEX) : \n{''.join(map(str, currentKey))}", timeout=0)

        if option == pyqfm.QF_KEY_OPTION_SET_INITIALIZATION_VECTOR_WITH_VERIFICATION:
            uiprovider.UI_ShowMessageDialog(title="Change Key", message=f"First 16 bytes of the new key will be used as {optionString} key\nLast 16bytes will not be used.\nIt is the dummy data for fixed length format\nof protocol structure", timeout=0)
        
        _userInput = uiprovider.UI_AskValueDialog(
            title="NeW key", message=f"Please enter the new {optionString} key up to 32 bytes \nstring\nIf you want to use the default key, press enter\nkey only.", timeout=0, default=""
        )
        try:
            userInput = _userInput
            userInput = userInput.encode('utf-8').hex()
            newKeyinputString[:len(userInput)] = map(int, userInput)
        except ValueError as e:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"invaild key", timeout=0)
                return
        
        if len(newKeyinputString) > MODULE_KEY_SIZE:
            uiprovider.UI_ShowMessageDialog(title="Error", message=f"invaild key length", timeout=0)
            return
        
        if len(newKeyinputString) > 0:
            newKeyLength = min(len(newKey), len(newKeyinputString))
            newKey[:newKeyLength] = newKeyinputString[:newKeyLength]
        else:
            newKey[0] = 1
            uiprovider.UI_ShowMessageDialog(title="Error", message=f"Key is not set. So the default key is used.", timeout=0)

        uiprovider.UI_ShowMessageDialog(title="Change Key", message=f"new {optionString} key (String) : {_userInput}\nnew {optionString} key (HEX) : \n{''.join(map(str, newKey))}", timeout=0)

        result = uiprovider.UI_AskDialog(
            title="WARNING",
            message=f"If you lose the new {optionString} key, \nyou can not use the module anymore.\nPlease keep the new {optionString} key safely.\nDo you read the warning?",
            ask_left="No",
            ask_right="Yes",
            title_attr=curses.A_STANDOUT | curses.A_BOLD,
        )
        if result == "Yes":
            pass
        else:
            return

        result = uiprovider.UI_AskDialog(
            title="Change Key",
            message=f"Do you want to change the {optionString} key?",
            ask_left="No",
            ask_right="Yes",
            title_attr=curses.A_STANDOUT | curses.A_BOLD,
        )
        if result == "Yes":
            ret = module.QF_ChangeKey(option, currentKey, newKey)
            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Change key", message=f"{optionString} key is changed successfully.")
                self.UI_printConsole(f"[Change Key] {optionString} Change.")
            else:    
                self.UI_printConsole(f"[Change Key] Error: {ret}")
        else:
            return
    
    def QF_resetKey(self, option):

        optionString = ""

        if option == pyqfm.QF_KEY_OPTION_RESET_ENCRYPTION_KEY:
            optionString = "encryption"
        elif option == pyqfm.QF_KEY_OPTION_RESET_INITIALIZATION_VECTOR:
            optionString = "iv"
        elif option == pyqfm.QF_KEY_OPTION_RESET_SECURE_KEY:
            optionString = "secure"
        else:
            print("Invalid option")
            return

        result = uiprovider.UI_AskDialog(
            title="Reset Key",
            message=f"Do you want to change the {optionString} key?",
            ask_left="No",
            ask_right="Yes",
            title_attr=curses.A_STANDOUT | curses.A_BOLD,
        )
        if result == "Yes":
            ret = module.QF_ResetKey(option)
            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Reset Key", message=f"{optionString} key is reset successfully.")
                self.UI_printConsole(f"[Reset Key] {optionString} reset.")
            else:    
                self.UI_printConsole(f"[Reset Key] Error: {ret}")
        else:
            return

    def QF_VerifyKey(self, option):
        
        MODULE_KEY_SIZE = 32
        optionString = ""
        currentKey = [0] * MODULE_KEY_SIZE
        currentKeyinputString = [0] * (MODULE_KEY_SIZE)

        if option == pyqfm.QF_KEY_OPTION_VERIFY_ENCRYPTION_KEY:
            optionString = "encryption"
        elif option == pyqfm.QF_KEY_OPTION_VERIFY_INITIALIZATION_VECTOR:
            optionString = "iv"
        else:
            print("Invalid option")
            return

        if (option == pyqfm.QF_KEY_OPTION_VERIFY_ENCRYPTION_KEY) or \
            (option == pyqfm.QF_KEY_OPTION_VERIFY_INITIALIZATION_VECTOR):
            _userInput = uiprovider.UI_AskValueDialog(
                title="Verify key", message=f"Please enter the current {optionString} key up to 32 bytes\nstring\nfor verification", timeout=0, default=""
            )
            try:
                userInput = _userInput
                userInput = userInput.encode('utf-8').hex()
                currentKeyinputString[:len(userInput)] = map(int, userInput)
            except ValueError as e:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"invaild key", timeout=0)
                return

            if len(currentKeyinputString) > 32:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"invaild key length", timeout=0)
                return
            
            if len(currentKeyinputString) > 0:
                currentKeylength = min(len(currentKey), len(currentKeyinputString))
                currentKey[:currentKeylength] = currentKeyinputString[:currentKeylength]

            uiprovider.UI_ShowMessageDialog(title="Verify Key", message=f"currentKey {optionString} key (String) : {_userInput}\ncurrentKey {optionString} key (HEX) : \n{''.join(map(str, currentKey))}", timeout=0)

            ret = module.QF_VerifyKey(option, currentKey)

            print(ret)

            if (ret != pyqfm.QF_RET_SUCCESS):
                uiprovider.UI_ShowMessageDialog(title="Verify Key", message=f"{optionString} Failed to verify key.")
                self.UI_printConsole(f"[Verify Key] {optionString} Failed.")
            else:
                uiprovider.UI_ShowMessageDialog(title="Verify Key", message=f"{optionString} key is verified.")
                self.UI_printConsole(f"[Verify Key] {optionString} Verified.")

        return

    def run(self):
        self.stdscr.refresh()
        while True:
            try:
                currentMenu = None
                if not self.QF_keyMenu:
                    currentMenu = uiprovider.menuList
                else:
                    currentMenu = uiprovider.keyList

                for i, row in enumerate(currentMenu):
                    x = 0
                    y = i
                    if i == self.UI_currentRow:
                        self.UI_Menu.attron(curses.A_REVERSE)
                        self.UI_Menu.addstr(y, x, row)
                        self.UI_Menu.attroff(curses.A_REVERSE)
                    else:
                        self.UI_Menu.addstr(y, x, row)

                self.UI_infoRefresh()

                key = self.stdscr.getch()

                if key == curses.KEY_UP and self.UI_currentRow > 0:
                    if "-" in currentMenu[self.UI_currentRow - 1]:
                        self.UI_currentRow -= 2
                    else:
                        self.UI_currentRow -= 1
                    self.UI_Menu.refresh()
                elif key == curses.KEY_DOWN and self.UI_currentRow < len(currentMenu) - 1:
                    if "-" in currentMenu[self.UI_currentRow + 1]:
                        self.UI_currentRow += 2
                    else:
                        self.UI_currentRow += 1
                    self.UI_Menu.refresh()
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if self.UI_currentRow == len(currentMenu) - 1:
                        if currentMenu == uiprovider.menuList:
                            self.UI_Menu.clear()
                            curses.endwin()
                            break
                        else:
                            currentMenu = uiprovider.menuList
                            self.UI_currentRow = 0
                            self.QF_keyMenu = False
                    else:
                        self.UI_Menu.clear()
                        self.UI_menuSelect(currentMenu[self.UI_currentRow])
                        self.UI_infoRefresh()

                while self.QF_freeScan == True:
                    res, packet = module.QF_ReceivePacket(1000) # BYTE *packet, int timeout

                    if module.QF_GetPacketValue(pyqfm.QF_PACKET_COMMAND, packet) == pyqfm.QF_COM_IS and \
                    module.QF_GetPacketValue(pyqfm.QF_PACKET_FLAG, packet) == pyqfm.QF_PROTO_RET_SUCCESS:
                        userID = module.QF_GetPacketValue(pyqfm.QF_PACKET_PARAM, packet)
                        subID = module.QF_GetPacketValue(pyqfm.QF_PACKET_SIZE, packet)
                        
                        self.UI_printConsole(f"User ID : {userID}, Sub ID : {subID}")
                    elif module.QF_GetPacketValue(pyqfm.QF_PACKET_COMMAND, packet) == pyqfm.QF_COM_IS and \
                    module.QF_GetPacketValue(pyqfm.QF_PACKET_FLAG, packet) == pyqfm.QF_PROTO_RET_TIMEOUT_MATCH:
                        self.UI_printConsole("matching timeout")
                        
                        time.sleep(2)

                    self.stdscr.nodelay(True)

                    if ord('q') == self.stdscr.getch():
                        self.QF_freeScanDisable()
                        self.QF_freeScan = False
                        self.UI_printConsole(f"[Free Scan] Disable.")
                        self.stdscr.nodelay(False)
                        break
                    self.UI_infoRefresh()
                    time.sleep(0.1)
            except Exception as err:
                caughtExceptions = str(err)
                if "" != caughtExceptions:
                    self.stdscr.clear()
                    curses.endwin()
                    return 0

    def UI_menuSelect(self, row):
        # Communication Setup
        if "Communication Setup" not in row and self.QF_connectStatus == False:
            uiprovider.UI_ShowMessageDialog(title="Warning!", message="Connection First", timeout=0)
        elif "Communication Setup" in row and self.QF_connectStatus == False:
            result = uiprovider.UI_AskDialog(
                title="Communication Setup",
                message="Select Communication Type",
                ask_left="Socket",
                ask_right="UART",
                title_attr=curses.A_STANDOUT | curses.A_BOLD,
            )
            # Communication Setup (Socket)
            if result == "Socket":
                socketIp = uiprovider.UI_AskValueDialog(
                    title="Socket IP", message="input ip", timeout=0, default="172.16.110.6"
                )
                socketPort = uiprovider.UI_AskValueDialog(
                    title="Socket Port", message=f"input port", timeout=0, default="12120"
                )
                uiprovider.UI_ShowMessageDialog(title="Socket", message="Connecting...", timeout=0.1)
                if module.QF_InitSocket(socketIp, socketPort) == 0:
                    self.QF_connectStatus = True
                    self.QF_connectType = "Socket"
                    self.QF_connValue1 = socketIp
                    self.QF_connValue2 = socketPort
                else:
                    uiprovider.UI_ShowMessageDialog(title="Socket", message="bad...", timeout=0)
            # Communication Setup (UART)
            elif result == "UART":
                uart_port = uiprovider.UI_AskValueDialog(
                    title="UART Port",
                    message="input Port",
                    timeout=0,
                    default="/dev/ttyUSB0",
                )
                uart_baudrate = uiprovider.UI_AskValueDialog(
                    title="UART Baudrate",
                    message=f"input Baudrate",
                    timeout=0,
                    default="115200",
                )
                uiprovider.UI_ShowMessageDialog(title="UART", message="Connecting...", timeout=0.1)
                if module.QF_InitCommPort(uart_port, uart_baudrate) == 0:
                    self.QF_connectStatus = True
                    self.QF_connectType = "UART"
                    self.QF_connValue1 = uart_port
                    self.QF_connValue2 = uart_baudrate
                else:
                    uiprovider.UI_ShowMessageDialog(title="UART", message="bad...", timeout=0)
        # Already Connected, bypass
        elif "Communication Setup" in row and self.QF_connectStatus == True:
            return 0
        elif "System Configuration" in row and self.QF_connectStatus == True:
            paramName = uiprovider.UI_ValueDialog(
                title="System Parameter Setting",
                message="Select Edit Parameter\n│  If no value is entered, it will be canceled.",
                values= uiprovider.paramList,
                title_attr=curses.A_STANDOUT | curses.A_BOLD,
            )
            parameter = getattr(pyqfm, paramName)
            ret, currentValue = module.QF_GetSysParameter(parameter)
            try:
                value = uiprovider.UI_AskValueDialog(
                    title="Edit Param", message=f"param: {paramName}\n\ncurrent value: {currentValue} \nnew value:", timeout=0, default="")
                if value == "":
                    return
                ret = module.QF_SetSysParameter(parameter, int(value))
            except ValueError as e:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"invaild Value", timeout=0)
                    return
            if ret == 0:
                self.UI_printConsole(f"[System Configuration] Update parameter")

                result = uiprovider.UI_AskDialog(
                    title="System Configuration",
                    message="Save parameter?",
                    ask_left="No",
                    ask_right="Yes",
                    title_attr=curses.A_STANDOUT | curses.A_BOLD,
                )
                if result == "Yes":
                    ret = module.QF_Save()
                    if ret == 0:
                        self.UI_printConsole(f"[System Configuration] Save parameter")
                    else:
                        self.UI_printConsole(f"[System Configuration] Error: {ret}")
                else:
                    return
            else:
                self.UI_printConsole(f"[System Configuration] Err: {ret}")
        # Reset System Parameter
        elif "Reset System Parameter" in row and self.QF_connectStatus == True:
            ret = module.QF_ResetSystemParameter()
            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Reset System Parameter", message="Done")
                self.UI_printConsole(f"[System Configuration] Done.")
            else:
                uiprovider.UI_ShowMessageDialog(title="Reset System Parameter", message="Err: {ret}")
                self.UI_printConsole(f"[System Configuration] Error: {ret}")
        # Enroll by scan
        elif "Enroll by scan" in row and self.QF_connectStatus == True:
            #uiprovider.UI_ShowMessageDialog(title="Enroll by scan", message="Enroll..", )
            ret, enrollID, imageQuality = module.QF_Enroll(0, pyqfm.QF_ENROLL_OPTION_ADD_NEW)
            if ret == 0:
                #uiprovider.UI_ShowMessageDialog(title="Enroll by scan", message=f"ID: {enrollID} imageQuality: {imageQuality}", timeout=0)
                self.UI_printConsole(f"[Enroll by scan] ID: {enrollID} imageQuality: {imageQuality}")
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Enroll by scan] Error: {ret}")
        # Identify by scan
        elif "Identify by scan" in row and self.QF_connectStatus == True:
            #uiprovider.UI_ShowMessageDialog(title="Identify by scan", message="Identify..")
            ret, userID, subID = module.QF_Identify()
            if ret == 0:
                #uiprovider.UI_ShowMessageDialog(title="Identify by scan", message=f"ID: {userID} subID: {subID}", timeout=0)
                self.UI_printConsole(f"[Identify by scan] ID: {userID} subID: {subID}")
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Identify by scan] Error: {ret}")
        # Verify by scan
        elif "Verify by scan" in row and self.QF_connectStatus == True:
            userID = uiprovider.UI_AskValueDialog(
                title="Verify by scan", message="userID", timeout=0, default=""
            )
            if userID:
                ret, subID = module.QF_Verify(int(userID))
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"Required userID", timeout=0)
                return 0

            if ret == 0:
                self.UI_printConsole(f"[Verify by scan] ID: {userID} subID: {subID}")
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Identify by scan] Error: {ret}")
        # Delete template
        elif "Delete template" in row and self.QF_connectStatus == True:
            userID = uiprovider.UI_AskValueDialog(
                title="Delete template", message="userID", timeout=0, default=""
            )
            subID = uiprovider.UI_AskValueDialog(
                title="Delete template", message="subID", timeout=0, default=""
            )
            if userID and subID:
                uiprovider.UI_ShowMessageDialog(title="Delete template", message="Deleting...", timeout=0.1)
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"Required ID", timeout=0)
                return 0
            
            ret = module.QF_DeleteOneTemplate(int(userID), int(subID))

            if  ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Delete template", message="Done.")
                self.UI_printConsole(f"[Delete template] Done.")
            else:    
                self.UI_printConsole(f"[Delete template] Error: {ret}")
        # Delete all templates
        elif "Delete all templates" in row and self.QF_connectStatus == True:
            result = uiprovider.UI_AskDialog(
                title="Delete all templates",
                message="are you happy?",
                ask_left="No",
                ask_right="Yes",
                title_attr=curses.A_STANDOUT | curses.A_BOLD,
            )
            if result == "Yes":
                ret = module.QF_DeleteAll()
                if ret == 0:
                    uiprovider.UI_ShowMessageDialog(title="Delete all templates", message="Done.")
                    self.UI_printConsole(f"[Delete all template] Done.")
                else:    
                    self.UI_printConsole(f"[Delete all template] Error: {ret}")
            else:
                return
        # Get all user informations
        elif "Get all user informations" in row and self.QF_connectStatus == True:
            uiprovider.UI_ShowMessageDialog(title="Get all user informations", message="wait...", timeout=0.1)
            ret, userInfo, numOfUser, numOfTemplate = module.QF_GetAllUserInfo()

            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Get all user informations", message="Done.")
                self.UI_printConsole(f"[Get all user informations] {numOfUser, numOfTemplate}")
                textbuf = ""
                for i in range(len(userInfo)):
                    if 31 >= len(textbuf):
                        textbuf = textbuf + f"{userInfo[i].userID, userInfo[i].numOfTemplate}"
                    else:
                        textbuf = textbuf + f"{userInfo[i].userID, userInfo[i].numOfTemplate}"
                        self.UI_printConsole(textbuf)
                        textbuf = ""
                if not textbuf == "":
                    self.UI_printConsole(textbuf)
            else:    
                self.UI_printConsole(f"[Get all user informations] Error: {ret}")
        # Read all templates
        elif "Read all templates" in row and self.QF_connectStatus == True:
            userID = uiprovider.UI_AskValueDialog(
                title="Delete template", message="userID", timeout=0, default=""
            )
            if userID:
                uiprovider.UI_ShowMessageDialog(title="Read all templates", message="Wait..", )
                ret, numOfTemplate, templateData = module.QF_ReadTemplate(int(userID))
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"Required userID", timeout=0)
                return 0

            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Read all templates", message="Done.")
                self.UI_printConsole(f"[Read all templates] userID:{userID} template:{numOfTemplate}")
                #for i in range(numOfTemplate):
                #        self.UI_printConsole(templateData)
            else:    
                self.UI_printConsole(f"[Get all user informations] Error: {ret}")
        # Enroll by template
        elif "Enroll by template" in row and self.QF_connectStatus == True:
            userID = uiprovider.UI_AskValueDialog(
                title="Enroll by template", message="userID", timeout=0, default=""
            )
            template = uiprovider.UI_AskValueDialog(
                title="Enroll by template", message="template path", timeout=0, default="1.dat"
            )
            if userID and template:
                #uiprovider.UI_ShowMessageDialog(title="Enroll by template", message="Template Reading..", )
                try:
                    with open(template, mode='rb') as file:
                        templateData = file.read()
                except FileNotFoundError:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: File '{template}' not found.", timeout=0)
                    return
                except PermissionError:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: Permission denied for file '{template}.", timeout=0)
                    return
                except Exception as e:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: An unexpected error occurred - {e}.", timeout=0)
                    return
                time.sleep(0.1)
                ret, enrollID = module.QF_EnrollTemplate(int(userID), pyqfm.QF_ENROLL_OPTION_ADD_NEW, len(templateData), templateData)
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"Required userID and templatePath", timeout=0)
                return 0
            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Enroll by template", message=f"ID: {enrollID}", timeout=0)
                self.UI_printConsole(f"[Enroll by template] ID: {enrollID}")
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Enroll by template] Error: {ret}")
        # Identify by template
        elif "Identify by template" in row and self.QF_connectStatus == True:
            template = uiprovider.UI_AskValueDialog(
                title="Identify by template", message="template path", timeout=0, default="1.dat"
            )
            if template:
                #uiprovider.UI_ShowMessageDialog(title="Identify by template", message="Template Reading..", )
                try:
                    with open(template, mode='rb') as file:
                        templateData = file.read()
                except FileNotFoundError:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: File '{template}' not found.", timeout=0)
                    return
                except PermissionError:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: Permission denied for file '{template}.", timeout=0)
                    return
                except Exception as e:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: An unexpected error occurred - {e}.", timeout=0)
                    return
                time.sleep(0.1)
            ret, userID, subID = module.QF_IdentifyTemplate(len(templateData), templateData)
            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Identify by template", message=f"ID: {userID} subID: {subID}", timeout=0)
                self.UI_printConsole(f"[Identify by template] ID: {userID} subID: {subID}")
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Identify by template] Error: {ret}")
        # Scan Template
        elif "Scan Template" in row and self.QF_connectStatus == True:
            template = uiprovider.UI_AskValueDialog(
                title="Scan Template", message="save template path", timeout=0, default="1.dat"
            )
            uiprovider.UI_ShowMessageDialog(title="Scan Template", message="Saving Template..")
            ret, templateData, templateSize, imageQuality = module.QF_ScanTemplate()
            if ret == 0:
                try:
                    with open(template, mode='wb') as file:
                        file.write(templateData)
                except FileNotFoundError:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: File '{template}' not found.", timeout=0)
                    return
                except PermissionError:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: Permission denied for file '{template}.", timeout=0)
                    return
                except Exception as e:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: An unexpected error occurred - {e}.", timeout=0)
                    return
                time.sleep(0.1)
                uiprovider.UI_ShowMessageDialog(title="Scan Template", message=f"Size: {templateSize} imageQuality: {imageQuality}", timeout=0)
                self.UI_printConsole(f"[Scan Template] Size: {templateSize} imageQuality: {imageQuality}")
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Scan Template] Error: {ret}")    
        # Enroll by template
        elif "Enroll by image" in row and self.QF_connectStatus == True:
            userID = uiprovider.UI_AskValueDialog(
                title="Enroll by image", message="userID", timeout=0, default=""
            )
            path = uiprovider.UI_AskValueDialog(
                title="Enroll by image", message="image path", timeout=0, default="qfm_scan.jpg"
            )
            if userID and path:
                uiprovider.UI_ShowMessageDialog(title="Enroll by image", message="Image Reading..", )
                try:
                    with open(path, mode='rb') as file:
                        imageData = file.read()
                except FileNotFoundError:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: File '{path}' not found.", timeout=0)
                    return
                except PermissionError:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: Permission denied for file '{path}.", timeout=0)
                    return
                except Exception as e:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: An unexpected error occurred - {e}.", timeout=0)
                    return
                time.sleep(0.1)
                ret, enrollID, imageQuality = module.QF_EnrollImage(int(userID), pyqfm.QF_ENROLL_OPTION_ADD_NEW, len(imageData), imageData)
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"Required userID and imagePath", timeout=0)
                return 0
            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Enroll by image", message=f"ID: {enrollID} imageQuality: {imageQuality}", timeout=0)
                self.UI_printConsole(f"[Enroll by scan] ID: {enrollID} imageQuality: {imageQuality}")
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Enroll by image] Error: {ret}")
        # Identify by template
        elif "Identify by image" in row and self.QF_connectStatus == True:
            path = uiprovider.UI_AskValueDialog(
                title="Identify by image", message="image path", timeout=0, default="qfm_scan.jpg"
            )
            if path:
                uiprovider.UI_ShowMessageDialog(title="Identify by image", message="Image reading...", )
                try:
                    with open(path, mode='rb') as file:
                        imageData = file.read()
                except FileNotFoundError:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: File '{path}' not found.", timeout=0)
                    return
                except PermissionError:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: Permission denied for file '{path}.", timeout=0)
                    return
                except Exception as e:
                    uiprovider.UI_ShowMessageDialog(title="Error", message=f"Error: An unexpected error occurred - {e}.", timeout=0)
                    return
            ret, userID, subID = module.QF_IdentifyImage(len(imageData), imageData)
            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Identify by image", message=f"ID: {userID} subID: {subID}", timeout=0)
                self.UI_printConsole(f"[Identify by image] ID: {userID} subID: {subID}")
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Identify by image] Error: {ret}")
        # Scan Template
        elif "Scan image" in row and self.QF_connectStatus == True:
            path = uiprovider.UI_AskValueDialog(
                title="Scan image", message="save image path", timeout=0, default="qfm_scan.jpg"
            )
            uiprovider.UI_ShowMessageDialog(title="Scan image", message="Saving...")
            ret, image = module.QF_ScanImage()
            ret, image = module.QF_SaveImage(path, image)

            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Scan image", message=f"Done.", timeout=0.1)
                self.UI_printConsole(f"[Scan image] Done.")
                ret = module.QF_ReleaseImage(image)
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Scan image] Error: {ret}")    
        # Upgrade firmware
        elif "Upgrade firmware" in row and self.QF_connectStatus == True:
            path = uiprovider.UI_AskValueDialog(
                title="Upgrade firmware", message="Firmware path", timeout=0, default="FW_QFM_PRO_P05A_44143af9_23112906.bin"
            )
            
            uiprovider.UI_ShowMessageDialog(title="Upgrade firmware", message="Upgrading firmware...")
            ret = module.QF_Upgrade(path, 4096 * 4)

            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Upgrade firmware", message=f"Done.\nRequired re-Communication Setup.", timeout=0.1)
                self.UI_printConsole(f"[Upgrade firmware] Done.\nRequired re-Communication Setup.")
                self.QF_connectStatus = False
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Upgrade firmware] Error: {ret}")   
        # Upgrade Patch
        elif "Update Patch" in row and self.QF_connectStatus == True:
            path = uiprovider.UI_AskValueDialog(
                title="Update Patch", message="Patch path", timeout=0, default="PATCH_8_342dc0af.bin"
            )
            uiprovider.UI_ShowMessageDialog(title="Update Patch", message="Upgrading patch...")
            ret = module.QF_UpdatePatch("PATCH_8_342dc0af.bin", 4096 * 4)

            if ret == 0:
                uiprovider.UI_ShowMessageDialog(title="Update Patch", message=f"Done.\nRequired re-Communication Setup.", timeout=0.1)
                self.UI_printConsole(f"[Update Patch] Done.\nRequired re-Communication Setup.")
                self.QF_connectStatus = False
            else:
                uiprovider.UI_ShowMessageDialog(title="Error", message=f"code: {ret}", timeout=0)
                self.UI_printConsole(f"[Update Patch] Error: {ret}")   
        # DFU Mode
        elif "DFU Mode" in row and self.QF_connectStatus == True:
            result = uiprovider.UI_AskDialog(
                title="DFU Mode",
                message="are you happy?",
                ask_left="No",
                ask_right="Yes",
                title_attr=curses.A_STANDOUT | curses.A_BOLD,
            )
            if result == "Yes":
                ret = module.QF_EnterDFUMode()
                if ret == 0:
                    self.UI_printConsole(f"[DFU Mode] Enter DFU Mode.")
                else:
                    self.UI_printConsole(f"[DFU Mode] Error: {ret}")
            else:
                return
        # Free Scan
        elif "Free Scan" in row and self.QF_connectStatus == True:
            if not self.QF_freeScan:
                uiprovider.UI_ShowMessageDialog(title="Free Scan", message="Free Scan Enable\n\nIf you wish to exit, please press 'q'", timeout=0.3)
                self.QF_freeScanEnable()
                self.UI_printConsole(f"[Free Scan] Enable. (Exit 'q')")   
                self.QF_freeScan = True
        # Read QR Code
        elif "Read QR Code" in row and self.QF_connectStatus == True:
            uiprovider.UI_ShowMessageDialog(title="Read QR Code", message="Ready Scan...", timeout=0.3)
            ret, string, length = module.QF_ReadQRCode()
            if ret == 0:
                self.UI_printConsole(f"[Read QR Code] Result length: {length}")
                self.UI_printConsole(string.decode('UTF-8')) 
            else:
                self.UI_printConsole(f"[Read QR Code] Error: {ret}")   
        # Change Key
        elif "Change Key" in row and self.QF_connectStatus == True:
            if not self.QF_keyMenu:
                self.QF_keyMenu = True
                self.UI_currentRow = 0
        # Secure Packet Protocol
        elif "Secure Packet Protocol" in row and self.QF_connectStatus == True:
            if not self.QF_secureMode:
                uiprovider.UI_ShowMessageDialog(title="Secure Packet Protocol", message="Enable", timeout=0.3)
                ret = module.QF_SetSecurePacketProtocolMode(1, None)
                if ret:
                    self.UI_printConsole(f"[Secure Packet Protocol] Enable")
                    self.QF_secureMode = True
                else:
                    self.UI_printConsole(f"[Secure Packet Protocol] Err: {ret}")
            else:
                uiprovider.UI_ShowMessageDialog(title="Secure Packet Protocol", message="Disable", timeout=0.3)
                ret = module.QF_SetSecurePacketProtocolMode(0, None)
                if ret:
                    self.UI_printConsole(f"[Secure Packet Protocol] Disable")
                    self.QF_secureMode = False  
                else:
                    self.UI_printConsole(f"[Secure Packet Protocol] Err: {ret}")
        # Packet Trace
        elif "Packet Trace" in row and self.QF_connectStatus == True:
            if not self.QF_packetTrace:
                uiprovider.UI_ShowMessageDialog(title="Packet Trace", message="Packet Trace Enable")
                module.QF_SetSendPacketCallback(self.SendPacketCallback)
                module.QF_SetReceivePacketCallback(self.ReceivePacketCallback)
                self.UI_printConsole(f"[Packet Trace] Enable.")   
                self.QF_packetTrace = True
            else:
                self.UI_printConsole(f"[Packet Trace] Disable.")   
                self.QF_packetTrace = False
        # Database Management
        elif "Database Management" in row and self.QF_connectStatus == True:
            result = uiprovider.UI_AskDialog(
                title="Database Management",
                message="Chosses Database",
                ask_left="Load",
                ask_right="Save",
                title_attr=curses.A_STANDOUT | curses.A_BOLD,
            )
            if result == "Load":
                path = uiprovider.UI_AskValueDialog(
                    title="Database Load", message="Database path", timeout=0, default="qfm.db"
                )
                uiprovider.UI_ShowMessageDialog(title="Update Patch", message="Loading data...", timeout=0.1)
                ret = module.QF_LoadDB(path)
                if ret == 0:
                    self.UI_printConsole(f"[Database] Loaded.")
                else:
                    self.UI_printConsole(f"[Database] Error: {ret}")
            elif result == "Save":
                path = uiprovider.UI_AskValueDialog(
                    title="Database Save", message="Database path", timeout=0, default="qfm.db"
                )
                uiprovider.UI_ShowMessageDialog(title="Database Save", message="Saving data...", timeout=0.1)
                ret = module.QF_SaveDB(path)
                if ret == 0:
                    self.UI_printConsole(f"[Database] Saved.")
                else:
                    self.UI_printConsole(f"[Database] Error: {ret}")
        # keyList Menu
        elif "1. Encryption Key" in row and self.QF_connectStatus == True:
            self.QF_changeKey(pyqfm.QF_KEY_OPTION_SET_ENCRYPTION_KEY)

        elif "2. IV Key" in row and self.QF_connectStatus == True:
            self.QF_changeKey(pyqfm.QF_KEY_OPTION_SET_INITIALIZATION_VECTOR)
        
        elif "3. Secure Key" in row and self.QF_connectStatus == True:
            self.QF_changeKey(pyqfm.QF_KEY_OPTION_SET_SECURE_KEY)
        
        elif "4. Encryption Key with verification" in row and self.QF_connectStatus == True:
            self.QF_changeKey(pyqfm.QF_KEY_OPTION_SET_ENCRYPTION_KEY_WITH_VERIFICATION)
        
        elif "5. IV Key with verification" in row and self.QF_connectStatus == True:
            self.QF_changeKey(pyqfm.QF_KEY_OPTION_SET_INITIALIZATION_VECTOR_WITH_VERIFICATION)
        
        elif "6. Secure Key with verification" in row and self.QF_connectStatus == True:
            self.QF_changeKey(pyqfm.QF_KEY_OPTION_SET_SECURE_KEY_WITH_VERIFICATION)
        
        elif "7. Reset Encryption Key" in row and self.QF_connectStatus == True:
            self.QF_resetKey(pyqfm.QF_KEY_OPTION_RESET_ENCRYPTION_KEY)
        
        elif "8. Reset IV Key" in row and self.QF_connectStatus == True:
            self.QF_resetKey(pyqfm.QF_KEY_OPTION_RESET_INITIALIZATION_VECTOR)
        
        elif "9. Reset Secure Key" in row and self.QF_connectStatus == True:
            self.QF_resetKey(pyqfm.QF_KEY_OPTION_RESET_SECURE_KEY)
        
        elif "10. Verify Encryption Key" in row and self.QF_connectStatus == True:
            self.QF_VerifyKey(pyqfm.QF_KEY_OPTION_VERIFY_ENCRYPTION_KEY)

        elif "11. Verify IV Key" in row and self.QF_connectStatus == True:
            self.QF_VerifyKey(pyqfm.QF_KEY_OPTION_VERIFY_INITIALIZATION_VECTOR)

def main():
    _main = UI_main()
    _main.run()   

if __name__ == "__main__":
    main = UI_main()
    main.run()