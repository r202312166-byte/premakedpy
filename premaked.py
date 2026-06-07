def when_opened_with() -> str:
    try:
        import sys
        if len(sys.argv) > 1:
            fpath = sys.argv[1]
            with open(fpath, 'r', encoding='utf-8') as file:
                return file.read()
    except Exception as e:
        print(e)
        return None
def tkinput(root, tit:str) -> str:
    try:
        import tkinter as tk
    except Exception as e:
        print(e)
        return None
    res = None
    def call_func():
        nonlocal res
        res = askety.get()
        askwin.destroy()
    askwin = tk.Toplevel(root)
    askwin.title(tit)
    askwin.geometry("200x50")

    askety = tk.Entry(askwin, width=20)
    askety.pack()

    setbtn = tk.Button(askwin, text="Enter", command=call_func)
    setbtn.pack()

    askwin.wait_window(askwin)
    return res

def fsave(content:str, type:list) -> None:
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception as e:
        print(e)
        return None
    ftype = [(f"{i} files", f"*.{i}") for i in type]
    ftype.append(("All files", "*.*"))
    path = filedialog.asksaveasfilename(
        title="Save as",
        initialdir="/",
        filetypes=ftype
    )
    if path:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
def fopen(readcontent:bool, type:list) -> str:
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception as e:
        print(e)
        return None
    ftype = [(f"{i} files", f"*.{i}") for i in type]
    ftype.append(("All files", "*.*"))
    path = filedialog.askopenfilename(
        title="Open",
        initialdir="/",
        filetypes=ftype
    )
    if path and readcontent:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    elif path:
        return path
def fconfig(root, items:list, cfile:str) -> None:
    try:
        import tkinter as tk
        import json
    except Exception as e:
        print(e)
        return None
    cfwin = tk.Toplevel(root)
    cfwin.title("Settings")
    cfwin.geometry(f"300x{25*len(items)+25}")
    rows = 0
    entrys = []
    for i in items:
        lb = tk.Label(cfwin, text=i)
        lb.grid(row=rows, column=0)
        entry = tk.Entry(cfwin, width=20)
        entry.grid(row=rows, column=1)
        entrys.append(entry)
        rows += 1
    def saveset():
        cfdict = {}
        for idx, ety in enumerate(entrys):
            cfdict.update({items[idx]:ety.get()})
        with open(cfile, 'w', encoding='utf-8') as file:
            json.dump(cfdict, file, indent=4)
        cfwin.destroy()
    svsetting = tk.Button(cfwin, text="Save Settings", command=saveset)
    svsetting.grid(row=rows, column=0)
def console_menu(tit:str, options:list, functions:list) -> object:
    idx = 1
    print(tit)
    for i in options:
        print(f"{idx}.: {i}")
        idx += 1
    menudic = {}
    menulis = [None]
    j = 0
    for i in functions:
        menulis.append(i)
        menudic.update({options[j]:i})
        j += 1
    coice = input("Enter choice: ")
    try:
        res = menulis[int(coice)]
    except TypeError:
        res = menudic[coice]
    finally:
        return res
def urlget(url:str) -> str:
    try:
        import urllib.request as ur
    except Exception as e:
        print(e)
        return None
    with ur.urlopen(url) as response:
        get = response.read().decode('utf-8')
        print(response.status)
    return get
def urlpost(url:str, data:dict) -> str:
    try:
        import urllib.request as ur
        import urllib.parse as up
    except Exception as e:
        print(e)
        return None
    data_bytes = up.urlencode(data).encode('utf-8')
    req = ur.Request(url, data=data_bytes)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    with ur.urlopen(req) as response:
        get = response.read().decode('utf-8')
        print(response.status)
        return get
def urlpostfile(url:str, filepath:str) -> str:
    try:
        import urllib.request as ur
        import urllib.parse as up
        import os
        from random import randint
    except Exception as e:
        print(e)
        return None
    filename = os.path.basename(filepath)
    boundary = f'----pulb|={randint(10000, 99999)}=|----'
    blankline = '\r\n'
    payload = []
    payload.append(f'--{boundary}')
    payload.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"')
    payload.append('Content-Type: application/octet-stream')
    payload.append('')
    payloadbytes = [line.encode('utf-8') for line in payload]
    with open(filepath, 'rb') as file:
        filebytes = file.read()
    bodybytes = b'\r\n'.join(payloadbytes) + b'\r\n' + filebytes + f'\r\n--{boundary}--\r\n'.encode('utf-8')
    req = ur.Request(url, data=bodybytes)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    req.add_header('Content-Length', str(len(bodybytes)))
    with ur.urlopen(req) as response:
        return response.read().decode('utf-8')