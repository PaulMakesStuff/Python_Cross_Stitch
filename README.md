## Image to Cross Stitch Pattern Converter

This Python script converts an input image into a cross-stitch pattern using DMC colors. It takes an image file as input, resizes it, quantizes the colors, and generates a pattern along with a color key for stitching.

### Usage
1. **Input File Selection:** Choose an image file (.jpg, .png, etc.).
2. **Number of Colours:** Specify the number of colors to be used in the pattern.
3. **Stitch Count:** Define the stitch count, i.e., the number of stitches in the x-axis.

### Dependencies
- Python 3.x
- PIL (Python Imaging Library)
- gooey

### Running the Script
Ensure all dependencies are installed, then execute the script with Python. The Gooey interface will guide you through the conversion process.

```bash
python pixelate.py
```

### Output
The script generates the following SVG files:

* col_sym.svg: Color with symbols pattern.
* blw_sym.svg: Black/white pattern with symbols.
* col_nsy.svg: Color-only pattern.
* key.svg: Color key for reference.

### Example input image below:

![Input Image](https://github.com/PaulMakesStuff/Python_Cross_Stitch/blob/master/wave.jpg)

Example output image below. This pattern has a stitch count of 100, and uses 10 DMC colours. Other outputs from this script include a black and white pattern; a colour pattern with no symbols to get an idea of what the final cross stitch will look like; as well as a key so you'll know what DMC colours to purchase.

![Output Image](https://github.com/PaulMakesStuff/Python_Cross_Stitch/blob/master/col_sym.png)

This package of files comes with a list of DMC colours, and their RGB values - this could be replaced with whatever thread you wish to use, for example Anchor. The nearest colour is picked based upon what DMC colour would look the closest, and is not simply done based upon how close the input RGB is to the DMC RGB.

### Note
This script uses adaptive quantization for color reduction to improve pattern quality. Adjusting the number of colors may affect the pattern's appearance and size.

