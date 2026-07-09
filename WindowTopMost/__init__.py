# coding = 'utf-8'
#
# 原项目为：https://github.com/xmc0211/WindowTopMost
#
# Warning:
# 如果要编译 WindowTopMost.dll 在 Python 环境下使用，需要注意以下情况（项目中的 WindowTopMost.dll 已经处理过，无需再更改）
# 原 WindowTopMost.dll 中的 WTMGetWorkerPath() （位于 DllMain.cpp）函数的源码为
#
# std::_tstring WTMGetWorkerPath() {
#     TCHAR ModulePathBuffer[2048];
#     GetModuleFileName(NULL, ModulePathBuffer, _countof(ModulePathBuffer));
#     std::_tstring ModuleFullPath(ModulePathBuffer);
#     size_t lastBackslashPos = ModuleFullPath.find_last_of(TEXT("\\"));
#     return ModuleFullPath.substr(0, lastBackslashPos + 1) + IAMWORKER_IMAGENAME;
# }
#
# 使用 Python 调用 WindowTopMost.dll 中的函数时，
# 要将上述函数的源码改成以下内容才能正常工作，
# 不然会一直重定向为 python.exe 的路径
# 从而导致部分函数无法正常工作
# 更改后的源码如下
#
# std::_tstring WTMGetWorkerPath() {
#     TCHAR ModulePathBuffer[2048];
#     HMODULE hmodule;
#     hmodule = GetModuleHandle(TEXT("WindowTopMost.dll"));
#     GetModuleFileName(hmodule, ModulePathBuffer, _countof(ModulePathBuffer));
#     std::_tstring ModuleFullPath(ModulePathBuffer);
#     size_t lastBackslashPos = ModuleFullPath.find_last_of(TEXT("\\"));
#     return ModuleFullPath.substr(0, lastBackslashPos + 1) + IAMWORKER_IMAGENAME;
# }
# 
# 更改后进行编译即可正常工作 

import os
import pathlib
import method.usumd as ud
from method.System.otherapi._user32 import *

# Loading DLL
def _get_file_path(path: str, file_type: str) -> list[str]:
    path_list = []
    for c in pathlib.Path(path).glob(file_type):
        path_list.append(os.path.normpath(str(c)))
    return path_list

def _get_WindowTopMost_DLL_path() -> str:
    dll_paths = _get_file_path(f"{ud.get_self_dir()}\\WindowTopMost", '*.dll')
    for i in dll_paths:
        if os.path.basename(i).lower() == 'WindowTopMost.dll'.lower():
            return os.path.abspath(i)
    raise FileNotFoundError('No such file: WindowTopMost.dll')

_WindowTopMost = WinDLL(_get_WindowTopMost_DLL_path(), use_last_error=True)
#############################################################################


def WTMCheckForDll() -> int:
    WTMCheckForDll = _WindowTopMost.WTMCheckForDll
    WTMCheckForDll.restype = BOOL
    res = WTMCheckForDll()
    return res


def WTMUnloadWorker() -> int:
    WTMUnloadWorker = _WindowTopMost.WTMUnloadWorker
    WTMUnloadWorker.restype = BOOL
    res = WTMUnloadWorker()
    return res


def WTMCheckEnvironment() -> int:
    WTMCheckEnvironment = _WindowTopMost.WTMCheckEnvironment
    WTMCheckEnvironment.restype = BOOL
    res = WTMCheckEnvironment()
    return res


def WTMInit() -> int:
    WTMInit = _WindowTopMost.WTMInit
    WTMInit.restype = BOOL
    res = WTMInit()
    return res


def WTMUninit() -> int:
    WTMUninit = _WindowTopMost.WTMUninit
    WTMUninit.restype = BOOL
    res = WTMUninit()
    return res


def WTMEnableUIAccess() -> int:
    WTMEnableUIAccess = _WindowTopMost.WTMEnableUIAccess
    WTMEnableUIAccess.restype = BOOL
    res = WTMEnableUIAccess()
    return res


def WTMCreateUIAccessWindow(
    dwExStyle: int, 
    lpClassName: str | bytes, 
    lpWindowName: str | bytes, 
    dwStyle: int, 
    X: int, 
    Y: int, 
    nWidth: int, 
    nHeight: int, 
    hWndParent: int, 
    hMenu: int, 
    hInstance, 
    lpParam,
    unicode: bool = True
) -> int:
    
    WTMCreateUIAccessWindow = _WindowTopMost.WTMCreateUIAccessWindowW if unicode else _WindowTopMost.WTMCreateUIAccessWindowA
    WTMCreateUIAccessWindow.argtypes = [
        DWORD,
        (LPCWSTR if unicode else LPCSTR),
        (LPCWSTR if unicode else LPCSTR),
        DWORD,
        INT,
        INT,
        INT,
        INT,
        HWND,
        HMENU,
        HINSTANCE,
        LPVOID
    ]

    WTMCreateUIAccessWindow.restype = HWND
    res = WTMCreateUIAccessWindow(
        dwExStyle,
        lpClassName,
        lpWindowName,
        dwStyle,
        X,
        Y,
        nWidth,
        nHeight,
        hWndParent,
        hMenu,
        hInstance,
        lpParam
    )

    return res


def WTMSetWindowBand(
    hWnd: int,
    hWndInsertAfter: int,
    dwBand: int 
) -> int:
    
    WTMSetWindowBand = _WindowTopMost.WTMSetWindowBand
    WTMSetWindowBand.argtypes = [HWND, HWND, DWORD]
    WTMSetWindowBand.restype = BOOL
    res = WTMSetWindowBand(hWnd, hWndInsertAfter, dwBand)
    return res


def WTMCreateWindowInBand(
    dwExStyle: int,
    lpClassName: str | bytes,
    lpWindowName: str | bytes,
    dwStyle: int,
    X: int,
    Y: int,
    nWidth: int,
    nHeight: int,
    hWndParent: int,
    hMenu: int,
    hInstance,
    lpParam,
    dwBand: int,
    unicode: bool = True
) -> int:
    
    WTMCreateWindowInBand = _WindowTopMost.WTMCreateWindowInBandW if unicode else _WindowTopMost.WTMCreateWindowInBandA
    WTMCreateWindowInBand.argtypes = [
        DWORD,
        (LPCWSTR if unicode else LPCSTR),
        (LPCWSTR if unicode else LPCSTR),
        DWORD,
        INT,
        INT,
        INT,
        INT,
        HWND,
        HMENU,
        HINSTANCE,
        LPVOID,
        DWORD
    ]

    WTMCreateWindowInBand.restype = HWND
    res = WTMCreateWindowInBand(
        dwExStyle,
        lpClassName,
        lpWindowName,
        dwStyle,
        X,
        Y,
        nWidth,
        nHeight,
        hWndParent,
        hMenu,
        hInstance,
        lpParam,
        dwBand
    )

    return res


def WTMCreateWindowInBandEx(
    dwExStyle: int,
    lpClassName: str | bytes,
    lpWindowName: str | bytes,
    dwStyle: int,
    X: int,
    Y: int,
    nWidth: int,
    nHeight: int,
    hWndParent: int,
    hMenu: int,
    hInstance,
    lpParam,
    dwBand: int,
    dwInternalFlag: int,
    unicode: bool = True
) -> int:
    
    WTMCreateWindowInBandEx = _WindowTopMost.WTMCreateWindowInBandExW if unicode else _WindowTopMost.WTMCreateWindowInBandExA
    WTMCreateWindowInBandEx.argtypes = [
        DWORD,
        (LPCWSTR if unicode else LPCSTR),
        (LPCWSTR if unicode else LPCSTR),
        DWORD,
        INT,
        INT,
        INT,
        INT,
        HWND,
        HMENU,
        HINSTANCE,
        LPVOID,
        DWORD,
        DWORD
    ]

    WTMCreateWindowInBandEx.restype = HWND
    res = WTMCreateWindowInBandEx(
        dwExStyle,
        lpClassName,
        lpWindowName,
        dwStyle,
        X,
        Y,
        nWidth,
        nHeight,
        hWndParent,
        hMenu,
        hInstance,
        lpParam,
        dwBand,
        dwInternalFlag
    )

    return res


def WTMGetWindowBand(hWnd: int, pdwBand) -> int:
    WTMGetWindowBand = _WindowTopMost.WTMGetWindowBand
    WTMGetWindowBand.argtypes = [HWND, LPDWORD]
    WTMGetWindowBand.restype = BOOL
    res = WTMGetWindowBand(hWnd, pdwBand)
    return res


def WTMGetIAMKey(pIAMKey) -> int:
    WTMGetIAMKey = _WindowTopMost.WTMGetIAMKey
    WTMGetIAMKey.argtypes = [PULONGLONG]
    WTMGetIAMKey.restype = BOOL
    res = WTMGetIAMKey(pIAMKey)
    return res
