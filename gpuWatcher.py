import time
import curses
from pynvml import *
import random

def initCurses(areaH: int, areaW: int):
    '''
        Description:
            Initlize a window to edit.
        Args:
            areaH -> int: The height of window.
            areaW -> int: The width of window.
        Return -> cureses window:
            Return a window.
    '''
    curses.initscr()
    stdscr = curses.newwin(areaH, areaW, 0, 0)
    stdscr.clear()
    stdscr.refresh()
    # 如何要用带颜色的字就必须调这个方法
    curses.start_color()
    curses.use_default_colors()
    # 设置颜色对，其实就是前景色和背景色
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_BLUE, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_RED, -1)
    curses.init_pair(6, curses.COLOR_WHITE, -1)
    return stdscr

def getDeviceInfo() -> list:
    '''
        Description:
            Get the gpu id.
        Args:

        Return -> list:
            Return the list contained gpus' id.
    '''
    nvmlInit()
    info = []
    deviceCount = nvmlDeviceGetCount()
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        info.append(["GPU" + str(i) + ":", nvmlDeviceGetName(handle)])
    nvmlShutdown()
    return info

def getDeviceTemp() -> list:
    '''
        Description:
            Get the temp of every gpu.
        Args:

        Return -> list:
            Return the temp of every gpu.
    '''
    nvmlInit()
    deviceCount = nvmlDeviceGetCount()
    tempInfo = []
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        temp = nvmlDeviceGetTemperature(handle,0)
        tempInfo.append("GPU:" + str(i) + "(" + str(temp) + "C)")
    nvmlShutdown()
    return tempInfo

def getDeviceMemOccupy():
    '''
        Description:
            Get the memory occupied percentage.
        Args:

        Return -> intPercentage(0-10), floatPercentage(0-10.0):
            Return the percentage of memory occupied.
            The first return value is int type.
            The Second return value is float type.
    '''
    nvmlInit()
    deviceCount = nvmlDeviceGetCount()
    memOccupyInt = []
    memOccupyFloat = []
    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        used = int(nvmlDeviceGetMemoryInfo(handle).used / nvmlDeviceGetMemoryInfo(handle).total * 10)
        used_F = float(nvmlDeviceGetMemoryInfo(handle).used / nvmlDeviceGetMemoryInfo(handle).total)
        memOccupyInt.append(used)
        memOccupyFloat.append(used_F)
    nvmlShutdown()
    return memOccupyInt, memOccupyFloat

def getRandom():
    '''
        Just for show.
    '''
    ans = []
    ans_f = []
    for i in range(4):
        p = random.uniform(0, 1.0)
        ans.append(int(p * 10))
        ans_f.append(p)
    return ans, ans_f

def main(stdscr):
    occupy = [[1, 2, 3, 4, 2, 5, 7, 8, 10, 7, 6, 4, 2, 6, 5, 4, 3, 3, 5, 6],
                [1, 2, 3, 4, 2, 5, 7, 8, 10, 7, 6, 4, 2, 6, 5, 4, 3, 3, 5, 6],
                [1, 2, 3, 4, 2, 5, 7, 8, 10, 7, 6, 4, 2, 6, 5, 4, 3, 3, 5, 6],
                [1, 2, 3, 4, 2, 5, 7, 8, 10, 7, 6, 4, 2, 6, 5, 4, 3, 3, 5, 6]]
    while True:
        stdscr.erase()
        # set color
        stdscr.attron(curses.color_pair(6))
        curses.curs_set(False)
        # stdscr.nodelay(True)
        curses.halfdelay(10)
        mStr = ""
        for i in range(97):
            mStr += "—"
        # bottom line
        stdscr.addstr(0, 0, mStr)
        # top line  
        stdscr.addstr(11, 0, mStr)
        # split line
        for i in range(5):
            for j in range(10):
                y = j + 1
                x = 21 * i + 12
                ch = '|'
                stdscr.addch(y, x, ch)
        info = getDeviceInfo()
        # print devices info
        for i in range(4):
            stdscr.addstr(i * 2 + 2, 0, info[i][0])
            stdscr.addstr(i * 2 + 3, 0, info[i][1])
        stdscr.attroff(curses.color_pair(6))
        # list info
        tempInfo = getDeviceTemp()
        memOccupy, perc = getRandom()
        for i in range(4):
            stdscr.attron(curses.color_pair(i + 1))
            stdscr.addstr(12, i * 21 + 14, tempInfo[i] + "({:.2f}%)".format(perc[i] * 100))
            for j in range(19):
                for h in range(occupy[i][j + 1]):
                    stdscr.addch(10 - h, i * 21 + 12 + j + 1, '█')
                occupy[i][j] = occupy[i][j + 1]
            for h in range(memOccupy[i]):
                stdscr.addch(10 - h, i * 21 + 13 + 19, '█')
            occupy[i][19] = memOccupy[i]
            stdscr.attroff(curses.color_pair(i + 1))
        stdscr.refresh()
        # time.sleep(1)
        try:
            c = stdscr.getch()
            if c == ord('q'):
                break
        except:
            continue   

if __name__ == '__main__':
    stdscr = initCurses(13, 98)
    curses.wrapper(main)