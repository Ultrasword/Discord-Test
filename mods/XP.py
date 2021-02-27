from PIL import Image, ImageDraw
from os import getcwd, path, remove

cwd = getcwd()

class Load_XP:
    def __init__(self, MAXXP, XP):
        self.barLen = int(XP / MAXXP * 180)
    
    def save_img(self):
        with Image.open(path.join(cwd, "images\\xp_bar.png")) as img:
            draw = ImageDraw.Draw(img)
            draw.rectangle([10,5,self.barLen,25],fill=(94,209,255),outline=None,width=1)
            img.save(path.join(cwd, "images\\temp.png"))
            img.close()

    def close(self):
        remove(path.join(cwd, "images\\temp.png"))
