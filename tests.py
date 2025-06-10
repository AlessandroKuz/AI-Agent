import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file


class TestGetFilesInfo(unittest.TestCase):
    def test_valid_calculator_path1(self):
        result = get_files_info("calculator", ".")
        self.assertFalse(result.startswith("Error: "))
        # print(result)

    def test_valid_calculator_path2(self):
        result = get_files_info("calculator", "pkg")
        self.assertFalse(result.startswith("Error: "))
        # print(result)

    def test_invalid_path1(self):
        result = get_files_info("calculator", "/bin")
        self.assertTrue(result.startswith("Error: "))
        # print(result)

    def test_invalid_path2(self):
        result = get_files_info("calculator", "../")
        self.assertTrue(result.startswith("Error: "))
        # print(result)

    def test_None_path(self):
        result = get_files_info("calculator")
        self.assertFalse(result.startswith("Error: "))
        # print(result)


class TestGetFileContent(unittest.TestCase):
    def test_text_with_more_than_max_chars(self):
        result = get_file_content("calculator", "lorem.txt")
        self.assertFalse(result.startswith("Error: "))
        self.assertTrue(result.endswith(" truncated at 10000 characters]"))
        # print(result[-200:])

    def test_valid_file1(self):
        result = get_file_content("calculator", "main.py")
        self.assertFalse(result.startswith("Error: "))
        print(result)

    def test_valid_file2(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        self.assertFalse(result.startswith("Error: "))
        print(result)

    def test_valid_file3(self):
        result = get_file_content("calculator", "/bin/cat")
        self.assertTrue(result.startswith("Error: "))
        print(result)


class TestWriteFile(unittest.TestCase):
    def test_write_file1(self):
        result = write_file("calculator", "lorem2.txt", "wait, this isn't lorem ipsum")
        self.assertTrue("Successfully wrote to " in result)
        self.assertTrue(result.endswith("characters written)"))
        print(result)

    def test_write_file2(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        self.assertTrue("Successfully wrote to " in result)
        self.assertTrue(result.endswith("characters written)"))
        print(result)

    def test_write_file_invalid(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        self.assertTrue(result.startswith("Error: "))
        print(result)


if __name__ == '__main__':
    unittest.main()
