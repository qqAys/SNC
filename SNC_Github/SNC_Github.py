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
