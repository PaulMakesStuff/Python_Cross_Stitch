# Python Cross Stitch Patterns!
Takes a .jpg image file and generates a cross stitch pattern using a user specified number of DMC colours.

Prior to using this script you will need to install [Python Imaging Library - PIL](http://www.pythonware.com/products/pil/). 
Once installed, open up either terminal, or command prompt and then run the following command replacing the file path with a 
path to the folder containing the image you wish to convert.

    python "/pixelate.py" "/wave.jpg" 10 100
    
 So the first argument is the name of the file to convert, note this must be .jpg for the time being, the second is the 
 number of DMC colours to use the third is the stitch count.
 
 Example input image below:
 
 ![Input Image](https://github.com/PaulMakesStuff/Python_Cross_Stitch/blob/master/wave.jpg)
 
Example output image below. This pattern has a stitch count of 100, and uses 10 DMC colours. Other outputs from this script include a black and white pattern; a colour pattern with no symbols to get an idea of what the final cross stitch will look like; as well as a key so you'll know what DMC colours to purchase.

 ![Output Image](https://github.com/PaulMakesStuff/Python_Cross_Stitch/blob/master/col_sym.png)
 
 This package of files comes with a list of DMC colours, and their RGB values - this could be replaced with whatever thred you wish to use, for example Anchor. The nearest colour is picked based upon what DMC colour would look the closest, and is not simply done based upon how close the input RGB is to the DMC RGB.
