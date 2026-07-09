# coding = 'utf-8'

import os
import mouse
import loguru
import keyboard
from method.usumd import process
from method.System.winusutypes import *
from method.System import windows as ws
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication
from PySide6.QtCore import QEvent, QObject, Qt, QRect, QTimer, Signal
from PySide6.QtGui import QCursor, QMouseEvent, QPainter, QPen, QColor


class HighlightWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint |
            Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setStyleSheet("background:transparent;")
        self.hide()
        self.target_rect = QRect()

    def set_target_rect(self, rect: QRect):
        self.target_rect = rect
        # 覆盖所有屏幕的完整区域
        from PySide6.QtGui import QGuiApplication
        screens = QGuiApplication.screens()
        if screens:
            total_geometry = screens[0].geometry()
            for s in screens[1:]:
                total_geometry = total_geometry.united(s.geometry())
        else:
            total_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(total_geometry)
        self.show()
        self.update()

    def paintEvent(self, event):
        if not self.target_rect.isNull():
            painter = QPainter(self)
            pen = QPen(QColor(255, 0, 0), 5)  # 红色，5像素宽
            painter.setPen(pen)
            # 将屏幕坐标转换为相对本窗口的坐标
            global_pos = self.target_rect.topLeft()
            local_pos = self.mapFromGlobal(global_pos)
            rect = QRect(local_pos, self.target_rect.size())
            painter.drawRect(rect)
        

class WindowFinder(QObject):
    """负责窗口查找逻辑的类"""
    window_locked = Signal(int, int, str, str)  # 信号：窗口句柄, PID, 进程名, 文件路径
    _trigger_lock = Signal()
    _trigger_stop = Signal()

    def __init__(self):
        super().__init__()
        self.highlighter = HighlightWidget()
        self.is_finding = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_highlight)
        self._trigger_lock.connect(self.lock_window)
        self._trigger_stop.connect(self.lock_window)

        self.press_esc = False
        self._candidate_hwnd = None
        self._pid = None
        self._class_name = None
        self._proc_name = None
        self._proc_path = None
        self._proc_title = None

    def start_find(self):
        """开始查找模式"""
        self.is_finding = True
        self.timer.start(30)  # 每30ms更新一次高亮位置

        # 监听全局事件
        mouse.hook(self.on_mouse_event)
        keyboard.on_press(self.on_key_press)
        loguru.logger.debug('开始查找窗口')

    def stop_find(self):
        """停止查找模式"""
        self.is_finding = False
        self.timer.stop()
        self.highlighter.hide()

        # 解除监听
        mouse.unhook_all()
        keyboard.unhook_all()
        loguru.logger.debug('停止查找窗口')
        print()
    
    def get_passed_hwnd(self):
        """获取要排除的 hwnd"""
        passed_hwnd = [
            self.highlighter.winId(),                                       # 排除自身窗口
            ws.FindWindow("Shell_TrayWnd", NULL),                           # 排除任务栏
            process.GetDesktopWindowHandle(),                               # 排除桌面窗口
            ws.FindWindow("XamlExplorerHostIslandWindow", NULL)             # 排除任务视图窗口
        ]
        return passed_hwnd

    def on_mouse_event(self, event):
        """处理鼠标事件"""
        if self.is_finding and isinstance(event, mouse.ButtonEvent) and event.event_type == 'down':
            if self._candidate_hwnd not in self.get_passed_hwnd():
                if event.button == 'left':
                    loguru.logger.debug('已按下鼠标左键，停止监听，并锁定窗口，返回相应的值')
                    self._trigger_lock.emit()

    def on_key_press(self, event):      
        """键盘按下回调"""
        if self.is_finding and event.name == 'esc':
            loguru.logger.debug('已按下Esc键，停止监听')
            self.press_esc = True
            self._trigger_stop.emit()

    def update_highlight(self):
        """实时更新所选的目标参量"""
        cursor_pos = QCursor.pos()
        hwnd = self.get_window_under_cursor(cursor_pos.x(), cursor_pos.y())
        hwnd = ws.GetAncestor(hwnd, ws.GA_ROOTOWNER)       # bug fixed: 修复 hwnd 返回不正确的问题
        if hwnd in self.get_passed_hwnd():
            hwnd = None
        
        if hwnd:
            self._candidate_hwnd = hwnd 
            rect = self.get_window_rect(hwnd)
            self.highlighter.set_target_rect(rect)
            self._pid = process.get_exec_pid_from_hwnd(hwnd)
            self._proc_path = process.GetProcessOrServPathById(self._pid)
            self._proc_name = os.path.basename(self._proc_path)
            window_title = (WCHAR * 2048)()
            ws.GetWindowText(hwnd, window_title, 2048, errcheck=False)
            self._proc_title = window_title.value
            class_name = (WCHAR * 2048)()
            ws.GetClassName(hwnd, class_name, 2048)
            self._class_name = class_name.value
        else:
            self.highlighter.hide()
            self._pid = None
            self._proc_name = None
            self._proc_path = None
            self._candidate_hwnd = None
            self._proc_title = None
            self._class_name = None

        loguru.logger.debug(
            f"hwnd={hwnd}, "
            f"pid={self._pid}, "
            f"name={self._proc_name}, "
            f"path={self._proc_path}, "
            f"title={self._proc_title}, "
            f"class_name={self._class_name}, "
            f"winId={self.highlighter.winId()}"
        )

    def lock_window(self):
        """锁定当前候选窗口"""
        if self.press_esc:      # bug fixed: 修复按下 Escape 键窗口不会恢复的问题
            self.window_locked.emit(0, 0, '', '')
            self.stop_find()
            return      # bug fixed: 修复在按下Esc键时，依旧进入下一个逻辑的问题

        if self._candidate_hwnd and not self.press_esc:     
            self.window_locked.emit(self._candidate_hwnd, self._pid, self._proc_name, self._proc_path)
            self.stop_find()
            return

    # ----- Windows API 包装 -----
    def get_window_under_cursor(self, x, y):
        point = ws.POINT(x, y)
        return ws.WindowFromPoint(point)

    def get_window_rect(self, hwnd):
        rect = ws.RECT()
        ws.GetWindowRect(hwnd, byref(rect))
        # 转换为 QRect
        return QRect(rect.left, rect.top,
                     rect.right - rect.left,
                     rect.bottom - rect.top)
    
