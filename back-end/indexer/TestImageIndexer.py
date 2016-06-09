import unittest
import os
import ImageIndexer
        
IMG_NORMAL              = os.path.join(os.getcwd(), r'testData\excellent.gif')
IMG_WRONG_EXTENSION     = os.path.join(os.getcwd(), r'testData\suatmmWrongExt.txt')
IMG_NO_EXTENSION        = os.path.join(os.getcwd(), r'testData\oldNoExt')
FOLDER_WITH_NO_IMAGES   = os.path.join(os.getcwd(), r'testData\noImages')
    
class TestImageIndexer(unittest.TestCase):

    def testNormalImage(self):
        print(os.path.abspath(IMG_NORMAL))
        self.assertTrue(ImageIndexer.isImage(IMG_NORMAL))

    def testImageWithWrongExtension(self):
        self.assertTrue(ImageIndexer.isImage(IMG_WRONG_EXTENSION))

    def testImageWithNoExtension(self):
        self.assertTrue(ImageIndexer.isImage(IMG_NO_EXTENSION))

    def testFolderWithNoImages(self):
        self.assertEqual(ImageIndexer.findImages(FOLDER_WITH_NO_IMAGES),[])

if __name__ == '__main__':
    unittest.main()
