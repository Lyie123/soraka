import cv2
import numpy as np
from collections import defaultdict
from os import walk
from os.path import join, exists
from dataclasses import dataclass
from imutils.object_detection import non_max_suppression
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def create_training_set_from_screenshots():
    w = walk('screenshots')
    root, _, files = next(w)

    extractor = Extractor()
    for file in files:
        image = cv2.imread(join(root, file))
        objects = extractor.extract_all(image)
        for i, object in enumerate(objects):
            cv2.imwrite(f"training/champions/{file.partition('.')[0]}_object_{i}.png", object)

@dataclass
class TemplateMatch:
    match_type: str
    name: str
    precision: float
    x: int
    y: int

class Detector:
    def __init__(self):
        self.load_assets()

    def load_assets(self):
        w = walk('assets/templates')
        _, directories, _ = next(w)
        self._templates = defaultdict(list)

        for directory in directories:
            root, _, files = next(w)

            if exists(join(root, 'mask.png')):
                mask = cv2.imread(join(root, 'mask.png'))
                if mask is None:
                    print(f"{join(root, 'mask.png')} is no valid mask")

                mask = cv2.resize(mask, (187, 111), interpolation=cv2.INTER_AREA)
                mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

            for file in filter(lambda x: x not in('mask.png', 'TFT7_JadeStatue.png'), files):
                img = cv2.imread(join(root, file))
                img = cv2.resize(img, (187, 111), interpolation=cv2.INTER_AREA)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                self._templates[directory].append({
                    'name': file.partition('.')[0],
                    'image': img,
                    'mask': mask
                })
    def find_all(self, img, match=None):
        if match is None:
          match = self._templates.keys()
        
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        matches = []

        for match_type in [key for key in self._templates.keys() if key in match]:
            for template in self._templates[match_type]:
                (tH, tW) = template['image'].shape[:2]
                result = cv2.matchTemplate(img, template['image'], cv2.TM_CCORR_NORMED, mask=template['mask'])
                (y_coords, x_coords) = np.where((result >= 0.94) & (result != np.inf))

                rects = []
                for (x, y) in zip(x_coords, y_coords):
                    rects.append((x, y, x + tW, y + tH))

                pick = non_max_suppression(np.array(rects))
                for (startX, startY, endX, endY) in pick:
                    matches.append(TemplateMatch(match_type, template['name'], result[startY][startX], startX, startY))

        return matches
    def find_text(self, img: np.array, config=None):
        '''
        0    Orientation and script detection (OSD) only.
        1    Automatic page segmentation with OSD.
        2    Automatic page segmentation, but no OSD, or OCR.
        3    Fully automatic page segmentation, but no OSD. (Default)
        4    Assume a single column of text of variable sizes.
        5    Assume a single uniform block of vertically aligned text.
        6    Assume a single uniform block of text.
        7    Treat the image as a single text line.
        8    Treat the image as a single word.
        9    Treat the image as a single word in a circle.
        10    Treat the image as a single character.
        11    Sparse text. Find as much text as possible in no particular order.
        12    Sparse text with OSD.
        13    Raw line. Treat the image as a single text line,
        '''

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret,img = cv2.threshold(img, 115, 255, cv2.THRESH_BINARY)
        img = cv2.dilate(img, (5, 5), img)
        return pytesseract.image_to_string(img, config=config)


class Extractor:
    def __init__(self):
        self._detector = Detector()
    
    def extract_all(self, image):
        result = []
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        objects = self._detector.find_all(image_gray, match=['healthbar'])
        for object in objects:
            roi = image[object.y-15:object.y+150, object.x-48:object.x+135]
            if roi.shape[0] > 0 and roi.shape[1] > 0:
                result.append(roi)
        return result


if __name__ == '__main__':
    print('hello world')
