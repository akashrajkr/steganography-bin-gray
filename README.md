# steganography-bin-gray
Python code that hides binary images inside gray-level images using LSB implementation.

```buildoutcfg
img1 --> path to image that hides or covers the img2.
img2 --> path to image that gets hidden inside img1.
```

## Usage

Then, merge and unmerge your files with:

```
python3 implementation.py merge --gray=images/gray.jpg --bin=images/binary.jpg --output=output/encoded.png
python3 implementation.py unmerge --img=images/encoded.png --output=output/decoded.png
```

**Note**: the **output image** from the **merge operation** and the **input image** for the **unmerge operation** must be in **PNG** format.
