'''
Same but with OOP
'''
from PIL import Image, ImageDraw, ImageFont
from numpy import array, bitwise_xor, asarray
import os

class IM:
    def __init__(self, path):
        self.path = path
        self.text = 'MennaHC'
                     
        
    def load_img(self):
        self.img = Image.open(self.path).convert('RGB')
        self.num_img = array(self.img)  #array 
        self.w, self.h = self.img.size 
        
    def design_pattern(self):
        n = self.h//7
        self.text = self.text * n 
        img2 = Image.new('RGB',self.img.size,(0,0,0,0))
        d = ImageDraw.Draw(img2)
        font = ImageFont.truetype('arial.ttf', self.h*self.w//500)
        #initial coordination
        x = 0
        y = 0 
        k = self.w//100
        for i in range(k):
            d.text((x,y), self.text, fill= (90,90,90), font = font) #now it is img complemtary colour
            self.num2_img = asarray(img2)
            y += 100
            
    def out(self):
        self.out_num = self.num_img & ~(self.num2_img)
        new_img = Image.fromarray(self.out_num, 'RGB')
        new_img.show()

        
    def execute(self):
        self.load_img()
        self.design_pattern()
        self.out()
        
        
        
if __name__ == "__main__":
    p = IM(r"D:\curri\sixth\Self\Markwater\hn.png") 
    p.execute()
    
    
    