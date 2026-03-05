from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()


def get_llm_response(
    prompt: str,
    temperature: float = 0.0,
    max_tokens: int = 500,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
) -> str:
    """
    Sends a prompt to the OpenAI API with configurable parameters and
    returns the response.

    Args:
        prompt (str): The prompt text to send to the model.
        model (str, optional): The model to use. Defaults to "gpt-3.5-turbo".
        temperature (float, optional): Sampling temperature. Defaults to 0.7.
        max_tokens (int, optional): Maximum number of tokens in the response.
            Defaults to 150.
        top_p (float, optional): Nucleus sampling parameter. Defaults to 1.0.
        frequency_penalty (float, optional): Frequency penalty. Defaults to 0.0.
        presence_penalty (float, optional): Presence penalty. Defaults to 0.0.

    Returns:
        str: The response from the LLM.
    """
    system_prompt = """You are an helpful AI assistant.
                    You always answer to the user's queries."""
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        # Extract and return the assistant's message from the response
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"
