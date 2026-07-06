# coding = 'utf-8'

import sys
import loguru
import Functions as fs
import method.usumd as ud
from PySide6 import QtWidgets
import method.System.windows as ws
from method.System.winusutypes import *
from PySide6.QtCore import QCoreApplication
from GUI import Ui_MainWindow, WindowFinder
from method.System.otherapi._user32 import zorder_band_names


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.self_hwnd = 0
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化变量
        self.locked_hwnd = None
        self.locked_pid = None
        self.locked_proc_name = None
        self.locked_proc_path = None

        # 控制开关
        self.set_window_top_state = False
        self.locked_window_top_button_state = False
        self.opened_file_location_button_state = False

        # 创建查找器对象
        self.finder = WindowFinder()
        self.finder.window_locked.connect(self.on_window_locked)

        # 绑定按钮点击事件
        self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.ui.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)
        self.ui.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)
        self.ui.pushButton_4.clicked.connect(self.on_pushButton_4_clicked)
        if not ws.IsUserAnAdmin() or ws.WIN32_WINNT < ws.WIN32_WINNT_WIN8:
            self.ui.checkBox.setEnabled(False)
            
        for num in range(0, 19):
            try:
                self.ui.comboBox.addItem("")
                self.ui.comboBox.setItemText(num, QCoreApplication.translate("MainWindow", zorder_band_names(num), None))
            except:
                pass


    def on_window_locked(self, hwnd, pid, proc_name, proc_path):
        self.locked_hwnd = hwnd
        self.locked_pid = pid
        self.locked_proc_name = proc_name
        self.locked_proc_path = proc_path
        self.deal_all_events()


    def deal_all_events(self):
        # 要执行的功能放在下面
        if self.finder.press_esc:   # bug fixed: 修复按下 Escape 键窗口不会恢复的问题
            self.finder.press_esc = False
            self.locked_hwnd = None
            self.locked_pid = None
            self.locked_proc_name = None
            self.locked_proc_path = None
            self.deal_pressed_esc_func()
            return
        
        if self.locked_window_top_button_state:
            self.deal_locked_window_top_func()
            self.locked_window_top_button_state = False
            return
        
        if self.opened_file_location_button_state:
            self.deal_opened_file_location()
            self.opened_file_location_button_state = False
            return
        

    # 功能实现部分
    def deal_pressed_esc_func(self):
        self.locked_window_top_button_state = False
        self.opened_file_location_button_state = False
        if ws.ShowWindow(self.self_hwnd, ws.SW_SHOWNORMAL):
            loguru.logger.debug('已成功恢复窗口')

    def deal_locked_window_top_func(self):
        loguru.logger.debug('相应的值如下：')
        loguru.logger.debug(f'目标 hwnd: {self.locked_hwnd}')
        loguru.logger.debug(f'PID: {self.locked_pid}')
        loguru.logger.debug(f'进程名: {self.locked_proc_name}')
        if not ws.ShowWindow(self.self_hwnd, ws.SW_SHOWNORMAL):     # bug fixed: 根据文档说明，修复其逻辑错误的问题
            fs.WindowTop(self.set_window_top_state, self.locked_hwnd, self.ui.checkBox.isChecked(), self.ui.comboBox.currentIndex())
            if self.set_window_top_state:
                loguru.logger.debug('已成功恢复窗口并将目标窗口置顶')
            else:
                loguru.logger.debug('已成功恢复窗口并将目标窗口取消置顶')
        ws.SetForegroundWindow(self.self_hwnd)

    def deal_opened_file_location(self):
        if not ws.ShowWindow(self.self_hwnd, ws.SW_SHOWNORMAL):
            loguru.logger.debug('已成功恢复窗口')
            ws.SetForegroundWindow(self.self_hwnd)
        
        try:
            ud.open_file_location2(self.locked_proc_path)
            loguru.logger.debug(f'已成功打开文件所在的位置，路径: {self.locked_proc_path}')
        except Exception as e:
            loguru.logger.error(f'未能打开文件所在的位置，原因如下：\n{str(e)}')
            ud.messagebox.showerror('WindowTop', f'未能打开文件所在的位置，原因如下：\n{str(e)}', self.self_hwnd)


    # 按钮事件处理
    def on_pushButton_clicked(self):
        self.set_window_top_state = True
        self.locked_window_top_button_state = True
        loguru.logger.debug('按钮1已响应')
        ws.ShowWindow(self.self_hwnd, ws.SW_HIDE)
        self.finder.start_find()

    def on_pushButton_2_clicked(self):
        self.set_window_top_state = False
        self.locked_window_top_button_state = True
        loguru.logger.debug('按钮2已响应')
        ws.ShowWindow(self.self_hwnd, ws.SW_HIDE)
        self.finder.start_find()
    
    def on_pushButton_3_clicked(self):
        loguru.logger.debug('按钮3已响应')
        fs.RunFileDlg(hwnd=self.self_hwnd)

    def on_pushButton_4_clicked(self):
        loguru.logger.debug('按钮4已响应')
        self.opened_file_location_button_state = True
        ws.ShowWindow(self.self_hwnd, ws.SW_HIDE)
        self.finder.start_find()


if __name__ == '__main__':
    loguru.logger.info('程序初始化')

    if not ws.IsUserAnAdmin():
        ud.messagebox.showinfo('WindowTop', '建议以管理员运行，部分功能会因此受限')

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    self_hwnd = fs.get_self_hwnd()
    window.self_hwnd = self_hwnd
    fs.WindowTop(True, self_hwnd)   # 窗口置顶
    fs.control_menu_state(self_hwnd)    # 默认为禁止窗口最大化和调整窗口大小
    sys.exit(app.exec())
