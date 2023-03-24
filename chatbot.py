import openai
import os

print(os.getenv("OPENAI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = 'gpt-3.5-turbo'


def cgpt_call(user_msg, temperature):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=user_msg,
        max_tokens=200,
        temperature=temperature
    )
    api_usage = response['usage']
    print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    return response.choices[0].message.content.strip()


def generate_response(prompt, temperature):
    try:
        user_msg = [{'role': 'user', 'content': prompt}]
        return cgpt_call(user_msg, temperature)
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)
