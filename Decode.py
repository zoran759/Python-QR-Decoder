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

if __name__ == "__main__":
    matrix = (numpy.asarray(Image.open("test.png").convert('L')).tolist())
    matrix = trimWhiteSpace(matrix)
    for i in (matrix):
        print(i)
    #print(trimWhiteRowSpace(matrix))
