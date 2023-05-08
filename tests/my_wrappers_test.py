import unittest
from src.my_wrappers import capture_output

# Test function to be used with capture_output
def hello_world(name):
    print(f"Hello, {name}!")
    
def greet(name, greeting):
    print(f"{greeting}, {name}!")
    
def add(a, b):
    print(f"Adding {a} and {b}")
    return a + b 

class TestCaptureOutput(unittest.TestCase):
    
    def test_capture_output_basic(self):
        # Test case 1: Basic functionality
        hello_world_wrapped = capture_output(hello_world)
        result, output = hello_world_wrapped("John")
        self.assertEqual(output.getvalue(), "Hello, John!\n")

    def test_capture_output_multiple(self):
        # Test case 2: Multiple arguments 
        greet_wrapped = capture_output(greet)
        result, output = greet_wrapped("Jane", "Hi")
        self.assertEqual(output.getvalue(), "Hi, Jane!\n")


    def test_capture_output_keyword(self):
        # Test case 3: Keyword arguments
        greet_wrapped = capture_output(greet)
        result, output = greet_wrapped(name="Alice", greeting="Hey")
        self.assertEqual(output.getvalue(), "Hey, Alice!\n")

    def test_capture_output_return(self):
    # Test case 4: Return value
        add_wrapped = capture_output(add)
        result, output = add_wrapped(1, 2)
        self.assertEqual(result, 3)
        self.assertEqual(output.getvalue(), "Adding 1 and 2\n")



if __name__ == '__main__':
    unittest.main()
