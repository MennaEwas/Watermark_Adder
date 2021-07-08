import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os


class WatermarkAdder:
    def __init__(self, imageDir, watermark, watermarkMode="N"):
        self.__imageDir = imageDir
        self.__image = self.__load_image(imageDir)
        self.__watermark = self.__make_watermark_matrix(watermark)
        self.__mode = watermarkMode

    @staticmethod
    def __load_image(imageDir):
        img = Image.open(imageDir).convert('RGB')
        img = ImageOps.exif_transpose(img)
        imgArray = np.array(img)
        return imgArray

    def __make_watermark_matrix(self, watermark):
        fntSize = self.__image.shape[0] // 20
        tempImg = Image.new("RGB", (fntSize * len(watermark), fntSize))
        fnt = ImageFont.truetype("arial.ttf", size=fntSize)
        d = ImageDraw.Draw(tempImg)
        d.text((0, 0), watermark, font=fnt)
        ns = d.textsize(watermark, font=fnt)
        # tempImg.save('no.png')
        temp = [[[+20, +20, +20]] * (fntSize * len(watermark))] * fntSize
        temp = np.array(temp)
        new = np.ma.masked_array(temp, mask=np.logical_not(tempImg))
        new = new.filled(0)[0:ns[1], 0:ns[0]]
        return new

    @staticmethod
    def __create_mask(img, temp):
        tmpMask = np.ma.masked_less_equal(temp, 255).filled(0)
        mask = np.ma.masked_array(img, mask=tmpMask, dtype=int)
        mask = mask.filled(-40)
        mask = np.ma.masked_array(mask, mask=np.logical_not(tmpMask)).filled(0)
        return mask

    def add_watermark(self):
        w, h, n = self.__watermark.shape
        ow, oh, n = self.__image.shape
        horizontalShift = (oh % h) // 2
        verticalShift = (ow % w) // 2
        nw = ow // w
        nh = oh // h
        skipR = -1
        skipC = -1
        for i in range(nw):
            for j in range(nh):
                if skipC < 0 or self.__mode == "I":
                    temp = np.add(self.__image[verticalShift + w * i:verticalShift + w * i + w,
                                  horizontalShift + h * j:horizontalShift + h * j + h], self.__watermark)
                    mask = self.__create_mask(self.__image[verticalShift + w * i:verticalShift + w * i + w,
                                                           horizontalShift + h * j:horizontalShift + h * j + h], temp)
                    self.__image[verticalShift + w * i:verticalShift + w * i + w,
                                 horizontalShift + h * j:horizontalShift + h * j + h] = np.add(temp, mask)
                skipC *= -1
            if skipR < 0:
                skipC = 1
            else:
                skipC = -1
            skipR *= -1
        img = Image.fromarray(self.__image)
        try:
            img.save("images\\" + self.__imageDir)
        except FileNotFoundError:
            os.mkdir(os.path.dirname(os.path.realpath(__file__)) + "\images")
            img.save("images\\" + self.__imageDir)


adder = WatermarkAdder("rainbowTest.jpg", "FAdy200", "N")
adder.add_watermark()
