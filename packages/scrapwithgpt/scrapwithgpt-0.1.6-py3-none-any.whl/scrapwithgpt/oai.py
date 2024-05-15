# Functions to call openAI LLM

from .config import (OAI_KEY, MODEL_EMB_SMALL, MODEL_CHAT, MAX_TOKEN_OUTPUT_DEFAULT, 
                     MODEL_GPT4_TURBO, MODEL_GPT4_STABLE, MAX_TOKEN_WINDOW_GPT4_TURBO, 
                     MAX_TOKEN_WINDOW_GPT4, MAX_TOKEN_WINDOW_GPT35_TURBO, MAX_TOKEN_OUTPUT_GPT3, MAX_TOKEN_OUTPUT_DEFAULT_HUGE)
from .utils import log_issue


from typing import Optional
import tiktoken
import openai


# *************************************************************

YOUR_CLIENT = openai.OpenAI(
    api_key=OAI_KEY,
)

# *************************************************************

def embed_text(
    text: str, max_attempts: int = 3, model=MODEL_EMB_SMALL
) -> Optional[list[float]]:
    """
    Micro function which returns the embedding of one chunk of text or None if issue.

    Model is the small one by default.
    """
    if text == "":
        return "res"  # FIXME
    attempts = 0
    while attempts < max_attempts:
        try:
            res = (
                YOUR_CLIENT.embeddings.create(
                    model=model, input=text, encoding_format="float"
                    ).data[0].embedding
            )
            return res
        except Exception as e:
            attempts += 1
            log_issue(f"OAI Embedding faced the exception {e} at attempt # {attempts} out of 3"
            )

def ask_question_gpt(question: str, role: str = "", model: str = MODEL_CHAT, 
                     max_tokens: int = MAX_TOKEN_OUTPUT_DEFAULT, verbose: bool = True, temperature=0, top_p=1,) -> Optional[str]:
    """
    Queries an OpenAI GPT model (GPT-3.5 Turbo or GPT-4) with a specific question.

    Args:
        question (str): The question to ask the model.
        role (str, optional): System prompt to be initialized in the chat table, defining ChatGPT's behavior.
        model (str, optional): The model to use. Defaults to GPT-3.5 Turbo. To choose GPT 4, use 'MODEL_GPT4_TURBO'
        max_tokens (int, optional): Maximum number of tokens for the answer.
        verbose (bool, optional): Will print information in the console.

    Returns:
        str: The model's reply to the question or None if issue
    """
    max_token_window = {
        MODEL_GPT4_TURBO: MAX_TOKEN_WINDOW_GPT4_TURBO,
        MODEL_GPT4_STABLE: MAX_TOKEN_WINDOW_GPT4,
        MODEL_CHAT: MAX_TOKEN_WINDOW_GPT35_TURBO,
    }.get(model, MAX_TOKEN_OUTPUT_GPT3)
    initial_token_usage = calculate_token(role) + calculate_token(question)
    if initial_token_usage > max_token_window:
        print("Your input is too large for the query regardless of the max_tokens for the reply.")
        return ""
    elif initial_token_usage + max_tokens > max_token_window:
        max_tokens_adjusted = max_token_window - initial_token_usage
        print(f"Your input + the requested tokens for the answer exceed the maximum amount of {max_token_window}.\n Please adjust the max_tokens to a MAXIMUM of {max_tokens_adjusted}")
        return ""
    current_chat = initialize_role_in_chatTable(role)
    current_chat = add_content_to_chatTable(question, "user", current_chat)
    if verbose:
        print(f"Completion ~ {max_tokens} tokens. Request ~ {initial_token_usage} tokens.\nContext provided to GPT is:\n{current_chat}")
    return request_chatgpt(current_chat, max_tokens=max_tokens, model=model, temperature=temperature, top_p=top_p)


def request_chatgpt(current_chat: list, max_tokens: int, stop_list=False, max_attempts=3, model=MODEL_CHAT, temperature=0, top_p=1) -> Optional[str]:
    """
    Calls the ChatGPT OpenAI completion endpoint with specified parameters.

    Args:
        current_chat (list): The prompt used for the request.
        max_tokens (int, optional): Maximum number of tokens for the answer.
        stop_list (bool, optional): Whether to use specific stop tokens. Defaults to False.
        max_attempts (int, optional): Maximum number of retries. Defaults to 3.
        model (str, optional): ChatGPT OpenAI model used for the request. Defaults to 'MODEL_CHAT'.
        temperature (float, optional): Sampling temperature for the response. A value of 0 means deterministic output. Defaults to 0.
        top_p (float, optional): Nucleus sampling parameter, with 1 being 'take the best'. Defaults to 1.

    Returns:
        str: The response text or None if issue
    """
    max_tokens = int(max_tokens)
    if max_tokens > MAX_TOKEN_OUTPUT_GPT3:
        print(f"The Max Tokens cannot exceed {MAX_TOKEN_OUTPUT_GPT3}. You put {max_tokens}. This is the max length of the response.")
        return
    stop = stop_list if (stop_list and len(stop_list) < 4) else ""
    attempts = 0
    valid = False
    rep = None    # print("Writing the reply for ", current_chat) # Remove in production - to see what is actually fed as a prompt
    while attempts < max_attempts and not valid:
        try:
            response = YOUR_CLIENT.chat.completions.create(
                messages=current_chat,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=0,
                presence_penalty=0,
                stop=stop,
                model=model,
            )
            rep = response.choices[0].message.content
            rep = rep.strip()
            valid = True
        except Exception as e:
            attempts += 1
    if not rep:
        print(f"We didn't get a reply despite {attempts} attempts")
    return rep


def ask_question_gpt4(question: str, role: str, model=MODEL_GPT4_TURBO, max_tokens=MAX_TOKEN_OUTPUT_DEFAULT_HUGE, verbose=False, temperature=0, top_p=1, json_on=False,) -> str:
    """
    Queries Chat GPT 4 with a specific question if too lazy to change the param in ask_question_gpt)
    """
    return ask_question_gpt(question=question, role=role, model=model, max_tokens=max_tokens, verbose=verbose, temperature=temperature, top_p=top_p)


def calculate_token(text: str) -> Optional[int]:
    """
    Calculates the number of tokens for a given text using a specific tokenizer.

    Args:
        text (str): The text to calculate tokens for.

    Returns:
        int: The number of tokens in the text or -1 if there's an error.
    
    Note:
        Uses the tokenizer API and takes approximately 0.13 seconds per query.
    """
    if not isinstance(text, str): 
        print(f"Input is {type(text)} - must be str. Try force conversation")
        try:
            text = str(text)
        except Exception as e:
            log_issue(e, calculate_token, f"Failed to convert to string => {text}")
            return
    try:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return len(encoding.encode(text))
    except Exception as e:
        log_issue(e, calculate_token, f"Input type: {type(text)}. Text: {text}")
        return -1

def initialize_role_in_chatTable(role_definition: str) -> list[dict[str, str]]:
    """
    We need to define how we want our model to perform.
    This function takes this definition as a input and returns it into the chat_table_format.
    """
    return [{"role": "system", "content": role_definition}]


def add_content_to_chatTable(
    content: str, role: str, chatTable: list[dict[str, str]]
) -> list[dict[str, str]]:
    """
    Feeds a chatTable with the new query. Returns the new chatTable.
    Role is either 'assistant' when the AI is answering or 'user' when the user has a question.
    Added a security in case change of name.
    """
    new_chatTable = list(chatTable)
    normalized_role = role.lower()
    if normalized_role in ["user", "client"]:
        new_chatTable.append({"role": "user", "content": content})
    else:
        new_chatTable.append({"role": "assistant", "content": content})
    return new_chatTable

# *************************************************************
if __name__ == "__main__":
    pass