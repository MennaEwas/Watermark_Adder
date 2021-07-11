# Watermark Adder Using Pillow and Numpy

## Examples

1. Before<\br>
   ![rainbowTest](/rainbowTest.jpg)<\br>
   After in Intense mode<\br>
   ![rainbowTestIntense](/images/rainbowTestIntense.jpg)<\br>
   After in Normal mode<\br>
   ![rainbowTEstNormal](images/rainbowTestNormal.jpg)<\br>
2. Before<\br>
   ![solidTest](solidTest.png)<\br>
   After in Intense mode<\br>
   ![solidTestIntense](images/solidTestIntense.png)<\br>
   After in Normal mode<\br>
   ![solidTestNormal](images/solidTestNormal.png)<\br>

## How

This was done by creating a matrix with suitable size of the water mark that had the value 20 for its R G B values to lighten up when there would be a pixel of the water mark then adding this matrix to the original image in the needed parts.
for the places where adding 20 will cause the color value to overflow 255 it will be replaces with -40 to darken it instead.
