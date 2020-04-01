# steganography-bin-gray
Python code that hides binary images inside gray-level images using LSB implementation.

```buildoutcfg
img1 --> path to image that hides or covers the img2.
img2 --> path to image that gets hidden inside img1.
```

## Usage

Then, merge and unmerge your files with:

```
python implementation.py merge --img1=res/img1.jpg --img2=res/img2.jpg --output=res/output.png
python implementation.py unmerge --img=res/output.png --output=res/output2.png
```

**Note**: the **output image** from the **merge operation** and the **input image** for the **unmerge operation** must be in **PNG** format.
