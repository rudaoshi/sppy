import logging
import sys
import unittest
import numpy
import numpy.testing as nptst 
import math 


from sparray.dyn_array import dyn_array 

class dyn_arrayTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        self.A = dyn_array((5, 5))

        nrow = 5 
        ncol = 7
        self.B = dyn_array((nrow, ncol))
        self.B[0, 1] = 1
        self.B[1, 3] = 5.2
        self.B[3, 3] = -0.2
        self.B[0, 6] = -1.23
        self.B[4, 4] = 12.2        
        
        nrow = 100 
        ncol = 100
        self.C = dyn_array((nrow, ncol))
        self.C[0, 1] = 1
        self.C[10, 3] = 5.2
        self.C[30, 34] = -0.2
        self.C[0, 62] = -1.23
        self.C[4, 41] = 12.2      
        
    def testInit(self): 
        A = dyn_array((5, 7))
        self.assertEquals(A.shape, (5, 7))
        
        A = dyn_array((1, 1))
        self.assertEquals(A.shape, (1, 1))
        
        A = dyn_array((1, 0))
        self.assertEquals(A.shape, (1, 0))
        
        A = dyn_array((0, 0))
        self.assertEquals(A.shape, (0, 0))
        
        #Test bad input params 
        self.assertRaises(IndexError, dyn_array, (0,))
        self.assertRaises(TypeError, dyn_array, 0)
        
        #TODO: Test other dtypes 
        A = dyn_array((5, 5))
        self.assertEquals(A.dtype, numpy.float)
        
        
    def testNDim(self): 
        A = dyn_array((5, 7))
        self.assertEquals(A.ndim, 2)
        
        A = dyn_array((0, 0))
        self.assertEquals(A.ndim, 2)
    
    def testSize(self): 
        self.assertEquals(self.A.size, 25)
        self.assertEquals(self.B.size, 35)
        self.assertEquals(self.C.size, 10000)
        
    def testGetnnz(self): 
       A = dyn_array((5, 7))
       self.assertEquals(A.getnnz(), 0)
       A[0, 0] = 1.0
       
       self.assertEquals(A.getnnz(), 1)
       
       A[2, 1] = 1.0
       self.assertEquals(A.getnnz(), 2)
       
       A[2, 5] = 1.0
       A[3, 5] = 1.0
       self.assertEquals(A.getnnz(), 4)
       
       #If we insert a zero it is not registered as zero 
       A[4, 4] = 0.0
       self.assertEquals(A.getnnz(), 4)
       
       #But erasing an item keeps it (can call prune)
       A[3, 5] = 0.0
       self.assertEquals(A.getnnz(), 4)
       
       B = dyn_array((5, 7))
       B[(numpy.array([1, 2, 3]), numpy.array([4, 5, 6]))] = 1
       self.assertEquals(B.getnnz(), 3)
       
       for i in range(5): 
           for j in range(7): 
               B[i, j] = 1
               
       self.assertEquals(B.getnnz(), 35)
       
       self.assertEquals(self.A.getnnz(), 0)
       self.assertEquals(self.B.getnnz(), 5)
       self.assertEquals(self.C.getnnz(), 5)
    
    def testSetItem(self):
        nrow = 5 
        ncol = 7
        A = dyn_array((nrow, ncol))
        A[0, 1] = 1
        A[1, 3] = 5.2
        A[3, 3] = -0.2
        
        self.assertEquals(A[0, 1], 1)
        self.assertAlmostEquals(A[1, 3], 5.2)
        self.assertAlmostEquals(A[3, 3], -0.2)
        
        for i in range(nrow): 
            for j in range(ncol): 
                if (i, j) != (0, 1) and (i, j) != (1, 3) and (i, j) != (3, 3): 
                    self.assertEquals(A[i, j], 0)
        
        self.assertRaises(ValueError, A.__setitem__, (20, 1), 1)  
        self.assertRaises(TypeError, A.__setitem__, (1, 1), "a")   
        self.assertRaises(ValueError, A.__setitem__, (1, 100), 1)   
        self.assertRaises(ValueError, A.__setitem__, (-1, 1), 1)   
        self.assertRaises(ValueError, A.__setitem__, (0, -1), 1) 
        
        result = A[(numpy.array([0, 1, 3]), numpy.array([1, 3, 3]))] 
        self.assertEquals(result[0], 1)
        self.assertEquals(result[1], 5.2)
        self.assertEquals(result[2], -0.2)
        
        #Replace value of A 
        A[0, 1] = 2
        self.assertEquals(A[0, 1], 2)
        self.assertAlmostEquals(A[1, 3], 5.2)
        self.assertAlmostEquals(A[3, 3], -0.2)
        
        for i in range(nrow): 
            for j in range(ncol): 
                if (i, j) != (0, 1) and (i, j) != (1, 3) and (i, j) != (3, 3): 
                    self.assertEquals(A[i, j], 0)
       
       
    def testStr(self): 
        nrow = 5 
        ncol = 7
        A = dyn_array((nrow, ncol))
        A[0, 1] = 1
        A[1, 3] = 5.2
        A[3, 3] = -0.2
        
        outputStr = "dyn_array shape:(5, 7) non-zeros:3\n" 
        outputStr += "(0, 1) 1.0\n"
        outputStr += "(1, 3) 5.2\n"
        outputStr += "(3, 3) -0.2\n"
        self.assertEquals(str(A), outputStr) 
        
        B = dyn_array((5, 5))
        outputStr = "dyn_array shape:(5, 5) non-zeros:0\n" 
        self.assertEquals(str(B), outputStr) 

    def testSum(self): 
        nrow = 5 
        ncol = 7
        A = dyn_array((nrow, ncol))
        A[0, 1] = 1
        A[1, 3] = 5.2
        A[3, 3] = -0.2
        
        self.assertEquals(A.sum(), 6.0)
        
        A[3, 4] = -1.2
        self.assertEquals(A.sum(), 4.8)
        
        A[0, 0] = 1.34
        self.assertEquals(A.sum(), 6.14)
        
        A[0, 0] = 0 
        self.assertEquals(A.sum(), 4.8)
        
        self.assertEquals(self.A.sum(), 0.0)
        self.assertEquals(self.B.sum(), 16.97)
        self.assertEquals(self.C.sum(), 16.97)

    def testGet(self): 
        self.assertEquals(self.B[0, 1], 1)
        self.assertEquals(self.B[1, 3], 5.2)
        self.assertEquals(self.B[3, 3], -0.2)
        self.assertEquals(self.B.getnnz(), 5)
        
        #Test negative indices 
        self.assertEquals(self.B[-5, -6], 1)
        self.assertEquals(self.B[-1, -3], 12.2)
        
        self.assertRaises(ValueError, self.B.__getitem__, (20, 1))  
        self.assertRaises(ValueError, self.B.__getitem__, (1, 20))  
        self.assertRaises(ValueError, self.B.__getitem__, (-6, 1))  
        self.assertRaises(ValueError, self.B.__getitem__, (1, -8))  
        self.assertRaises(TypeError, self.B.__getitem__, (1))
        self.assertRaises(ValueError, self.B.__getitem__, "a")
        self.assertRaises(ValueError, self.B.__getitem__, ("a", "c"))
        
        #Test array indexing using arrays  
        C = self.B[numpy.array([0, 1, 3]), numpy.array([1, 3, 3])]
        self.assertEquals(C.shape[0], 3)
        self.assertEquals(C[0], 1)
        self.assertEquals(C[1], 5.2)
        self.assertEquals(C[2], -0.2)
        
        C = self.A[numpy.array([0, 1, 3]), numpy.array([1, 3, 3])]
        self.assertEquals(C[0], 0)
        self.assertEquals(C[1], 0)
        self.assertEquals(C[2], 0)
        
        A = dyn_array((2, 2))
        self.assertRaises(ValueError, A.__getitem__, (numpy.array([0, 1]), numpy.array([1, 3])))
        
        A = dyn_array((2, 2))
        self.assertRaises(ValueError, A.__getitem__, (numpy.array([0, 2]), numpy.array([1, 1])))
        
        A = dyn_array((0, 0))
        self.assertRaises(ValueError, A.__getitem__, (numpy.array([0, 1, 3]), numpy.array([1, 3, 3])))
        
        
        #Test submatrix indexing 
        C = self.B[:, :]
        
        for i in range(C.shape[0]): 
            for j in range(C.shape[1]): 
                C[i, j] = self.B[i, j]
                
        C = self.B[0:5, 0:7]
        
        for i in range(C.shape[0]): 
            for j in range(C.shape[1]): 
                C[i, j] = self.B[i, j]
        
        C = self.B[numpy.array([0, 1, 3]), :]
        self.assertEquals(C.shape, (3, 7))
        self.assertEquals(C.getnnz(), 4)
        self.assertEquals(C[0, 1], 1)
        self.assertEquals(C[1, 3], 5.2)
        self.assertEquals(C[2, 3], -0.2)
        self.assertEquals(C[0, 6], -1.23)
        
        C = self.B[numpy.array([0, 1, 3]), 0:7]
        self.assertEquals(C.shape, (3, 7))
        self.assertEquals(C.getnnz(), 4)
        self.assertEquals(C[0, 1], 1)
        self.assertEquals(C[1, 3], 5.2)
        self.assertEquals(C[2, 3], -0.2)
        self.assertEquals(C[0, 6], -1.23)
        
        C = self.B[:, numpy.array([3])]
        self.assertEquals(C.shape, (5, 1))
        self.assertEquals(C.getnnz(), 2)
        self.assertEquals(C[1, 0], 5.2)
        self.assertEquals(C[3, 0], -0.2)
                
    def testSubArray(self): 
        rowInds = numpy.array([0, 1], numpy.int)
        colInds = numpy.array([1, 3, 6], numpy.int)
        A = self.B.subArray(rowInds, colInds)
        
        for i in range(A.shape[0]): 
            for j in range(A.shape[1]): 
                self.assertEquals(A[i, j], self.B[rowInds[i], colInds[j]])
                
        #Try all rows/cols 
        rowInds = numpy.arange(5)
        colInds = numpy.arange(7)
        
        A = self.B.subArray(rowInds, colInds)
        
        for i in range(A.shape[0]): 
            for j in range(A.shape[1]): 
                self.assertEquals(A[i, j], self.B[rowInds[i], colInds[j]])
                
        #No rows/cols 
        rowInds = numpy.array([], numpy.int)
        colInds = numpy.array([], numpy.int)
        
        A = self.B.subArray(rowInds, colInds)
        self.assertEquals(A.shape, (0, 0))
        
        A = self.A.subArray(rowInds, colInds)
        self.assertEquals(A.shape, (0, 0))
                
    def testNonZeroInds(self): 
        
        (rowInds, colInds) = self.B.nonzero()
        
        for i in range(rowInds.shape[0]): 
            self.assertNotEqual(self.B[rowInds[i], colInds[i]], 0)
        
        self.assertEquals(self.B.getnnz(), rowInds.shape[0])
        self.assertEquals(self.B.sum(), self.B[rowInds, colInds].sum())

        
        (rowInds, colInds) = self.C.nonzero()
        
        for i in range(rowInds.shape[0]): 
            self.assertNotEqual(self.C[rowInds[i], colInds[i]], 0)   
            
        self.assertEquals(self.C.getnnz(), rowInds.shape[0])
        self.assertEquals(self.C.sum(), self.C[rowInds, colInds].sum())
        
        #Try an array with no non zeros 
        nrow = 5 
        ncol = 7
        A = dyn_array((nrow, ncol))
        (rowInds, colInds) = A.nonzero()
        
        self.assertEquals(A.getnnz(), rowInds.shape[0])
        self.assertEquals(rowInds.shape[0], 0)
        self.assertEquals(colInds.shape[0], 0)
        
        #Zero size array 
        nrow = 0 
        ncol = 0
        A = dyn_array((nrow, ncol))
        (rowInds, colInds) = A.nonzero()
        self.assertEquals(A.getnnz(), rowInds.shape[0])
        self.assertEquals(rowInds.shape[0], 0)
        self.assertEquals(colInds.shape[0], 0)

    def testDiag(self): 
        nptst.assert_array_equal(self.A.diag(), numpy.zeros(5))
        nptst.assert_array_equal(self.B.diag(), numpy.array([  0,    0,    0,   -0.2,  12.2]))
        nptst.assert_array_equal(self.C.diag(), numpy.zeros(100))
        
        D = dyn_array((3, 3))
        D[0, 0] = -1
        D[1, 1] = 3.2 
        D[2, 2] = 34 
        
        nptst.assert_array_equal(D.diag(), numpy.array([-1, 3.2, 34]))
        
        E = dyn_array((0, 0)) 
        nptst.assert_array_equal(E.diag(), numpy.array([]))
        
    def testMean(self): 
        self.assertEquals(self.A.mean(), 0)
        self.assertAlmostEquals(self.B.mean(), 0.4848571428571428)
        self.assertAlmostEquals(self.C.mean(), 0.001697)
        
        D = dyn_array((0, 0)) 
        self.assertTrue(math.isnan(D.mean()))
    
    def testCopy(self): 
        A = dyn_array((5, 5)) 
        A[0, 0] = 1
        A[1, 0] = 2
        A[4, 2] = 3
        self.assertEquals(A[0, 0], 1)
        self.assertEquals(A[1, 0], 2)
        self.assertEquals(A[4, 2], 3)
        
        B = A.copy() 
        A[0, 0] = 2
        A[1, 0] = 3
        A[4, 2] = 4
        A[4, 4] = 5
        
        self.assertEquals(A[0, 0], 2)
        self.assertEquals(A[1, 0], 3)
        self.assertEquals(A[4, 2], 4)   
        self.assertEquals(A[4, 4], 5) 
        self.assertEquals(A.getnnz(), 4)
        
        self.assertEquals(B[0, 0], 1)
        self.assertEquals(B[1, 0], 2)
        self.assertEquals(B[4, 2], 3)
        self.assertEquals(B.getnnz(), 3)
        
    def testMultiply(self): 
        val = 2.0 
        C = self.B * val
        
        self.assertEquals(self.B[0, 1], 1)
        self.assertEquals(self.B[1, 3], 5.2)
        self.assertEquals(self.B[3, 3], -0.2)
        self.assertEquals(self.B[0, 6], -1.23)
        self.assertEquals(self.B[4, 4], 12.2)
        
        self.assertEquals(C[0, 1], self.B[0, 1]*val)
        self.assertEquals(C[1, 3], self.B[1, 3]*val)
        self.assertEquals(C[3, 3], self.B[3, 3]*val)
        self.assertEquals(C[0, 6], self.B[0, 6]*val)
        self.assertEquals(C[4, 4], self.B[4, 4]*val)


if __name__ == "__main__":
    unittest.main()
    
    