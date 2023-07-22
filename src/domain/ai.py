import openai
import os

class Ai():
    
    def __init__(self) -> None:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
    
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
