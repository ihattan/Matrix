def dot(listA, listB):
    if not len(listA) == len(listB):
        print("invalid dot product dimension: {}*{}".format(len(listA), len(listB)))
        return 0
    return sum([listA[i]*listB[i] for i in range(len(listA))])

class Matrix:

    def __init__(self, matrix):
        self.rows = len(matrix)
        self.columns = len(matrix[0])
        self.matrix = matrix

    def identity(self):
        identity = []
        for i in range(self.rows):
            identity.append([])
            for j in range(self.columns):
                if i == j:
                    identity[i].append(1)
                else: identity[i].append(0)

        return Matrix(identity)

    def transpose(self):
        return Matrix([[self.matrix[j][i] for j in range(self.rows)] for i in range(self.columns)])

    def scalarMul(self, scalar):
        return Matrix([[self.matrix[i][j]*scalar for j in range(self.rows)]
                    for i in range(self.columns)])

    def addition(self, other):
        if not self.rows == other.rows or not self.columns == other.columns:
            print("invalid addition dimensions: {}x{} + {}x{}".format(self.rows, self.columns, other.rows, other.columns))
            return [[]]

        return Matrix([[self.matrix[i][j]+other.matrix[i][j] for j in range(self.columns)] for i in range(self.rows)])

    def subtraction(self, other):
        if not self.rows == other.rows or not self.columns == other.columns:
            print("invalid subtraction dimensions: {}x{} + {}x{}".format(self.rows, self.columns, other.rows, other.columns))
            return [[]]

        return Matrix([[self.matrix[i][j]-other.matrix[i][j] for j in range(self.columns)] for i in range(self.rows)])

    def matrixMul(self, other):
        if not self.columns == other.rows:
            print("invalid dimensions for matrix multiplication: {}x{} * {}x{}".format(self.rows, self.columns, other.rows, other.columns))
            return [[]]

        otherTranspose = other.transpose()

        return Matrix([[dot(self.matrix[i], otherTranspose.matrix[j])
                            for j in range(len(otherTranspose.matrix))]
                                for i in range(len(self.matrix))
                       ])

    def rowMul(self, row, scalar):
        self.matrix[row] = [self.matrix[row][i]*scalar for i in range(len(self.matrix[0]))]

    def rowSwitch(self, currentRow, otherRow):
        self.matrix[currentRow], self.matrix[otherRow] = self.matrix[otherRow], self.matrix[currentRow]

    def rowAdd(self, currentRow, otherRow, scalar=1):
        self.matrix[currentRow] = [self.matrix[currentRow][i] + (scalar*self.matrix[otherRow][i]) for i in range(len(self.matrix[0]))]

    def subMatrix(self, remRow, remCol):
        if remRow >= self.rows or remCol >= self.columns:
            print("invalid subMatrix dimensions: {}x{} remRow={}, remCol={}".format(self.rows, self.columns, remRow, remCol))
            return [[]]

        result = self.matrix[:remRow]+self.matrix[remRow+1:]
        for i in range(len(result)):
            result[i] = result[i][0:remCol]+result[i][remCol+1:]

        return Matrix(result)

    def determinant(self):
        if not self.rows == self.columns:
            print("invalid determinant dimensions: {}x{}".format(self.rows, self.columns))
            return 0

        if self.rows == 2:
            return (self.matrix[0][0]*self.matrix[1][1])-(self.matrix[0][1]*self.matrix[1][0])

        if self.rows > 6:
            return self.gaussDet()

        total = 0
        for i in range(self.rows):
            result = self.matrix[0][i]*(self.subMatrix(0, i)).determinant()
            if i%2 == 1:
                total -= result
            else: total += result

        return total

    def rowReduce(self, det):
        for i in range(self.rows-1):
            j = i+1
            while self.matrix[i][i] == 0 and not self.rows < j:
                if not self.matrix[j][i] == 0 and not self.matrix[i][j] == 0:
                    self.rowSwitch(i,j)
                    det *= -1
                j += 1
        return det

    def gaussDet(self):
        if not self.rows == self.columns:
            print("invalid gaussDet dimensions: {}x{}".format(self.rows, self.columns))
            return 0

        reducing = Matrix([[self.matrix[i][j] for j in range(self.columns)] for i in range(self.rows)])

        det = 1
        det = reducing.rowReduce(det)

        for i in range(reducing.rows):
            if reducing.matrix[i][i] == 0:
                return ([[]], 0)
            for j in range(i+1, reducing.columns):
                if not reducing.matrix[j][i] == 0:
                    reducing.rowAdd(j, i, (-reducing.matrix[j][i]/reducing.matrix[i][i]))
                    det = reducing.rowReduce(det)

        for i in range(reducing.rows):
            det *= reducing.matrix[i][i]

        return det

    def trace(self):
        if not self.rows == self.columns:
            print("invalid trace dimensions: {}x{}".format(self.rows, self.columns))
            return 0

        return sum([self.matrix[i][i] for i in range(self.rows)])

    def invRowReduce(self, identity):
        for i in range(self.rows-1):
            j = i+1
            while self.matrix[i][i] == 0 and not self.rows < j:
                if not self.matrix[j][i] == 0 and not self.matrix[i][j] == 0:
                    self.rowSwitch(i,j)
                    identity.rowSwitch(i, j)
                j += 1

        return identity

    def inverse(self):
        if not self.rows == self.columns:
            print("invalid inverse dimension: {}x{}".format(self.rows, self.columns))

        if self.rows == 2:
            det = self.determinant()
            if det == 0:
                print("matrix has no inverse, det == 0")
                return math.inf
            invdet = 1/det
            result = [[self.matrix[1][1],-self.matrix[0][1]],[self.matrix[1][0],self.matrix[0][0]]]
            return Matrix(result).scalarMul(invdet)

        reducing = Matrix([[self.matrix[i][j] for j in range(self.columns)] for i in range(self.rows)])
        identity = self.identity()
        identity = reducing.invRowReduce(identity)

        for i in range(reducing.rows):
            if reducing.matrix[i][i] == 0:
                print("matrix has no inverse, det == 0")
                return math.inf
            for j in range(i+1, reducing.columns):
                if not reducing.matrix[j][i] == 0:
                    identity.rowAdd(j, i, (-reducing.matrix[j][i]/reducing.matrix[i][i]))
                    reducing.rowAdd(j, i, (-reducing.matrix[j][i]/reducing.matrix[i][i]))
                    identity = reducing.invRowReduce(identity)
            identity.rowMul(i, 1/reducing.matrix[i][i])
            reducing.rowMul(i, 1/reducing.matrix[i][i])

        for i in range(reducing.rows):
            for j in range(i):
                if not reducing.matrix[j][i] == 0:
                    identity.rowAdd(j, i, (-reducing.matrix[j][i]/reducing.matrix[i][i]))
                    reducing.rowAdd(j, i, (-reducing.matrix[j][i]/reducing.matrix[i][i]))

        return identity

    def __str__(self):
        rep = '--\n'
        for row in self.matrix:
            for cell in row:
                rep += '|{: 06.3f}  '.format(cell)
            rep += '\n'
        return rep+'~~'
