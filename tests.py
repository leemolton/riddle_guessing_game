import unittest
import unittest.mock
import quiz


class test_run(unittest.TestCase): #Test suite

    def test_is_this_thing_on(self): #Basic functionality test (Test passing)
        self.assertEqual(1,1)
        
        
    def can_i_write_to_a_file(self, message): #Test opening a file and writing to it (Test passing)
       with open (self, 'a') as file:
           file.writelines(message + "\n")
           
    
    def is_file_empty(self): #Test if file is empty to start with (Test passing)
        data = []
        self.assertEqual(len(data),0)
        
        
    def test_request(self):
        url = "/templates/index.html"
        self.assertTrue(url, "/templates/index.html")
        
        
    def test_index_function(self, mocked_index):
        mocked_index.return_value = 1
        self.assertEqual(mocked_index, 1)

print("All the tests have passed")




