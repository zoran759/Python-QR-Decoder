import PIL, numpy, sys, operator
from PIL import Image


class QRMatrix:
    """
    The QRMatrix Class that will allow users to encode and decode QR Codes.
    """

    def __init__(self, image="", message=""):
        """
        Creates a QRMatrix object. Only one parameter (image or message) can bbe filled. It's from that
        where this code will decide whether to encode or decode. If an image path is insterted, it will
        decode the image. Otherwise it will encode.

        When decoding, it begins by using numpy to convert the image in binary ndary array. 0 will refer
        to black pixels and 255 will refer to white pixels. Afterwards, it is converted into a list of lists where
        white space is then trimmed and the matrix is then scaled.
        :param image: The path to the image.
        :param message: The message to be encoded.
        :return:
        """
        if not bool(image) ^ bool(message):
            raise Exception("You can only have an image or message. Not both or neither.")
        elif len(image) > 0:
            self.matrix = numpy.asarray(Image.open(image).convert('L')).tolist()
            self.__trimWhiteSpace()
            self.__scaleMatrix()  # May need to modify later if using real images.
        else:
            print("Matrix Maker has not been implemented yet")

    def __str__(self):
        """
        Creates an n x n matrix representation of the QRMatrix object. For this representation, 255 will become 1.
        :return: The String representation of a QRMatrix.
        """
        for row in self.matrix:
            print [i if i != 255 else 1 for i in row]
        return ""



    def out_of_bounds(self, x ,y):
        if x > len(self.matrix) - 1 or y > len(self.matrix) - 1:
            return 1 #move downward
        elif x < 0 or y < 0:
            return 1 #not possible
        elif x < 9 and (y < 9 or y >= len(self.matrix) - 8):
            return 1
        elif x < 9 and y >= len(self.matrix) - 8:
            return 1
        else:
            return False

    def decode(self):
        list = self.traverse_matrix()
        factor = 128
        word = ""
        character = 0
        self.type = self.decode_bits(list, 0 , 4)
        self.length = self.decode_bits(list, 4)
        print(self.length)
        for i in range(self.length):
            word+=chr(self.decode_bits(list, 12 + i*8))


        # for i in list[12:]:
        #     character += i * factor
        #     if factor == 1:
        #         word+=chr(character)
        #         factor = 256
        #         character = 0
        #     factor/=2
        return word

    def in_fixed_area(self, x, y):
        if x in range(len(self.matrix) - 10 + 1,len(self.matrix) - 5 +1) and y in range(len(self.matrix) - 10 + 1,len(self.matrix) - 5 + 1):
            return True
        elif x == 6 or y == 6:
            return True

    def decode_bits(self, matrix, start, number_of_bits=8):
        factor = 2 << (number_of_bits - 2)
        character = 0
        for i in matrix[start:start+number_of_bits]:
            character += i * factor
            if factor == 1:
                print(chr(character))
                return character
            factor/=2

    def traverse_matrix(self):
        """

        :return:
        """
        representation = []
        x, y, direction = len(self.matrix)-1, len(self.matrix)-1, -1
        matrix = self.demask()
        while True:
            if self.out_of_bounds(x,y):
                direction,y,x = -direction,y-2,x-direction
            if not self.in_fixed_area(x,y):
                representation+= [matrix[x][y]]
            if x == 0 and y ==10:
                break
            elif y%2!=0:
                x,y = x+direction, y+1
            else:
                y-=1
        return representation


    def demask(self):
        """
        Removes the mask on the QR Matrix. This creates a matrix that has 1 represent black spots and 0 represent
        white spots, the oppisite of the normal matrix. Also accounts for skipped row and column.

        :return: The unmasked QR Code
        """
        mask = self.extractMaskPattern()
        decodedMatrix = []
        y = 0
        while y < len(self.matrix):
            row = []
            x = 0
            while x < len(self.matrix[0]):
                modifyValue = self.matrix[y][x]
                if (modifyValue == 255):
                    modifyValue = 1
                row += [(~modifyValue + 2 ^ ~mask[y][x] + 2)]
                x += 1
            decodedMatrix += [row]
            y += 1
        return decodedMatrix

    def encode(self):
        """
        Encodes the matrix.
        :return:
        """

        return

    def extractMaskPattern(self):
        """
        Find the mask pattern in the QR Code and returns the bit array representation of it. Remember that 255 is used
        to represent white and 0 is used to represet black. These 3 bits will correspond with a power of 2 to create
        a unique value. This will then be used to create a mask patter to decode things. Remember that row and column
        7 must be skipped because they are special. Last part needed to adjust for shift.

        :return: The mask pattern created.
        """

        maskPattern = self.matrix[8][2:5]
        power = 1
        total = 0
        for i in maskPattern:
            if i == 0:
                total += power
            power <<= 1

        maskMatrix = []
        j = 0
        for row in self.matrix:
            i = 0
            newRow = []
            for val in self.matrix[j]:
                if self.extractMaskNumberBoolean(total, i, j):
                    newRow += [0]
                else:
                    newRow += [1]
                i += 1
            j += 1
            maskMatrix += [newRow]
        return maskMatrix

    def extractMaskNumberBoolean(self, number, j, i):
        """
        The forumlas were copied inversely so the operands have been reversed in this function. This function
        returns a boolean that matches a certain pattern

        :param number: The mask pattern number.
        :param i: The x position.
        :param j: The y position.
        :return: The boolean of whether or not a spot should be inverted.
        """
        if number == 1:
            return i % 2 == 0
        elif number == 2:
            return ((i * j) % 3 + i + j) % 2 == 0
        elif number == 3:
            return (i + j) % 3 == 0
        elif number == 4:
            return (i / 2 + j / 3) % 2 == 0
        elif number == 5:
            return (i + j) % 2 == 0
        elif number == 6:
            return ((i * j) % 3 + i * j) % 2 == 0
        elif number == 7:
            return j % 3 == 0

    def __trimWhiteSpace(self):
        """
        Removes every row that only contains white space. Once row with without white space is discovered,
        find the starting location of the black pixel and the last location of the black pixel. Use these variables
        to trim of remaining white space througout the image.

        :return: The matrix without trailing white pixels.
        """

        isUsefulRow = False
        trimmedMatrix = []
        startPoint, endPoint = 0, 0
        for row in self.matrix:
            if isUsefulRow:
                if len(trimmedMatrix) == endPoint - startPoint:
                    break
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
                wastedSpace += 1
            else:
                break
        lastBlackIndex, count = wastedSpace, wastedSpace
        for num in firstRow[wastedSpace:]:
            if num == 0:
                lastBlackIndex = count
            count += 1
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

        :return: The scale of the matrix
        """
        # TODO: Use Finder Pattern Method

        for row in matrix:
            scale = 0
            for num in row:
                scale += 1
                if num == 255:
                    return scale // 7
        raise Exception("This image is not binary!")

    def __scaleMatrix(self):
        """
        Scales the matrix to the smallest size possible

        :return: Nothing
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
                    xCount += 1
                scaledMatrix += [newRow]
            yCount += 1
        self.matrix = scaledMatrix

    def __find_usable_space(self):
        """

        :return:
        """
        return len(self.matrix) - 7 - 2

    def test(self):
        numeric_matrix = QRMatrix("samples/test.png")
        top = [1, 2, 3, 4, 5]
        mid = [6, 7, 8, 9, 10]
        mid2 = [11,12,13,14,15]
        mid3=[16,17,18,19,20]
        bot = [21,22,23,24,25]
        matrix = [top, mid,mid2,mid3, bot]
        return numeric_matrix.traverse_matrix(matrix) == [9,6,3,2,5,8,7,4,1]

if __name__ == "__main__":
    if str(sys.argv[1]) == "decode" or sys.argv[1] == "encode":
        QRCode = QRMatrix(sys.argv[2])
        for i in (QRCode.demask()):
            print(i)
        # QRCode.traverse_matrix()

        print(QRCode.decode())
        # for i in QRCode.demask():
        #     print(i)
        # print(len(QRCode.matrix))
        # import doctest
        # doctest.testmod()
        #print(QRCode.test())

