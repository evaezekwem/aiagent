import unittest
from unittest.mock import patch
import os
from tools.evaluate_math_expression import evaluate_math_expression
from tools.get_current_temperature import get_current_temperature
from tools.get_file_content import get_file_content
from tools.get_files_info import get_files_info
from tools.run_python_file import run_python_file
from tools.write_file import write_file
from main import Agent, parse_args

class TestEvaluateMathExpression(unittest.TestCase):
    def test_valid_arithmetic(self):
        self.assertEqual(evaluate_math_expression("2 + 2"), 4)
        self.assertEqual(evaluate_math_expression("3 * 4 - 5"), 7)

    def test_math_functions(self):
        self.assertAlmostEqual(evaluate_math_expression("sin(0)"), 0)
        self.assertEqual(evaluate_math_expression("sqrt(16)"), 4)

    def test_parentheses(self):
        self.assertEqual(evaluate_math_expression("(2 + 3) * 4"), 20)

    def test_division_by_zero(self):
        self.assertTrue("Error" in str(evaluate_math_expression("1 / 0")))

    def test_invalid_syntax(self):
        self.assertTrue("Error" in str(evaluate_math_expression("2 +")))

    def test_unsafe_code(self):
        self.assertTrue("Error" in str(evaluate_math_expression("__import__('os').system('echo hi')")))

class TestGetCurrentTemperature(unittest.TestCase):
    def test_valid_city(self):
        try:
            temp = get_current_temperature(os.getcwd(), "San Francisco")
            self.assertIsInstance(temp, float)
        except Exception as e:
            self.assertTrue("Could not geocode city" not in str(e))

    def test_invalid_city(self):
        with self.assertRaises(ValueError):
            get_current_temperature(os.getcwd(), "FakeCity")

    def test_empty_city(self):
        with self.assertRaises(ValueError):
            get_current_temperature(os.getcwd(), "")

class TestGetFileContent(unittest.TestCase):
    def test_valid_file(self):
        fname = "tests.py"
        result = get_file_content(os.getcwd(), fname)
        self.assertIsInstance(result, str)
        self.assertFalse(result.startswith("Error:"))

    def test_file_outside(self):
        result = get_file_content(os.getcwd(), "../main.py")
        self.assertTrue(result.startswith("Error:"))

    def test_nonexistent_file(self):
        result = get_file_content(os.getcwd(), "does_not_exist.txt")
        self.assertTrue(result.startswith("Error:"))

    def test_directory_instead_of_file(self):
        result = get_file_content(os.getcwd(), ".")
        self.assertTrue(result.startswith("Error:"))
    
class TestGetFilesInfo(unittest.TestCase):
    def test_valid_directory(self):
        result = get_files_info(os.getcwd(), ".")
        self.assertIn("is_dir=", result)

    def test_directory_outside(self):
        result = get_files_info(os.getcwd(), "../")
        self.assertTrue(result.startswith("Error:"))

    def test_nonexistent_directory(self):
        result = get_files_info(os.getcwd(), "does_not_exist_dir")
        self.assertTrue(result.startswith("Error:"))

    def test_file_instead_of_directory(self):
        result = get_files_info(os.getcwd(), "tests.py")
        self.assertTrue(result.startswith("Error:"))

class TestRunPythonFile(unittest.TestCase):
    def setUp(self):
        # Create hello.py for subprocess tests
        self.hello_path = os.path.join(os.getcwd(), "hello.py")
        with open(self.hello_path, "w") as f:
            f.write(
                "import sys\n"
                "if __name__ == '__main__':\n"
                "    name = sys.argv[1] if len(sys.argv) > 1 else 'World'\n"
                "    print(f'Hello, {name or 'World'}')\n"
            )

    def tearDown(self):
        # Remove hello.py after tests
        if os.path.exists(self.hello_path):
            os.remove(self.hello_path)
            
    def test_valid_python_file(self):
        result = run_python_file(os.getcwd(), "hello.py")
        self.assertIn("Hello, World", result)

    def test_python_file_with_args(self):
        # Should not error, but may not use args
        result = run_python_file(os.getcwd(), "hello.py", ["Alice"])
        self.assertIn("Hello, Alice", result)

    def test_file_outside(self):
        result = run_python_file(os.getcwd(), "../main.py")
        self.assertTrue(result.startswith("Error:"))

    def test_nonexistent_file(self):
        result = run_python_file(os.getcwd(), "does_not_exist.py")
        self.assertTrue(result.startswith("Error:"))

    def test_non_python_file(self):
        result = run_python_file(os.getcwd(), "README.md")
        self.assertTrue(result.startswith("Error:"))

class TestWriteFile(unittest.TestCase):
    def tearDown(self):
        files_to_remove = [
            "test_write.txt",
            "../test_write.txt",
            "newdir/test_write.txt",
            "test_write_empty.txt"
        ]
        for fname in files_to_remove:
            abs_path = os.path.join(os.getcwd(), fname)
            if os.path.exists(abs_path):
                try:
                    os.remove(abs_path)
                except Exception:
                    pass
        # Remove newdir if empty
        newdir_path = os.path.join(os.getcwd(), "newdir")
        if os.path.isdir(newdir_path) and not os.listdir(newdir_path):
            try:
                os.rmdir(newdir_path)
            except Exception:
                pass
    def test_valid_file_write(self):
        result = write_file(os.getcwd(), "test_write.txt", "hello world")
        self.assertTrue(result.startswith("Successfully wrote to"))

    def test_file_outside(self):
        result = write_file(os.getcwd(), "../test_write.txt", "hello world")
        self.assertTrue(result.startswith("Error:"))

    def test_nonexistent_parent(self):
        result = write_file(os.getcwd(), "newdir/test_write.txt", "hello world")
        self.assertTrue(result.startswith("Successfully wrote to"))

    def test_empty_content(self):
        result = write_file(os.getcwd(), "test_write_empty.txt", "")
        self.assertTrue(result.startswith("Successfully wrote to"))

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "fake-key")
        self.system_prompt = "You are a helpful assistant."
        self.user_prompt = "Say hello!"
        self.agent = Agent(api_key=self.api_key, system_prompt=self.system_prompt, user_prompt=self.user_prompt, verbose=True)

    def test_config(self):
        config = self.agent._config()
        self.assertIsNotNone(config)

    def test_call_function_unknown(self):
        class DummyCall:
            name = "not_a_function"
            args = {}
        result = self.agent._call_function(DummyCall())
        self.assertEqual(result.parts[0].function_response.response["error"], "Unknown function: not_a_function")

    def test_generate_response(self):
        # Mock generate_response to avoid API call
        with patch.object(self.agent, 'generate_response', return_value='mocked_response'):
            result = self.agent.generate_response()
            self.assertEqual(result, 'mocked_response')

    def test_run(self):
        # Mock run to avoid API call
        with patch.object(self.agent, 'run', return_value='mocked_run'):
            result = self.agent.run()
            self.assertEqual(result, 'mocked_run')

class TestParseArgs(unittest.TestCase):
    def test_parse_args_verbose(self):
        prompt, verbose = parse_args(["hello", "--verbose"])
        self.assertEqual(prompt, "hello")
        self.assertTrue(verbose)

    def test_parse_args_no_verbose(self):
        prompt, verbose = parse_args(["hello", "world"])
        self.assertEqual(prompt, "hello world")
        self.assertFalse(verbose)

if __name__ == "__main__":
    unittest.main()
