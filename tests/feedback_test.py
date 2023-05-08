import unittest
from src.feedback import gemerate_simple_feedback, get_similarity,\
    generate_passed_tests_message, generate_test_cases_feedback,\
    generate_elements_feedback

class TestGemerateSimpleFeedback(unittest.TestCase):
    def test_generate_simple_feedback(self):
        results = [{"result": True}, {"result": False}]
        expected_elements = [{"name": "Assign", "occurences": [3], "hint": ""}]
        cases = 1

        expected_feedback = "You passed 1 tests.\n" \
                            "Your code is using Assign at line(s): 3.\n" \
                            " For case 2 your code did not pass."

        feedback = gemerate_simple_feedback(results, expected_elements, cases)
        self.assertEqual(feedback, expected_feedback)


    def test_generate_simple_feedback_no_elements(self):
        results = [{"result": True}, {"result": False}]
        expected_elements = []
        cases = 1

        expected_feedback = "You passed 1 tests.\n" \
                            " For case 2 your code did not pass."

        feedback = gemerate_simple_feedback(results, expected_elements, cases)
        self.assertEqual(feedback, expected_feedback)


    def test_generate_simple_feedback_with_hints(self):
        results = [{"result": True}, {"result": False}]
        expected_elements = [{"name": "Assign", "occurences": [], "hint": "Try using the Assign statement."}]
        cases = 1

        expected_feedback = "You passed 1 tests.\n" \
                            "Try using the Assign statement.\n" \
                            " For case 2 your code did not pass."

        feedback = gemerate_simple_feedback(results, expected_elements, cases)
        self.assertEqual(feedback, expected_feedback)


    def test_generate_passed_tests_message(self):
        cases = 0
        total_tests = 2
        expected_feedback = "Congratulations you passed all the tests!\n"

        feedback = generate_passed_tests_message(cases, total_tests)
        self.assertEqual(feedback, expected_feedback)
    
    
    def test_generate_test_cases_feedback(self):
        results = [{"result": "Foo"}, {"result": "Bar"}]
        expected_feedback = " For case 1 your code has a Foo. For case 2 your code has a Bar."

        feedback = generate_test_cases_feedback(results)
        self.assertEqual(feedback, expected_feedback)


    def test_generate_elements_feedback(self):
        expected_elements = [{"name": "Assign", "occurences": [], "hint": ""}]
        expected_feedback = "Your code is not using any Assign.\n"

        feedback = generate_elements_feedback(expected_elements)
        self.assertEqual(feedback, expected_feedback)



class TestGetSimilarity(unittest.TestCase):
    def test_very_high_similarity(self):
        result = "Congratulations you passed all the tests!"
        expected = "Congratulations you passed all the tests!"

        percentage, similarity = get_similarity(result, expected)
        self.assertEqual(percentage, 100)
        self.assertEqual(similarity, "very high similarity")

    def test_high_similarity(self):
        result = "You passed 1 tests."
        expected = "You passed 2 tests. Try again!"

        percentage, similarity = get_similarity(result, expected)
        self.assertGreaterEqual(percentage, 50)
        self.assertLess(percentage, 75)
        self.assertEqual(similarity, "high similarity")

    def test_low_similarity(self):
        result = "Your code is not using any Assign."
        expected = "The gibberish is using For at line(s): 3."

        percentage, similarity = get_similarity(result, expected)
        self.assertGreaterEqual(percentage, 25)
        self.assertLess(percentage, 50)
        self.assertEqual(similarity, "low similarity")

    def test_very_low_similarity(self):
        result = "This code has no similarity."
        expected = "Nothing."

        percentage, similarity = get_similarity(result, expected)
        self.assertGreaterEqual(percentage, 0)
        self.assertLess(percentage, 25)
        self.assertEqual(similarity, "very low similarity")


if __name__ == '__main__':
    unittest.main()
