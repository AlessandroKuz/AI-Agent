import unittest
from functions.get_files_info import get_files_info


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


if __name__ == '__main__':
    unittest.main()
