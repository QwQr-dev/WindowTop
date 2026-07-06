# coding = 'utf-8'

import os
from method import usumd as ud
from method.System import errcheck
import method.System.windows as ws
import method.System.otherapi as oapi
from method.System.winusutypes import *
from method.usumd import process, messagebox

_wtm_init_state = False


def WindowTop(
    state: bool = False, 
    hwnd: int = ws.GetForegroundWindow(), 
    is_zorder_top: bool = False, 
    nband: int = 1
):
    
    """ 窗口置顶 """

    if ws.IsUserAnAdmin() and is_zorder_top:
        import WindowTopMost as wtm
        global _wtm_init_state
        if not _wtm_init_state:
            if not wtm.WTMInit():
                return False
        
        _wtm_init_state = True
        if not wtm.WTMGetIAMKey(byref(ULONGLONG())):
            return False

        if state:
            if not wtm.WTMSetWindowBand(HWND(hwnd), 0, nband):
                return False
        else:
            if (not wtm.WTMSetWindowBand(HWND(hwnd), 0, wtm.ZBID_DESKTOP) or 
                not ws.SetWindowPos(hwnd, ws.HWND_NOTOPMOST, 0, 0, 0, 0, ws.SWP_NOMOVE | ws.SWP_NOSIZE, errcheck=False)):
                return False
        return True
    
    state = ws.HWND_TOPMOST if state else ws.HWND_NOTOPMOST
    if not ws.SetWindowPos(hwnd, state, 0, 0, 0, 0, ws.SWP_NOMOVE | ws.SWP_NOSIZE):
        return False
    return True



def RunFileDlg(
    title: str | None = None, 
    description: str | None = None, 
    hwnd: int | None = None, 
    icon_path: str = '',
    fuLoad: int = ws.LR_LOADFROMFILE
) -> None:
    
    """ 运行对话框 """
    hIcon = None
    if os.path.exists(icon_path):
        hIcon = ws.LoadImage(None, icon_path, ws.IMAGE_ICON, 0, 0, fuLoad)
    oapi.RunfileDlg(hwnd, hIcon, ud.syspath.SYSTEM32, title, description)


def get_self_hwnd() -> int:
    ''' 获取自身的 hwnd '''
    return errcheck.null_to_zero(process.get_exec_hwnd_from_pid(ws.GetCurrentProcessId()))


def control_menu_state(
    hwnd: int = ws.GetForegroundWindow(), 
    menu_flags: int = ws.WS_MAXIMIZEBOX | ws.WS_SIZEBOX    # 默认为禁止窗口最大化和调整窗口大小
):
    
    # 获取当前样式
    style = ws.GetWindowLongPtr(hwnd, ws.GWL_STYLE)
    # 去掉最大化框标志
    new_style = style & ~menu_flags
    ws.SetWindowLongPtr(hwnd, ws.GWL_STYLE, new_style)
    # 通知窗口重绘
    flags = ws.SWP_NOMOVE | ws.SWP_NOSIZE | ws.SWP_NOZORDER | ws.SWP_FRAMECHANGED
    ws.SetWindowPos(hwnd, 0, 0, 0, 0, 0, flags)

