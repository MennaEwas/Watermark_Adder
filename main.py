import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os


class WatermarkAdder:
    def __init__(self, imageDir: str, watermark: str, watermarkMode: str = "N", sameLocation: bool = False):
        """
        Adding String watermarks to images and saves them in the same directory with a changed name or
        a new images folder created in the same directory

        :param imageDir: image directory
        :param watermark: watermark string to be added
        :param watermarkMode: string indicator for Normal mode or Intense mode
        :param sameLocation: bool to chose save location mode
        """
        self.__imageDir = imageDir
        self.__image = self.__load_image(imageDir)
        self.__watermark = self.__make_watermark_array(watermark)
        self.__mode = watermarkMode
        self.__locationMode = sameLocation

    @staticmethod
    def __load_image(imageDir):
        """
        loads the image using PIL and converts it to a numpy array

        :param imageDir: image directory
        :return: numpy array of the image
        """
        img = Image.open(imageDir).convert('RGB')
        # loads the right orientation from the exif tag
        img = ImageOps.exif_transpose(img)
        imgArray = np.array(img)
        return imgArray

    def __make_watermark_array(self, watermark: str) -> np.core._multiarray_umath.ndarray:
        """
        creates the image array of the string in suitable dimensions according to the images resolution
        using PIL draw function to create an image with the string on it then using that as a mask

        :param watermark: watermark string
        :return: numpy array of the watermark
        """
        # defining the font size dynamically to fit every resolution
        fntSize = self.__image.shape[0] // 20
        # creating an empty black image that is bigger or equal in width to the string that will be added to it
        tempImg = Image.new("RGB", (fntSize * len(watermark), fntSize))
        fnt = ImageFont.truetype("arial.ttf", size=fntSize)
        d = ImageDraw.Draw(tempImg)
        # adds the string to the temp image
        d.text((0, 0), watermark, font=fnt)
        # getting the exact shape of the string on the temp image
        ns = d.textsize(watermark, font=fnt)
        # creating a numpy array that is the size of the temp image and full with 20 as it is R G B values
        temp = np.full((fntSize, fntSize * len(watermark), 3), 20, dtype=int)
        # creating a mask to only leave 20 where the string would be on the temp image
        new = np.ma.masked_array(temp, mask=np.logical_not(tempImg))
        # slicing the array to only leave the string without any extras
        new = new.filled(0)[0:ns[1], 0:ns[0]]
        return new

    @staticmethod
    def __create_mask(img, temp):
        """
        creates a numpy mask of the values that get over 255 and fill their places with -40

        :param img: numpy image array
        :param temp: numpy image array
        :return: numpy masked array
        """
        tmpMask = np.ma.masked_less_equal(temp, 255).filled(0)
        mask = np.ma.masked_array(img, mask=tmpMask, dtype=int)
        mask = mask.filled(-40)
        mask = np.ma.masked_array(mask, mask=np.logical_not(tmpMask)).filled(0)
        return mask

    def __save(self, img: Image.Image):
        """
        saves the new image in the desired directory

        :param img: PIL image
        """
        if not self.__locationMode:
            try:
                img.save("images\\" + self.__imageDir)
            except FileNotFoundError:
                os.mkdir(os.path.dirname(os.path.realpath(__file__)) + "\images")
                img.save("images\\" + self.__imageDir)
        else:
            temp = self.__imageDir.split(".")
            extension = temp[-1]
            newDir = "".join(temp[:-1]) + " Watermarked." + extension
            img.save(newDir)

    def add_watermark(self):
        """
        adds the watermark image array to the original image either in a grid (Normal mode) or over the whole
        image (Intense mode)
        """
        w, h, n = self.__watermark.shape
        ow, oh, n = self.__image.shape
        # centralizing the watermark grid
        horizontalShift = (oh % h) // 2
        verticalShift = (ow % w) // 2
        nw = ow // w
        nh = oh // h
        skipRP = -1
        skipCP = -1
        for i in range(nw):
            for j in range(nh):
                if skipCP < 0 or self.__mode == "I":
                    # adding the watermark numpy array to part of the image to make the needed pixel lighter
                    temp = np.add(self.__image[verticalShift + w * i:verticalShift + w * i + w,
                                  horizontalShift + h * j:horizontalShift + h * j + h], self.__watermark)
                    # creating the mask to remove any above 255 color values to make them darker insted of lighter
                    mask = self.__create_mask(self.__image[verticalShift + w * i:verticalShift + w * i + w,
                                              horizontalShift + h * j:horizontalShift + h * j + h], temp)
                    # adding the maks and the temp to change all the needed pixels in the right way
                    self.__image[verticalShift + w * i:verticalShift + w * i + w,
                                 horizontalShift + h * j:horizontalShift + h * j + h] = np.add(temp, mask)
                skipCP *= -1
            if skipRP < 0:
                skipCP = 1
            else:
                skipCP = -1
            skipRP *= -1
        img = Image.fromarray(self.__image)
        self.__save(img)


adder = WatermarkAdder("rainbowTest.jpg", "FAdy200", "N", True)
adder.add_watermark()
