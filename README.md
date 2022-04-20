# Python Cross Stitch Patterns!
Takes an image file and generates a cross stitch pattern using a user specified number of DMC colors.

Prior to using this script you will need to install [Python Imaging Library - PIL](http://www.pythonware.com/products/pil/). 
Once installed, open up either terminal, or command prompt and then run the following command replacing the file path with a 
path to the folder containing the image you wish to convert.


```bash
$ ./pixelate.py --help
usage: pixelate.py [-h] [-c COLORS] [-s STITCHES] [-o OUTPUT] image

Convert image to cross stitch pattern

positional arguments:
  image                 Image to convert

options:
  -h, --help            show this help message and exit
  -c COLORS, --colors COLORS
                        Number of colors for the chart (default: 10)
  -s STITCHES, --stitches STITCHES
                        Number of stitches in X axis (default: 100)
  -o OUTPUT, --output OUTPUT
                        Output directory for files (default: current directory)
```

 Example:
 ```bash
 $ ./pixelate.py ./examples/wave.jpg -o examples
 ```

 Example input image below:
 
 ![Input Image](./examples/wave.jpg?raw=true)
 
Example output image below. This pattern has a stitch count of 100, and uses 10 DMC colors (default). Other outputs from this script include a black and white pattern; a color pattern with no symbols to get an idea of what the final cross stitch will look like; as well as a key so you'll know what DMC colors to purchase.

 ![Output Image](./examples/col_sym.png?raw=true)
 
 This package of files comes with a list of DMC colors, and their RGB values - this could be replaced with whatever thread you wish to use, for example Anchor. The nearest color is picked based upon what DMC color would look the closest, and is not simply done based upon how close the input RGB is to the DMC RGB.
