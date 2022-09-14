import requests
import os
import cv2
import numpy as np

CDRAGON_CHAMPIONS = 'https://raw.communitydragon.org/latest/cdragon/tft/en_us.json'
CDRAGON_BASE_STORE = 'https://raw.communitydragon.org/latest/game/assets/ux/tft/championsplashes/'
CDRAGON_HEALTHBAR = 'https://raw.communitydragon.org/latest/game/assets/ux/tft/tfthealthbaratlas.png'

PATH_STORE = './assets/templates/store/'
PATH_HEALTHBAR = './assets/templates/ux/'
PATH_TRAINING = './training_data/'


def setup():
	# create training data structure
	data = requests.get(CDRAGON_CHAMPIONS).json()

	cols = ['apiName', 'icon']
	champions = [{k: champion[k] for k in cols} for champion in data['sets']['7']['champions']]

	try:
		for champion in champions:
			os.makedirs(f"{PATH_TRAINING}{champion['apiName']}")

		os.mkdir(f"{PATH_TRAINING}NO_CHAMPION")
	except FileExistsError as e:
		print(e)

	try:
		os.makedirs(os.path.dirname(PATH_STORE))	
		for champion in champions:
			with open(f"{PATH_STORE}{champion['apiName']}.png", 'wb') as f:
				f.write(requests.get(f"{CDRAGON_BASE_STORE}{os.path.basename(champion['icon'].replace('dds', 'png').lower())}", stream=True).content)

		mask = np.full((128, 256, 1), 255, dtype=np.uint8)
		mask[35:, :170] = 0
		mask[0:15, 90:166] = 0
		cv2.imwrite(f'{PATH_STORE}mask.png', mask)
	except FileExistsError as e:
		print(e)
	
	try:
		os.makedirs(os.path.dirname(PATH_HEALTHBAR))
		with open(f"{PATH_HEALTHBAR}healthbar.png", 'wb') as f:
			f.write(requests.get(CDRAGON_HEALTHBAR, stream=True).content)
	except FileExistsError as e:
		print(e)

def training_data_stats():
	stats = {}
	for n in os.listdir(PATH_TRAINING):
		_, _, files = next(os.walk(f'{PATH_TRAINING}{n}'))
		stats[n] = len(files)
	stats = dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))
	print(stats)

def crop_champions_from_bench(path_to_screenshots: str):
	for n in os.listdir(path_to_screenshots):
		f = os.path.join(path_to_screenshots, n)
		if os.path.isfile(f):
			img = cv2.imread(f'{path_to_screenshots}{n}')
			roi = img[660:860, 360:1440, :3]
			width = int(roi.shape[1]/9)
			for i in range(9):
				crop = roi[:, width*i:width*i+width, :]
				cv2.imwrite(f'{path_to_screenshots}/cropped/{n.partition(".")[0]}_{i}.png', crop)
		

if __name__ == '__main__':
	training_data_stats()
	#crop_champions_from_bench('./screenshot/')