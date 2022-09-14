from win32gui import GetWindowRect, SetForegroundWindow, GetClientRect, ShowWindow, FindWindow, ClientToScreen
from win32com import client
from functools import wraps
from time import sleep, time
from abc import ABC, abstractmethod
from mss.windows import MSS as mss
import numpy as np
import keyboard
import cv2

def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap

class WindowNotFoundError(ValueError):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

class Screenshot(ABC):
	def __init__(self, target: str) -> None:
		self._target = target
		self._shell = client.Dispatch("WScript.Shell")

	def search(self):
		self._hwnd = FindWindow(None, self._target)
		if not self._hwnd:
			raise WindowNotFoundError(f'No window with name "{self._target}" found')

		ShowWindow(self._hwnd, 5)
		self._shell.sendKeys(' ')
		SetForegroundWindow(self._hwnd)
		self._shell.sendKeys('%')
		sleep(0.1)

		_left, _top, _right, _bottom = GetClientRect(self._hwnd)
		left, top = ClientToScreen(self._hwnd, (_left, _top))
		right, bottom = ClientToScreen(self._hwnd, (_right, _bottom))

		self.x = left
		self.y = top
		self.width = right-left
		self.height = bottom-top

	@abstractmethod
	def capture(self):
		raise NotImplementedError()
			
class FastShot(Screenshot):
	def capture(self, update_hwnd: bool=False):
		if update_hwnd:
			self.search()
		
		with mss() as sct:
			rect = {'top': self.y, 'left': self.x, 'width': self.width, 'height': self.height}
			img_numpy = np.array(sct.grab(rect))
		return img_numpy


if __name__ == '__main__':
	screenshot = FastShot(target='League of Legends (TM) Client')#'league of legends', dpi=1.25)
	while True:
		if keyboard.is_pressed('alt'):
			img = screenshot.capture(update_hwnd=True)
			cv2.imwrite(f"screenshot/{round(time()*1000)}.png", img)
			print('screenshot')
			sleep(0.2)