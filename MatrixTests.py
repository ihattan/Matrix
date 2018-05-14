import Matrix

a = Matrix.Matrix([[1,1],[2,2]])
b = Matrix.Matrix([[1,2],[3,4]])

aPlusB = a.addition(b)
aMinusB = a.subtraction(b)
aScalar5 = a.scalarMul(5)
determinantA = a.determinant()
inverseB = b.inverse()

print 'a ='
print a
print 'b ='
print b
print 'a+b ='
print aPlusB
print 'a-b ='
print aMinusB
print '5*a ='
print aScalar5
print 'det(a) ='
print determinantA
print 'inv(b) ='
print inverseB

c = Matrix.Matrix([[1,2,3],[4,5,6]])

aTimesC = a.matrixMul(c)
transposeC = c.transpose()

print 'c ='
print c
print 'a * c ='
print aTimesC
print 'transpose(c) ='
print transposeC

d = Matrix.Matrix([[2,1,2],[4,3,1],[1,6,2]])

determinantD = d.determinant()

print 'd ='
print d
print 'det(d) ='
print determinantD
print 'uses the standard equation for 3x3 determinants'

e = Matrix.Matrix([[3,2,5,1,2,6],[2,7,4,1,3,4],[1,5,2,4,6,4],[1,0,0,1,1,1],[0,0,2,1,5,3],[0,0,2,1,0,5]])
determinantE = e.determinant()
inverseE = e.inverse()
id = inverseE.matrixMul(e)

print 'e ='
print e
print 'det(e) ='
print determinantE
print 'uses Gaussian Elimination'
print 'inv(e) ='
print inverseE
print 'also uses Gaussian Elimination'
print 'inverseE * e ='
print  id
