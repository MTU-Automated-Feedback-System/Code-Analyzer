from difflib import SequenceMatcher
import openai
import os
openai.api_key = os.environ.get("OPENAI_API_KEY")

# This function could be modularized

# Test of the above function
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


def gemerate_simple_feedback(results, expected_elements, cases):
    total_tests = len(results)
    
    passed_tests_message = generate_passed_tests_message(cases, total_tests)
    elements_feedback = generate_elements_feedback(expected_elements)
    test_cases_feedback = generate_test_cases_feedback(results)
    
    return passed_tests_message + elements_feedback + test_cases_feedback


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


"""
    This simple role is working better than the more complex one.
    It seems that the current model "gpt-3.5-turbo" is not able to have a complex role.
    It seems better to keep it short and let is construct the answer with a very simple request.
"""
def chat_general(exercise, submission): # pragma: no cover
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"You are an assistant for students that are learning programming.\
            You will provide feedback in a single sentence for the following assignment:{exercise['description']['description']}"},
        {"role": "user", "content": "Review this code: " + submission},

        ]
    )
    return completion["choices"][0]["message"]["content"]


"""
    Custom prompt using elements of the exercise json to construct coherent sentences.
    This setup seems to be able to provide high quality feedback.
    However, since we have a higher amount of words (tokens), the cost is significantly higher. 
"""
def chat_case(exercise, submission, case_index, code_output): # pragma: no cover
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"You are an assistant for students that are learning programming.\
            You will provide feedback for the following assignment:\n{exercise['description']['description']}.\
            The student solution should use the following elements: {', '.join([e['name'] for e in exercise['expected_elements']])}.\
            The student code is failing to pass the following case with the given expected result: {exercise['test_cases'][case_index]}.\
            Provide hints in 2 to 3 sentences to fix the student code and pass the case."},\
        {"role": "user", "content": f"Review this code:  {submission}.\
            That returns the following output: {code_output}."}
        ]
    )
    return completion["choices"][0]["message"]["content"]


"""
    Example of a more complex role, explaining how to behave more in depth and the structure of the answers.
    Unfortunately, this is not working as expected, the model explains too much and does not provide a simple answer.
    It also starts hallucinating and providing feedback that isn't correct, or completely miss some requirements.
"""
def chat_case_specific_role(exercise, submission): # pragma: no cover
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an assistant for students that are learning programming.\
                You will provide explanations as if I was a student that is learning programming.\
                For some student code, you will explain what to fix to achieve the assignment and meet the requirements: {exercise}"},
            {"role": "user", "content": "Give an hint for this student code in 2 sentences: " + submission},

        ]
    )
    return completion["choices"][0]["message"]["content"]
