import PIL, numpy
from PIL import Image


def trimWhiteSpace(matrix):
    """
    Removes every row that only contains white space. Once row with without white space is discovered,
    find the starting location of the black pixel and the last location of the black pixel. Use these variables
    to trim of remaining white space througout the image.

    :param matrix: The matrix that contains trailing white pixels.
    :return: The matrix without trailing white pixels.
    """
    isUsefulRow = False
    qrSide = 0
    trimmedMatrix =[]
    for row in matrix:
        if isUsefulRow:
            #process
        elif not rowIsWhiteSpace(row):
            isUsefulRow = True
            #process the row



def rowIsWhiteSpace(row):
    for i in row:
        if i != 255:
            return False
    return True

if __name__ == "__main__":
    numpy.set_printoptions(threshold=numpy.nan)
    matrix = (numpy.asarray(Image.open("test.png").convert('L')).tolist())

    for i in (matrix):
        print(i)
    #print(trimWhiteRowSpace(matrix))
