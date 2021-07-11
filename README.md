# Watermark Adder Using Pillow and Numpy

## Examples

1. **Before**    
   ![rainbowTest](/rainbowTest.jpg)  
   **After in Intense mode**  
   ![rainbowTestIntense](/images/rainbowTestIntense.jpg)  
   **After in Normal mode**  
   ![rainbowTEstNormal](images/rainbowTestNormal.jpg)  
2. **Before**  
   ![solidTest](solidTest.png)  
   **After in Intense mode**  
   ![solidTestIntense](images/solidTestIntense.png)  
   **After in Normal mode**  
   ![solidTestNormal](images/solidTestNormal.png)  

## How

This was done by creating a matrix with suitable size of the water mark that had the value 20 for its R G B values to lighten up when there would be a pixel of the water mark then adding this matrix to the original image in the needed parts.
for the places where adding 20 will cause the color value to overflow 255 it will be replaces with -40 to darken it instead.
