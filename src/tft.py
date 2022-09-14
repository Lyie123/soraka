from screenshot import FastShot
from detection import Detector
from typing import Dict
from pprint import pprint
import numpy as np
import cv2

def crop(img: np.array, area: tuple[int, int, int, int]) -> np.array:
	return img[area[0]:area[1], area[2]:area[3], :]

class Tft:
	# ystart, yend, xstart, xend @ 1920x1080 resolution
	AREA_STORE = (920, 1080, 475, 1490) 
	AREA_GOLD = (883, 911, 869, 924)
	AREA_LADDER = (189, 779, 1690, 1922)
	AREA_LEVEL = (883, 906, 315, 365)
	AREA_XP = (882, 882+28, 402, 402+56)
	AREA_STREAK = (878, 909, 993, 1025)
	AREA_PROGRESS = (8, 35, 760, 812)

	def __init__(self):
		self._screenshot = FastShot('League of Legends (TM) Client')
		self._detector = Detector()

	def extract(self, img: np.array) -> Dict:
		store = self._detector.find_all(crop(img, self.AREA_STORE), match='store')
		gold = self._detector.find_text(crop(img, self.AREA_GOLD), config='--psm 10 digits').strip()
		level = self._detector.find_text(crop(img, self.AREA_LEVEL), config='--psm 10 digits').strip()
		xp = self._detector.find_text(crop(img, self.AREA_XP), config=' -l eng --oem 1 -c tessedit_char_whitelist=0123456789/ --psm 11')
		streak = self._detector.find_text(crop(img, self.AREA_STREAK), config='--psm 8').strip()
		try:
			progress_t1, progress_t2 = self._detector.find_text(crop(img, self.AREA_PROGRESS)).split('-')
		except ValueError:
			progress_t1 = ''
			progress_t2 = ''
		return {
			'gold': gold,
			'store': [n.name for n in sorted(store, key=lambda x: x.x)],
			'level': level,
			'xp': xp,
			'streak': streak,
			'progress': {'t1': progress_t1.strip(), 't2': progress_t2.strip()}
		}
	def get_gamestate(self):
		img = self._screenshot.capture(update_hwnd=True)[:, :, :3]
		return self.extract(img)



if __name__ == '__main__':
	img = cv2.imread(r'tests\screenshot\s2.png')
	tft = Tft()
	cv2.imwrite('xp.png', tft._crop(img, tft.AREA_XP))