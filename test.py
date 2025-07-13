from openai import OpenAI

settings = "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"

client = OpenAI(api_key=settings)

response = client.responses.create(
    model="gpt-4.1-nano",
    input="""
    
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
Some people believe that teenagers should study all school subjects equally, while others think that they should focus more on the subjects they enjoy or do well in. While both opinions have their upsides and downsides, I believe that focusing on specific subjects outweighs studying all subjects with equal attention.

On one side, studying all subjects can help students build a strong base of general knowledge. In the future, people may need skills from different areas, so learning all subjects is useful. For example, a student who wants to be a doctor still needs to know how to write reports or understand history and culture. Also, if students give equal attention to all subjects, they may discover new interests or talents they didn’t know before. It also helps students become more flexible and think in different ways, which is important in today’s changing world.

However, I believe that students should be allowed to focus on the subjects they enjoy or are good at. This can help them stay motivated and achieve better results. For instance, if a student likes art or math, spending more time on that subject might help them become professionals in the future. Forcing students to study every subject equally may lead to stress or boredom, especially if they struggle in certain areas. By focusing on fewer subjects, students can also manage their time more effectively and prepare for careers that match their skills and interests.

In conclusion, although studying all subjects has benefits, I believe that it is more useful for teenagers to concentrate on the subjects they are interested in or strong at. This helps them reach their full potential and work towards their future goals with more focus and confidence.

""",
)

print(response.output_text)
