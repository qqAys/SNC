import base64
import subprocess
import tkinter
import winreg
from ctypes import windll
from os import popen, remove
from platform import release
from random import randint
from re import search
from tkinter import messagebox
from tkinter import ttk

APP_NAME = "SNC"
version = '1.0.0.5'
AMIDEWINx64_PATH = "AMIDEWINx64.EXE"

tmp = open("tmp.ico", "wb+")
img = b'AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABMLAAATCwAAAAAAAAAAAAD///8A////AP///wD///8F' \
      b'////Sv///6j////k/////P////z////k////qP///0r///8F////AP///wD///8A////AP///wD///8Y////k' \
      b'////+/////////////////x8fH/2tra/+bm5v/////v////k////xj///8A////AP///wD///8Y////sv/////////////////////Kysr' \
      b'/ZmZm/3Jycv9jY2P/kJCQ//f39/////+y////GP///wD///8F////k//////////////////////9/f3/a2tr/6+vr/+enp7/b29v/2VlZf' \
      b'+zs7P//////////5P///8F////Sv///+///////////////////////Pz8/2tra/+8vLz/Xl5e/66urv+VlZX/l5eX///////////v////Sv' \
      b'///6j///////////////////////////////+Xl5f/lJSU/46Ojv9wcHD/ZWVl/9PT0////////////////6j////k' \
      b'////////////////6urq/6ioqP+goKD/oaGh/2JiYv/o6Oj/z8/P/+Pj4//////////////////////k/////P//////////6urq/19fX' \
      b'/96enr/oqKi/3l5ef8mJib/s7Oz/////////////////////////////////P////z//////////6ampv9sbGz////////////9/f3/goKC' \
      b'/19fX//8/Pz///////////////////////////z////k//////////+Ojo7/jo6O/////////////////+bm5v9NTU3/3d3d' \
      b'///////////////////////////k////qP//////////paWl/29vb//////////////////+/v7/Z2dn/7q6uv' \
      b'//////////////////////////qP///0r////v/////93d3f9ISEj/0tLS/////////////////3Jycv+1tbX/////////////////////7' \
      b'////0r///8F////k///////////n5+f/1hYWP/X19f//////+Xl5f9bW1v/2dnZ/////////////////////5P///8F////AP///xj///+y' \
      b'//////39/f+srKz/ZmZm/3p6ev9qamr/oaGh//7+/v///////////////7L///8Y////AP///wD///8A////GP///5P////v//////Dw8P' \
      b'/Y2Nj/5OTk////////////////7////5P///8Y////AP///wD///8A////AP///wD///8F////Sv///6j////k/////P////z////k////qP' \
      b'///0r///8F////AP///wD' \
      b'///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA== '
tmp.write(base64.b64decode(img))
tmp.close()

# 实例化GUI
window = tkinter.Tk()


class MenuCommand(object):
    @staticmethod
    def menu_about():
        tkinter.messagebox.showinfo("关于",
                                    f'ver:{version}\n\n作者：Jinx\n你可以在下方网址进行更新或与我联系：\nhttps://qqays.xyz\n© 2021 - 2022 '
                                    f'qqAys.')


class SetMain(object):
    def __init__(self):
        # 判断管理员身份
        if windll.shell32.IsUserAnAdmin() == 0:
            tkinter.messagebox.showerror(title='错误', message='请以管理员身份运行。')
            window.destroy()
            exit()
        print('░' * 34)
        print('░    ██████  ███▄    █  ▄████▄   ░')
        print('░  ▒██    ▒  ██ ▀█   █ ▒██▀ ▀█   ░')
        print('░  ░ ▓██▄   ▓██  ▀█ ██▒▒▓█    ▄  ░')
        print('░    ▒   ██▒▓██▒  ▐▌██▒▒▓▓▄ ▄██  ░')
        print('░  ▒██████▒▒▒██░   ▓██░▒ ▓███▀   ░')
        print('░  ▒ ▒▓▒ ▒ ░░ ▒░   ▒ ▒ ░ ░▒ ▒    ░')
        print('░  ░ ░▒  ░  ░ ░░   ░ ▒░  ░  ▒    ░')
        print('░  ░  ░  ░     ░   ░ ░ ░         ░')
        print('░        ░           ░ ░ ░       ░')
        print('░' * 34)
        print('░            SNC_Main            ░')
        print('░              Jinx              ░')
        print('░        https://qqays.xyz       ░')
        print(f'░           ver{version}           ░')
        print('░' * 34)
        self.WIN_REGISTRY_PATH = "SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"

    # 获取设备列表
    @staticmethod
    def devices_list():
        check = subprocess.check_output('GETMAC /v /FO list', stderr=subprocess.STDOUT)
        device_info = check.decode('gbk')
        return device_info

    @staticmethod
    def random_mac():
        mac = [0x52, 0x54, 0x00,
               randint(0x00, 0x7f),
               randint(0x00, 0xff),
               randint(0x00, 0xff)]
        new_mac = ''.join(map(lambda x: "%02x" % x, mac)).upper()
        show_mac = '-'.join(map(lambda x: "%02x" % x, mac)).upper()
        text_mac_info.delete('1.0', 'end')
        text_mac_info.insert(tkinter.INSERT, f'生成随机物理地址：\n{show_mac}\n\n')
        return new_mac

    @staticmethod
    def set_mac():
        target_device = entry.get('1.0', 'end')
        progress_bar['value'] = 10
        window.update()
        return target_device.strip()

    def set_mac_address(self, target_device, new_mac):
        reg_hdl = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg_hdl, self.WIN_REGISTRY_PATH)
        info = winreg.QueryInfoKey(key)
        progress_bar['value'] = 20
        window.update()

        adapter_key = None
        adapter_path = None
        target_index = -1

        for index in range(info[0]):
            subkey = winreg.EnumKey(key, index)
            path = self.WIN_REGISTRY_PATH + "\\" + subkey

            if subkey == 'Properties':
                break

            new_key = winreg.OpenKey(reg_hdl, path)
            try:
                adapterDesc = winreg.QueryValueEx(new_key, "DriverDesc")
                if adapterDesc[0] == target_device:
                    adapter_path = path
                    target_index = index
                    progress_bar['value'] = 30
                    text_mac_info.insert(tkinter.INSERT, f'查找到适配器地址：\n{adapter_path}\n\n')
                    window.update()
                    break
                else:
                    winreg.CloseKey(new_key)
            except WindowsError as err:
                if err.errno == 2:
                    pass
                else:
                    raise err

        if adapter_path is None:
            winreg.CloseKey(key)
            winreg.CloseKey(reg_hdl)
            text_mac_info.delete('1.0', 'end')
            tkinter.messagebox.showerror(title='错误', message='找不到目标设备，点击确定以继续。')
            device_status = 1
            return device_status

        adapter_key = winreg.OpenKey(reg_hdl, adapter_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(adapter_key, "NetworkAddress", 0, winreg.REG_SZ, new_mac)
        text_mac_info.insert(tkinter.INSERT, f'正在修改物理地址……\n\n')
        winreg.CloseKey(adapter_key)
        winreg.CloseKey(key)
        winreg.CloseKey(reg_hdl)
        progress_bar['value'] = 40
        window.update()
        text_mac_info.insert(tkinter.INSERT, f'物理地址修改成功。\n\n')
        self.restart_adapter(target_index, target_device)

    @staticmethod
    def get_sys_uuid():
        uuid = popen(f'{AMIDEWINx64_PATH} /SU')
        res = uuid.read()
        for line in res.splitlines()[11:]:
            return line.strip()[42:-2]

    @staticmethod
    def random_sys_uuid_index():
        progress_bar['value'] = 50
        random_hex = [randint(0x00, 0xff)]
        index = ''.join(map(lambda x: "%02x" % x, random_hex)).upper()
        progress_bar['value'] = 60
        return index

    @staticmethod
    def new_sys_uuid():
        old_uuid = SetMain.get_sys_uuid()
        if old_uuid is None:
            uuid_status = 1
            return uuid_status
        uuid_index = SetMain.random_sys_uuid_index()
        if uuid_index == old_uuid[-2:]:
            uuid_index = SetMain.random_sys_uuid_index()
            uuid = old_uuid[:-2] + uuid_index
            text_mac_info.insert(tkinter.INSERT, f'生成随机UUID：\n{uuid}\n\n')
            progress_bar['value'] = 70
        else:
            uuid = old_uuid[:-2] + uuid_index
            text_mac_info.insert(tkinter.INSERT, f'生成随机UUID：\n{uuid}\n\n')
            progress_bar['value'] = 70
        return uuid

    @staticmethod
    def change_uuid():
        uuid = SetMain.new_sys_uuid()
        if uuid == 1:
            return
        res = popen(f'{AMIDEWINx64_PATH} /SU {uuid}')
        text_mac_info.insert(tkinter.INSERT, f'正在修改UUID……\n\n')
        progress_bar['value'] = 80
        res = res.read()
        text_mac_info.insert(tkinter.INSERT, f'修改UUID成功。\n\n')
        for line in res.splitlines()[11:]:
            return line.strip()[42:-1]

    def restart_adapter(self, target_index, target_device):
        text_mac_info.insert(tkinter.INSERT, f'正在重启适配器：\n{target_device}\n\n')
        if release() == 'XP':
            cmd = "devcon hwids =net"
            try:
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            except FileNotFoundError:
                raise
            query = '(' + target_device + '\r\n\s*.*:\r\n\s*)PCI\\\\(([A-Z]|[0-9]|_|&)*)'
            query = query.encode('ascii')
            match = search(query, result)
            cmd = 'devcon restart "PCI\\' + str(match.group(2).decode('ascii')) + '"'
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            text_mac_info.insert(tkinter.INSERT, f'重启适配器成功。\n\n')
            progress_bar['value'] = 90
            window.update()
        else:
            cmd = "wmic path win32_networkadapter where index=" + str(target_index) + " call disable"
            subprocess.check_output(cmd)
            cmd = "wmic path win32_networkadapter where index=" + str(target_index) + " call enable"
            subprocess.check_output(cmd)
            text_mac_info.insert(tkinter.INSERT, f'重启适配器成功，请等待网络连接。\n\n')
            progress_bar['value'] = 90
            window.update()

    def run(self):
        res1 = tkinter.messagebox.askyesno('提示', '确定要继续吗？')
        if res1 is True:
            target_device = self.set_mac()
            mac_address = self.random_mac()
            device_status = self.set_mac_address(target_device, mac_address)
            self.change_uuid()
            progress_bar['value'] = 100
            window.update()
            tkinter.messagebox.showinfo('提示', '修改成功。')
            self.end()
        else:
            return

    def end(self):
        text_mac_info.delete('1.0', 'end')
        mac_info = tkinter.COMMAND = run.devices_list()
        text_mac_info.insert(tkinter.INSERT, f'当前UUID：{self.get_sys_uuid()}\n{mac_info}')
        progress_bar['value'] = 0


# 界面初始化：阶段1
width = 560
height = 500
# -居中显示
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
window.geometry(size_geo)
window.resizable(0, 0)

# -菜单初始化
main_menu = tkinter.Menu(window)
menu = MenuCommand()
main_menu.add_command(label="关于", command=menu.menu_about)
window.config(menu=main_menu)
# -标题、图标、LOGO初始化
window.title(APP_NAME)
window.iconbitmap("tmp.ico")
remove("tmp.ico")

# 实例化类
run = SetMain()

# 界面初始化：阶段2
tkinter.Label(window, text='信息框', font=('', 10)).pack()
text_mac_info = tkinter.Text(window)
text_mac_info.pack()

# -获取设备列表并插入文本框
mac_info = tkinter.COMMAND = run.devices_list()
text_mac_info.insert(tkinter.INSERT, f'当前UUID：{run.get_sys_uuid()}\n{mac_info}')

# 界面初始化：阶段3
tkinter.Label(window, text="\n适配器名", font=('', 10)).pack()
# -输入框初始化
entry = tkinter.Text(window, height=1)
entry.pack()

# -执行按钮初始化
tkinter.Button(window, text='执行', font=('', 10), command=run.run).place(x=255, y=410)

# -进度条初始化
progress_bar = ttk.Progressbar(window, length=480)
progress_bar.place(x=50, y=450)
# --设置进度极值
progress_bar['maximum'] = 100

window.mainloop()
