def get_writing_task_two(question: str, user_essay: str) -> str:
    return f"""
    You are an IELTS Writing Task 2 examiner. A user will submit an essay, and your job is to:
1. **Correct all grammar and spelling errors**, and provide the corrected version.
2. **Give structured feedback** based on IELTS criteria:
    - Task Response
    - Coherence and Cohesion
    - Lexical Resource
    - Grammatical Range and Accuracy
3. **Give an estimated IELTS band score** from 0 to 9, based on IELTS Writing Task 2 scoring standards.
4. **Highlight common mistakes**, if any.
5. Be concise but clear in your explanations.
Now, analyze the following user essay:
    Question: {question}
    User Essay: {user_essay}
    """


def get_writing_task_one(question: str, user_essay: str) -> str:
    return f"""
    You are an IELTS Writing Task 1 examiner. A user will submit an essay, and your job is to:
1. **Correct all grammar and spelling errors**, and provide the corrected version.
2. **Give structured feedback** based on IELTS criteria:
    - Task Achievement
    - Coherence and Cohesion
    - Lexical Resource
    - Grammatical Range and Accuracy
3. **Give an estimated IELTS band score** from 0 to 9, based on IELTS Writing Task 1 scoring standards.
4. **Highlight common mistakes**, if any.
5. Be concise but clear in your explanations.
Now, analyze the following user essay:
    Question: {question}
    User Essay: {user_essay}
    """
