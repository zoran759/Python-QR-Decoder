import PIL, numpy
from PIL import Image

class QRMatrix:
    def __init__(self, image="", message=""):
        """
        Creates a QRMatrix object.
        :param image:
        :param message:
        :return:
        """
        if image is "" and message is "" or (not image is "" and not message is ""):
            raise Exception("You can only have an image or message. Not both or neither.")
        elif len(image) > 0:
            self.matrix = numpy.asarray(Image.open("test.png").convert('L')).tolist()
            self.__trimWhiteSpace()
            self.__scaleMatrix()      #May need to modify later if using real images.
        else:
            print("Matrix Maker has not been implemented yet")

    def __str__(self):
        """
        Creates an n x n matrix representation of the QRMatrix object
        :return: The String representation of a QRMatrix
        """
        for row in self.matrix:
            print [i if i!=255 else 1 for i in row]
        return ""
    
    def __trimWhiteSpace(self):
        """
        Removes every row that only contains white space. Once row with without white space is discovered,
        find the starting location of the black pixel and the last location of the black pixel. Use these variables
        to trim of remaining white space througout the image.

        :return: The matrix without trailing white pixels.
        """

        isUsefulRow = False
        trimmedMatrix =[]
        for row in self.matrix:
            if isUsefulRow:
                trimmedMatrix += [row[startPoint: endPoint]]
            elif not self.__rowIsWhiteSpace(row):
                isUsefulRow = True
                startPoint, endPoint = self.__extractEndPoints(row)
        self.matrix = trimmedMatrix

    def __extractEndPoints(self, firstRow):
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


    def __rowIsWhiteSpace(self, row):
        """
        Returns a boolean of whether row is white space.

        :param row: A row of a matrix.
        :return: True if all white pixels, false otherwise.
        """
        for i in row:
            if i != 255:
                return False
        return True

    def __findRatio(self, matrix):
        """
        Finds and returns the ratio of the image to it's 1 pixel per black pixel equivalent.
        TODO: REDO TO DO FINDER PATTERN. FIND THE NUMBER OF BLACK TO WHITE CHANGES

        :return: The scale of the matrix
        """

        for row in matrix:
            scale = 0
            for num in row:
                scale+=1
                if num == 255:
                    return scale // 7
        raise Exception

    def __scaleMatrix(self):
        """
        Scales the matrix to the smallest size possible

        :return:
        """
        ratio = self.__findRatio(self.matrix)
        scaledMatrix = []
        yCount = 0
        for row in self.matrix:
            if yCount % ratio == 0:
                xCount = 0
                newRow = []
                for value in row:
                    if xCount % ratio == 0:
                        newRow += [value]
                    xCount+=1
                scaledMatrix += [newRow]
            yCount+=1
        self.matrix = scaledMatrix



if __name__ == "__main__":
    test = QRMatrix("test.png")
    print(test)