# Python Cross Stitch Patterns!
Takes a .jpg image file and generates a cross stitch pattern using a user specified number of DMC colours.

Prior to using this script you will need to install [Python Imaging Library - PIL](http://www.pythonware.com/products/pil/). 
Once installed, open up either terminal, or command prompt and then run the following command replacing the file path with a 
path to the folder containing the image you wish to convert.

    python "/pixelate.py" "/wave.jpg" 10 100
    
 So the first argument is the name of the file to convert, note this must be .jpg for the time being, the second is the 
 number of DMC colours to use the third is the stitch count.
 
 Example output below is the colour pattern file with symbols:

 ![Output Image](https://github.com/PaulMakesStuff/Python_Cross_Stitch/blob/master/col_sym.png)
