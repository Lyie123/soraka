import cv2
from src.tft import Tft


def test_extract_s1():
    champions = ['TFT7_Leona', 'TFT7_Skarner', 'TFT7_Aatrox', 'TFT7_Heimerdinger', 'TFT7_Gnar']
    gold = '10'
    xp = '4'
    level = '3'
    streak = '1'
    progress_t1 = '2'
    progress_t2 = '2'
    

    img = cv2.imread('tests/screenshot/s1.png')

    tft = Tft()
    objects = tft.extract(img)

    print(objects)

    assert champions == objects['store']
    assert gold == objects['gold']
    #assert xp == objects['xp']
    assert level == objects['level']
    assert streak == objects['streak']
    assert progress_t1 == objects['progress']['t1']
    assert progress_t2 == objects['progress']['t2']
def test_extract_s2():
    champions = ['TFT7_Gnar', 'TFT7_Karma', 'TFT7_Nidalee', 'TFT7_Varus', 'TFT7_Ezreal']
    gold = '17'
    xp = '0'
    level = '4'
    streak = '2'
    progress_t1 = '2'
    progress_t2 = '3'

    img = cv2.imread('tests/screenshot/s2.png')

    tft = Tft()
    objects = tft.extract(img)

    print(objects)

    assert champions == objects['store']
    assert gold == objects['gold']
    #assert xp == objects['xp']
    assert level == objects['level']
    assert streak == objects['streak']
    assert progress_t1 == objects['progress']['t1']
    assert progress_t2 == objects['progress']['t2']
def test_extract_s3():
    champions = ['TFT7_Ashe', 'TFT7_Qiyana', 'TFT7_Elise', 'TFT7_TahmKench', 'TFT7_Ezreal']
    gold = '8'
    xp = '4'
    level = '5'
    streak = '3'
    progress_t1 = '2'
    progress_t2 = '5'

    img = cv2.imread('tests/screenshot/s3.png')

    tft = Tft()
    objects = tft.extract(img)

    print(objects)

    assert champions == objects['store']
    assert gold == objects['gold']
    #assert xp == objects['xp']
    assert level == objects['level']
    assert streak == objects['streak']
    assert progress_t1 == objects['progress']['t1']
    assert progress_t2 == objects['progress']['t2']
def test_extract_s4():
    champions = ['TFT7_Ashe', 'TFT7_Ezreal']
    gold = '2'
    xp = '4'
    level = '5'
    streak = '3'
    progress_t1 = '2'
    progress_t2 = '5'

    img = cv2.imread('tests/screenshot/s4.png')

    tft = Tft()
    objects = tft.extract(img)

    print(objects)

    assert champions == objects['store']
    assert gold == objects['gold']
    #assert xp == objects['xp']
    assert level == objects['level']
    assert streak == objects['streak']
    assert progress_t1 == objects['progress']['t1']
    assert progress_t2 == objects['progress']['t2']