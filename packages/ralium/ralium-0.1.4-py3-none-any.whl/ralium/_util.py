import http.server

import platform
import ctypes
import winreg
import sys
import os

__all__ = ["BasicHTTPServer", "_norm_url", "_get_path_limit", "_get_path", "_is_markup_filelike"]

class BasicHTTPServer(http.server.SimpleHTTPRequestHandler):
    pass

def _norm_url(path):
    return os.path.normpath(f"/{path.lstrip('/\\')}").replace("\\", "/")

def _get_path_limit_winreg():
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\FileSystem") as key:
        max_path_length, _ = winreg.QueryValueEx(key, "LongPathsEnabled")
        return max_path_length

def _get_path_limit():
    system = platform.system()

    try:
        if system == 'Windows':
            return os.path.getconf('PC_NAME_MAX')
        
        if system == 'Darwin':
            return os.pathconf('/', 'PC_NAME_MAX')

        libc = ctypes.CDLL('libc.so.6')
        return libc.fpathconf('/', 261)
    except:
        if system == "Windows":
            return 32767 if _get_path_limit_winreg() else 255

def _get_path(path):
    if getattr(sys, "frozen", False):
        return os.path.abspath(os.path.join(sys._MEIPASS, path))
    return os.path.abspath(path)

# A copy of the 'BeautifulSoup._markup_resembles_filename' function
def _is_markup_filelike(markup):
    path_characters = '/\\'
    extensions = ['.html', '.htm', '.xml', '.xhtml', '.txt']
    if isinstance(markup, bytes):
        path_characters = path_characters.encode("utf8")
        extensions = [x.encode('utf8') for x in extensions]
    filelike = False
    if any(x in markup for x in path_characters):
        filelike = True
    else:
        lower = markup.lower()
        if any(lower.endswith(ext) for ext in extensions):
            filelike = True
    return filelike