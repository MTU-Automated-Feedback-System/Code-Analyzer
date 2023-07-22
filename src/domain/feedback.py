from difflib import SequenceMatcher

class Feedback():

    def __init__(self) -> None:
        self.feedback = ""
        
    """_summary_
    """
    def gemerate_simple_feedback(self, results, expected_elements, cases):
        total_tests = len(results)
        
        passed_tests_message = self.generate_passed_tests_message(cases, total_tests)
        elements_feedback = self.generate_elements_feedback(expected_elements)
        test_cases_feedback = self.generate_test_cases_feedback(results)
        
        self.feedback = passed_tests_message + elements_feedback + test_cases_feedback
    
    
    def generate_passed_tests_message(cases: int, total_tests: int) -> str:
        if cases == 0:
            return "Congratulations you passed all the tests!\n"
        else:
            return f"You passed {total_tests - cases} tests.\n"


    def generate_elements_feedback(expected_elements: list) -> str:
        feedback = ""
        for elements in expected_elements:
            element = elements["name"]
            lines = elements["occurences"]
            if len(lines) > 0:
                feedback += f"Your code is using {element} at line(s): {', '.join(map(str, lines))}.\n"
            elif len(elements["hint"]) > 0:
                feedback += elements["hint"] + "\n"
            else:
                feedback += f"Your code is not using any {element}.\n"
        return feedback


    def generate_test_cases_feedback(results: list) -> str:
        feedback = ""
        for i, result in enumerate(results):
            if result["result"] == False:
                feedback += f" For case {i+1} your code did not pass."
            elif type(result["result"]) == str:
                feedback += f" For case {i+1} your code has a {result['result']}."
        return feedback


def get_similarity(result, expected):
    percentage = SequenceMatcher(None, result, expected).ratio() * 100
    print("Percentage: ", percentage)

    match percentage:
        case p if 0 <= p < 25:
            return percentage, "very low similarity"
        case p if 25 <= p < 50:
            return percentage, "low similarity"
        case p if 50 <= p < 75:
            return percentage, "high similarity"
        case p if 75 <= p <= 100:
            return percentage, "very high similarity"
        
    return 0, "invalid percentage"

