import click
import cv2
import matplotlib.pyplot  as plt
import numpy as np
import sys


class Steganography(object):
    @staticmethod
    def imshow(img, title='image'):
        plt.axis("off")
        plt.title(title)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()

    @staticmethod
    def merge(img1, img2):
        global grayimg, binimg
        """Merge two images. The second one will be merged into the first one.
        :param img1: First image
        :param img2: Second image
        :return: A new merged image.
        """
        # Reading image
        print('Reading images...')
        grayimg = cv2.imread(img1)
        binimg = cv2.imread(img2)
        if (type(grayimg) is not np.ndarray) or (type(binimg) is not np.ndarray) :
            print('Entered path is not right or something went wrong. Can\'t read image.')
            sys.exit()


        if binimg.shape[0] > grayimg.shape[0] or binimg.shape[1] > grayimg.shape[1]:
            # raise ValueError('Image 2 should not be larger than Image 1!')
            print('Binary image found larger than grayscale image.\nResizing binary image to fit inside gray image...')
            binimg = cv2.resize(binimg, (grayimg.shape[0], grayimg.shape[1]), cv2.INTER_AREA)

        # Checking for outlier pixel values in binary image
        for x in range(0, binimg.shape[0]):
            for y in range(0, binimg.shape[1]):
                val = binimg[x, y][0]
                if val >= 128:
                    val = 255
                else:
                    val = 0
                binimg[x, y] = [val for _ in range(3)]

        # Encoding...
        print('Encoding images...')
        for x in range(0, grayimg.shape[0]):
            for y in range(0, grayimg.shape[1]):
                if not (x >= binimg.shape[0] or y >= binimg.shape[1]):
                    if binimg[x, y, 0] < 128:
                        if not grayimg[x, y, 0] % 2 == 0:
                            grayimg[x, y] = [(grayimg[x, y][0] + 1) for _ in range(3)]
                    elif binimg[x, y, 0] > 128:
                        if not grayimg[x, y, 0] % 2 == 1:
                            grayimg[x, y] = [(grayimg[x, y][0] + 1) for _ in range(3)]
                else:
                    if not grayimg[x, y, 0] % 2 == 0:
                        grayimg[x, y] = [(grayimg[x, y][0] + 1) for _ in range(3)]
        print('Done encoding.')
        Steganography.imshow(grayimg, 'Encoded image')
        return grayimg

    @staticmethod
    def unmerge(img):
        """Unmerge an image.
        :param img: The input image.
        :param output: The output path
        """
        print('Reading grayscale cover image...')
        grayimg = cv2.imread(img)
        if  type(grayimg) is not np.ndarray:
            print('Entered path is not right or something went wrong. Can\'t read image.')
            sys.exit()

        # Decoding..
        print('Extracting binary image...')
        final_img = np.zeros((grayimg.shape[0], grayimg.shape[1], 3), np.uint8)
        original_size = (grayimg.shape[0], grayimg.shape[1])
        for x in range(0, grayimg.shape[0]):
            for y in range(0, grayimg.shape[1]):
                if grayimg[x, y, 0] % 2 == 1:
                    final_img[x, y] = [255 for _ in range(3)]
                if not final_img[x, y, 0] == 0:
                    original_size = (x+1, y+1)
        final_img = final_img[0:original_size[0], 0:original_size[1]]
        print('Done extracting.')
        Steganography.imshow(final_img, 'Decoded image')
        return final_img
        # print(original_size)

@click.group()
def cli():
    pass


@cli.command()
@click.option('--img1', required=True, type=str, help='Grayscale image that will hide another image')
@click.option('--img2', required=True, type=str, help='Binary image that will be hidden')
@click.option('--output', required=True, type=str, help='Output image')
def merge(img1, img2, output):
    merged_image = Steganography.merge(img1, img2)
    cv2.imwrite(output,merged_image)
    print('Encoded image saved in', output)

@cli.command()
@click.option('--img', required=True, type=str, help='Image that will be hidden')
@click.option('--output', required=True, type=str, help='Output extracted binary image')
def unmerge(img, output):
    unmerged_image = Steganography.unmerge(img)
    cv2.imwrite(output, unmerged_image)
    print('Extracted image saved in', output)

if __name__ == '__main__':
    cli()
