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
    trimmedMatrix =[]
    for row in matrix:
        if isUsefulRow:
            trimmedMatrix += [row[startPoint: endPoint]]
        elif not rowIsWhiteSpace(row):
            isUsefulRow = True
            startPoint, endPoint = extractEndPoints(row)
    return trimmedMatrix

def extractEndPoints(firstRow):
    """
    Extracts the dimensions of the matrix by utilizing the first row. This finds the first black spot and the last.

    :param firstRow: The first row with data.
    :return: A tuple of index of the first useful bit and the last useful bit.
    """
    wastedSpace = 0
    for num in firstRow:
        if num == 255:
            wastedSpace+=1
        else:
            break
    lastBlackIndex, count = wastedSpace, wastedSpace
    for num in firstRow[wastedSpace:]:
        if num == 0:
            lastBlackIndex = count
        count+=1
    return (wastedSpace, lastBlackIndex)


def rowIsWhiteSpace(row):
    """
    Returns a boolean of whether row is white space.

    :param row: A row of a matrix.
    :return: True if all white pixels, false otherwise.
    """
    for i in row:
        if i != 255:
            return False
    return True

def findRatio(matrix):
    """
    Finds and returns the ratio of the image to it's 1 pixel per black pixel equivalent.

    :param matrix: The QR equivalent matrix.
    :return: The scale of the matrix
    """

    for row in matrix:
        scale = 0
        for num in row:
            scale+=1
            if num == 255:
                return scale // 7
    return Exception

def scaleMatrix(matrix):
    """
    Scales the matrix to the smallest size possible

    :param matrix:
    :return:
    """
    ratio = findRatio(matrix)
    scaledMatrix = []
    yCount = 0
    for row in matrix:
        if yCount % ratio == 0:
            xCount = 0
            newRow = []
            for value in row:
                if xCount % ratio == 0:
                    newRow += [value]
                xCount+=1
            scaledMatrix += [newRow]
        yCount+=1
    return scaledMatrix



if __name__ == "__main__":
    matrix = numpy.asarray(Image.open("test.png").convert('L')).tolist()
    matrix = trimWhiteSpace(matrix)
    print(findRatio(matrix))
    matrix = scaleMatrix(matrix)
    print len(matrix)
    for i in (matrix):
        print(i)
