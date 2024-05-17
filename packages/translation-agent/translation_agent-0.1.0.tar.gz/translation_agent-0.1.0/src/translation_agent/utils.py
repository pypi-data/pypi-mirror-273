# coding: utf-8

import os
from typing import List, Union

import openai
import tiktoken
from dotenv import find_dotenv, load_dotenv

# import spacy
from icecream import ic
from langchain_text_splitters import RecursiveCharacterTextSplitter

# find dotenv does this check up the folder structure
load_dotenv(find_dotenv())  # read local .env file
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_TOKENS_PER_CHUNK = (
    1000  # if text is more than this many tokens, we'll break it up into
)
# discrete chunks to translate one chunk at a time


def get_completion(
    prompt: str,
    system_message: str = "You are a helpful assistant.",
    model: str = "gpt-4-turbo",
    temperature: float = 0,
    json_mode: bool = False,
) -> Union[str, dict]:
    """
        Generate a completion using the OpenAI API.

    Args:
        prompt (str): The user's prompt or query.
        system_message (str, optional): The system message to set the context for the assistant.
            Defaults to "You are a helpful assistant.".
        model (str, optional): The name of the OpenAI model to use for generating the completion.
            Defaults to "gpt-4-turbo".
        temperature (float, optional): The sampling temperature for controlling the randomness of the generated text.
            Defaults to 0.
        json_mode (bool, optional): Whether to return the response in JSON format.
            Defaults to False.

    Returns:
        Union[str, dict]: The generated completion.
            If json_mode is True, returns the complete API response as a dictionary.
            If json_mode is False, returns the generated text as a string.
    """

    if json_mode:
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    else:
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content


# def get_completion_content(
#     prompt,
#     system_message="You are a helpful assistant.",
#     model="gpt-4-0125-preview",
#     temperature=0,
#     JSON_mode=False,
# ):
#     completion = get_completion(
#         prompt, system_message, model, temperature, JSON_mode
#     )
#     return completion.choices[0].message.content


def one_chunk_initial_translation(
    source_lang: str, target_lang: str, source_text: str
) -> str:
    """
    Translate the entire text as one chunk using an LLM.

    Args:
        source_lang (str): The source language of the text.
        target_lang (str): The target language for translation.
        source_text (str): The text to be translated.

    Returns:
        str: The translated text.
    """

    system_message = f"You are an expert language translator, specializing in {source_lang} to {target_lang} translation."

    translation_prompt = f"""Your task is provide a professional translation of a text from {source_lang} to {target_lang}.

Translate the text below, delimited by XML tags <SOURCE_TEXT> and </SOURCE_TEXT> and output the translation.
Do not output anything other the translation.

<SOURCE_TEXT>
{source_text}
</SOURCE_TEXT>
"""
    prompt = translation_prompt.format(source_text=source_text)

    translation = get_completion(prompt, system_message=system_message)

    return translation


def one_chunk_reflect_on_translation(
    source_lang: str, target_lang: str, source_text: str, translation_1: str
) -> str:
    """
    Use an LLM to reflect on the translation, treating the entire text as one chunk.

    Args:
        source_lang (str): The source language of the text.
        target_lang (str): The target language of the translation.
        source_text (str): The original text in the source language.
        translation_1 (str): The initial translation of the source text.

    Returns:
        str: The LLM's reflection on the translation, providing constructive criticism and suggestions for improvement.
    """

    system_message = f"You are an expert language translator and mentor, specializing in {source_lang} to {target_lang} translation."

    reflection_prompt = """Your task is to carefully read a source text and a translation from {source_lang} to {target_lang}, and then give constructive criticism and helpful suggestions for the translation.

The source text and initial translation, delimited by XML tags <SOURCE_TEXT> and <TRANSLATION>, are as follows:

<SOURCE_TEXT>
{source_text}
</SOURCE_TEXT>

<TRANSLATION>
{translation_1}
</TRANSLATION>

When writing suggestions, pay attention to whether there are ways to improve the translation's \
(i) accuracy (by correcting errors of addition, mistranslation, omission, untranslated text),
(ii) fluency (grammar, inconsistency, punctuation, register, spelling), \
(iii) style (fix awkward wording),
(iv) terminology (inappropriate for context, inconsistent use), or \
(v) other errors.

Write a list of specific, helpful and constructive suggestions for improving the translation.
Each suggestion should address one specific part of the translation."""

    prompt = reflection_prompt.format(
        source_lang=source_lang,
        target_lang=target_lang,
        source_text=source_text,
        translation_1=translation_1,
    )
    reflection = get_completion(prompt, system_message=system_message)

    return reflection


def one_chunk_improve_translation(
    source_lang: str,
    target_lang: str,
    source_text: str,
    translation_1: str,
    reflection: str,
) -> str:
    """
    Use the reflection to improve the translation, treating the entire text as one chunk.

    Args:
        source_lang (str): The source language of the text.
        target_lang (str): The target language for the translation.
        source_text (str): The original text in the source language.
        translation_1 (str): The initial translation of the source text.
        reflection (str): Expert suggestions and constructive criticism for improving the translation.

    Returns:
        str: The improved translation based on the expert suggestions.
    """

    system_message = f"You are an expert language translator, specializing in {source_lang} to {target_lang} translation."

    prompt = f"""Your task is to carefully read, then improve, a translation from {source_lang} to {target_lang}, taking into
account a set of expert suggestions and constructive criticisms.

The source text, initial translation, and expert suggestions, delimited by XML tags <SOURCE_TEXT>, <TRANSLATION> and <EXPERT_SUGGESTIONS> are as follows:

<SOURCE_TEXT>
{source_text}
</SOURCE_TEXT>

<TRANSLATION>
{translation_1}
</TRANSLATION>

<EXPERT_SUGGESTIONS>
{reflection}
</EXPERT_SUGGESTIONS>

Taking into account the expert suggestions rewrite the translation to improve it, paying attention
to whether there are ways to improve the translation's \
(i) accuracy (by correcting errors of addition, mistranslation, omission, untranslated text),
(ii) fluency (grammar, inconsistency, punctuation, register, spelling), \
(iii) style (fix awkward wording),
(iv) terminology (inappropriate for context, inconsistent use), or \
(v) other errors. Output the list of suggestions in JSON, using the key "suggestions".

Output the new translation, and nothing else."""

    # prompt = improvement_prompt.format( ### Make this an F string?
    #    source_lang=source_lang,
    #    target_lang=target_lang,
    #    source_text=source_text,
    #    translation_1=translation_1,
    #    reflection=reflection,
    # )
    translation_2 = get_completion(prompt, system_message)

    return translation_2


def one_chunk_translate_text(
    source_lang: str, target_lang: str, source_text: str
) -> str:
    """
    Translate a single chunk of text from the source language to the target language.

    This function performs a two-step translation process:
    1. Get an initial translation of the source text.
    2. Reflect on the initial translation and generate an improved translation.

    Args:
        source_lang (str): The source language of the text.
        target_lang (str): The target language for the translation.
        source_text (str): The text to be translated.

    Returns:
        str: The improved translation of the source text.
    """
    translation_1 = one_chunk_initial_translation(
        source_lang, target_lang, source_text
    )
    # print(f"-------\ntranslation_1: {translation_1}\n")
    reflection = one_chunk_reflect_on_translation(
        source_lang, target_lang, source_text, translation_1
    )
    # print(f"-------\nReflection: {reflection}\n")
    translation_2 = one_chunk_improve_translation(
        source_lang, target_lang, source_text, translation_1, reflection
    )
    # print(f"-------\ntranslation_2: {translation_2}\n")

    return translation_2


# english_model = None  # spacy.load("en_core_web_sm")


# def find_sentence_starts(text):
#     global english_model
#     if english_model is None:
#         english_model = spacy.load("en_core_web_sm")  # load the english model

#     doc = english_model(text)

#     # To store the indices of the first character of each sentence
#     sentence_starts = []

#     # Iterate over the sentences
#     for sent in doc.sents:
#         # Find the start index of the first character of each sentence
#         start_index = sent.start_char
#         sentence_starts.append(start_index)

#     return sentence_starts


def num_tokens_in_string(
    input_str: str, encoding_name: str = "cl100k_base"
) -> int:
    """
    Calculate the number of tokens in a given string using a specified encoding.

    Args:
        str (str): The input string to be tokenized.
        encoding_name (str, optional): The name of the encoding to use. Defaults to "cl100k_base",
            which is the most commonly used encoder (used by GPT-4).

    Returns:
        int: The number of tokens in the input string.

    Example:
        >>> text = "Hello, how are you?"
        >>> num_tokens = num_tokens_in_string(text)
        >>> print(num_tokens)
        5
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(input_str))
    return num_tokens


# # Horribly inefficient linear search, but shouldn't matter
# def index_of_closest_value(values, target_value):
#     """Given a list of values and a specific target_value, find the index of the closest value in the list. (Inefficient implementation using linear search.)"""

#     closest_value = values[0]
#     index_of_closest_value = 0
#     min_diff = abs(target_value - closest_value)

#     for i in range(1, len(values)):  # Start from the second element
#         val = values[i]
#         diff = abs(target_value - val)
#         if diff < min_diff:
#             min_diff = diff
#             closest_value = val
#             index_of_closest_value = i

#     return index_of_closest_value


def multichunk_initial_translation(
    source_lang: str, target_lang: str, source_text_chunks: List[str]
) -> List[str]:
    """
    Translate a text in multiple chunks from the source language to the target language.

    Args:
        source_lang (str): The source language of the text.
        target_lang (str): The target language for translation.
        source_text_chunks (List[str]): A list of text chunks to be translated.

    Returns:
        List[str]: A list of translated text chunks.
    """

    system_message = f"You are an expert language translator, specializing in {source_lang} to {target_lang} translation."

    translation_prompt = """Your task is provide a professional translation from {source_lang} to {target_lang} of PART of a text.

The source text is below, delimited by XML tags <SOURCE_TEXT> and </SOURCE_TEXT>. Translate only the part within the source text
delimited by <TRANSLATE_THIS> and </TRANSLATE_THIS>. You can use the rest of the source text as context, but do not translate any
of the other text. Do not output anything other than the translation of the indicated part of the text.

<SOURCE_TEXT>
{tagged_text}
</SOURCE_TEXT>

To reiterate, you should translate only this part of the text, shown here again between <TRANSLATE_THIS> and </TRANSLATE_THIS>:
<TRANSLATE_THIS>
{chunk_to_translate}
</TRANSLATE_THIS>

Output only the translation of the portion you are asked to translate, and nothing else.
"""

    translation_chunks = []
    for i in range(len(source_text_chunks)):
        # Will translate chunk i
        tagged_text = (
            "".join(source_text_chunks[0:i])
            + "<TRANSLATE_THIS>"
            + source_text_chunks[i]
            + "</TRANSLATE_THIS>"
            + "".join(source_text_chunks[i + 1 :])
        )

        prompt = translation_prompt.format(
            source_lang=source_lang,
            target_lang=target_lang,
            tagged_text=tagged_text,
            chunk_to_translate=source_text_chunks[i],
        )
        # print(f"-------------\n{prompt}")

        translation = get_completion(prompt, system_message=system_message)
        translation_chunks.append(translation)

    return translation_chunks


def multichunk_reflect_on_translation(
    source_lang: str,
    target_lang: str,
    source_text_chunks: List[str],
    translation_1_chunks: List[str],
) -> List[str]:
    """
    Provides constructive criticism and suggestions for improving a partial translation.

    Args:
        source_lang (str): The source language of the text.
        target_lang (str): The target language of the translation.
        source_text_chunks (List[str]): The source text divided into chunks.
        translation_1_chunks (List[str]): The translated chunks corresponding to the source text chunks.

    Returns:
        List[str]: A list of reflections containing suggestions for improving each translated chunk.
    """

    system_message = f"You are an expert language translator and mentor, specializing in {source_lang} to {target_lang} translation."

    reflection_prompt = """Your task is to carefully read a source text and part of a translation of that text from {source_lang} to {target_lang}, and then give constructive criticism and helpful suggestions for improving the translation.

The source text is below, delimited by XML tags <SOURCE_TEXT> and </SOURCE_TEXT>, and the part that has been translated
is delimited by <TRANSLATE_THIS> and </TRANSLATE_THIS> within the source text. You can use the rest of the source text
as context for critiquing the translated part.

<SOURCE_TEXT>
{tagged_text}
</SOURCE_TEXT>

To reiterate, only part of the text is being translated, shown here again between <TRANSLATE_THIS> and </TRANSLATE_THIS>:
<TRANSLATE_THIS>
{chunk_to_translate}
</TRANSLATE_THIS>

The translation of the indicated part, delimited below by <TRANSLATION> and </TRANSLATION>, is as follows:
<TRANSLATION>
{translation_1_chunk}
</TRANSLATION>

When writing suggestions, pay attention to whether there are ways to improve the translation's:
(i) accuracy (by correcting errors of addition, mistranslation, omission, untranslated text),
(ii) fluency (grammar, inconsistency, punctuation, register, spelling),
(iii) style (fix awkward wording),
(iv) terminology (inappropriate for context, inconsistent use), or
(v) other errors.

Write a list of specific, helpful and constructive suggestions for improving the translation.
Each suggestion should address one specific part of the translation."""

    reflection_chunks = []
    for i in range(len(source_text_chunks)):
        # Will translate chunk i
        tagged_text = (
            "".join(source_text_chunks[0:i])
            + "<TRANSLATE_THIS>"
            + source_text_chunks[i]
            + "</TRANSLATE_THIS>"
            + "".join(source_text_chunks[i + 1 :])
        )

        prompt = reflection_prompt.format(
            source_lang=source_lang,
            target_lang=target_lang,
            tagged_text=tagged_text,
            chunk_to_translate=source_text_chunks[i],
            translation_1_chunk=translation_1_chunks[i],
        )
        # print(f"-------------\n{prompt}")

        reflection = get_completion(prompt, system_message=system_message)
        reflection_chunks.append(reflection)

    return reflection_chunks


def multichunk_improve_translation(
    source_lang: str,
    target_lang: str,
    source_text_chunks: List[str],
    translation_1_chunks: List[str],
    reflection_chunks: List[str],
) -> List[str]:
    """
    Improves the translation of a text from source language to target language by considering expert suggestions.

    Args:
        source_lang (str): The source language of the text.
        target_lang (str): The target language for translation.
        source_text_chunks (List[str]): The source text divided into chunks.
        translation_1_chunks (List[str]): The initial translation of each chunk.
        reflection_chunks (List[str]): Expert suggestions for improving each translated chunk.

    Returns:
        List[str]: The improved translation of each chunk.
    """

    system_message = f"You are an expert language translator, specializing in {source_lang} to {target_lang} translation."

    improvement_prompt = """Your task is to carefully read, then improve, a translation from {source_lang} to {target_lang}, taking into
account a set of expert suggestions and constructive critisms. Below, the source text, initial translation, and expert suggestions are provided.

The source text is below, delimited by XML tags <SOURCE_TEXT> and </SOURCE_TEXT>, and the part that has been translated
is delimited by <TRANSLATE_THIS> and </TRANSLATE_THIS> within the source text. You can use the rest of the source text
as context, but need to provide a translation only of the part indicated by <TRANSLATE_THIS> and </TRANSLATE_THIS>.

<SOURCE_TEXT>
{tagged_text}
</SOURCE_TEXT>

To reiterate, only part of the text is being translated, shown here again between <TRANSLATE_THIS> and </TRANSLATE_THIS>:
<TRANSLATE_THIS>
{chunk_to_translate}
</TRANSLATE_THIS>

The translation of the indicated part, delimited below by <TRANSLATION> and </TRANSLATION>, is as follows:
<TRANSLATION>
{translation_1_chunk}
</TRANSLATION>

The expert translations of the indicated part, delimited below by <EXPERT_SUGGESTIONS> and </EXPERT_SUGGESTIONS>, is as follows:
<EXPERT_SUGGESTIONS>
{reflection_chunk}
</EXPERT_SUGGESTIONS>

Taking into account the expert suggestions rewrite the translation to improve it, paying attention
to whether there are ways to improve the translation's
(i) accuracy (by correcting errors of addition, mistranslation, omission, untranslated text),
(ii) fluency (grammar, inconsistency, punctuation, register, spelling),
(iii) style (fix awkward wording),
(iv) terminology (inappropriate for context, inconsistent use), or
(v) other errors. Output the list of suggestions in JSON, using the key "suggestions".

Output the new translation of the indicated part, and nothing else."""

    translation_2_chunks = []
    for i in range(len(source_text_chunks)):
        # Will translate chunk i
        tagged_text = (
            "".join(source_text_chunks[0:i])
            + "<TRANSLATE_THIS>"
            + source_text_chunks[i]
            + "</TRANSLATE_THIS>"
            + "".join(source_text_chunks[i + 1 :])
        )

        prompt = improvement_prompt.format(
            source_lang=source_lang,
            target_lang=target_lang,
            tagged_text=tagged_text,
            chunk_to_translate=source_text_chunks[i],
            translation_1_chunk=translation_1_chunks[i],
            reflection_chunk=reflection_chunks[i],
        )
        # print(f"-------------\n{prompt}")

        translation_2 = get_completion(prompt, system_message=system_message)
        translation_2_chunks.append(translation_2)

    return translation_2_chunks


# Did we kill this? Else why spanish?
def multichunk_translation(source_lang, target_lang, source_text_chunks):
    """
    Improves the translation of multiple text chunks based on the initial translation and reflection.

    Args:
        source_lang (str): The source language of the text chunks.
        target_lang (str): The target language for translation.
        source_text_chunks (List[str]): The list of source text chunks to be translated.
        translation_1_chunks (List[str]): The list of initial translations for each source text chunk.
        reflection_chunks (List[str]): The list of reflections on the initial translations.

    Returns:
        List[str]: The list of improved translations for each source text chunk.
    """

    translation_1_chunks = multichunk_initial_translation(
        source_lang, target_lang, source_text_chunks
    )
    # for t in translation_1_chunks:
    #    print(t + "\n----\n")

    reflection_chunks = multichunk_reflect_on_translation(
        source_lang, target_lang, source_text_chunks, translation_1_chunks
    )
    # for t in reflection_chunks:
    #    print(t + "\n----\n")

    translation_2_chunks = multichunk_improve_translation(
        source_lang,
        target_lang,
        source_text_chunks,
        translation_1_chunks,
        reflection_chunks,
    )

    return translation_2_chunks


def calculate_chunk_size(token_count: int, token_limit: int) -> int:
    """
    Calculate the chunk size based on the token count and token limit.

    Args:
        token_count (int): The total number of tokens.
        token_limit (int): The maximum number of tokens allowed per chunk.

    Returns:
        int: The calculated chunk size.

    Description:
        This function calculates the chunk size based on the given token count and token limit.
        If the token count is less than or equal to the token limit, the function returns the token count as the chunk size.
        Otherwise, it calculates the number of chunks needed to accommodate all the tokens within the token limit.
        The chunk size is determined by dividing the token limit by the number of chunks.
        If there are remaining tokens after dividing the token count by the token limit,
        the chunk size is adjusted by adding the remaining tokens divided by the number of chunks.

    Example:
        >>> calculate_chunk_size(1000, 500)
        500
        >>> calculate_chunk_size(1530, 500)
        389
        >>> calculate_chunk_size(2242, 500)
        496
    """

    if token_count <= token_limit:
        return token_count

    num_chunks = (token_count + token_limit - 1) // token_limit
    chunk_size = token_count // num_chunks

    remaining_tokens = token_count % token_limit
    if remaining_tokens > 0:
        chunk_size += remaining_tokens // num_chunks

    return chunk_size


# def distribute_objects(x, n):
#     # Calculate the quotient and the remainder
#     quotient, remainder = divmod(x, n)

#     # Create a list to hold the number of objects per box
#     boxes = [quotient + 1 if i < remainder else quotient for i in range(n)]

#     return boxes


def translate(
    source_lang, target_lang, source_text, max_tokens=MAX_TOKENS_PER_CHUNK
):
    """Translate the source_text from source_lang to target_lang."""

    num_tokens_in_text = num_tokens_in_string(source_text)

    ic(num_tokens_in_text)

    if num_tokens_in_text < max_tokens:
        ic("Translating text as single chunk")

        final_translation = one_chunk_translate_text(
            source_lang, target_lang, source_text
        )

        return final_translation

    else:
        ic("Translating text as multiple chunks")

        token_size = calculate_chunk_size(
            token_count=num_tokens_in_text, token_limit=max_tokens
        )

        ic(token_size)

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4",
            chunk_size=token_size,
            chunk_overlap=0,
        )

        source_text_chunks = text_splitter.split_text(source_text)

        # # We've implemented a sentence splitter only for English, so if doing multi-chunk,
        # # make sure the source language is English.
        # if source_lang != "English":
        #     sys.error(
        #         "Sorry, only English source language supported for now for "
        #         "translation for long (multi-chunk) texts."
        #     )

        # potential_breakpoints = find_sentence_starts(
        #     source_text
        # )  # use start of sentences as potential places to break up the text into chunks
        # num_sentences = len(potential_breakpoints)
        # potential_breakpoints.append(len(source_text))

        # tokens_in_sentence = (
        #     []
        # )  # tokens_in_sentence[i] is the number of tokens in the i-th sentence
        # for i in range(num_sentences):
        #     start_index = potential_breakpoints[i]
        #     end_index = potential_breakpoints[i + 1]
        #     tokens_in_sentence.append(
        #         num_tokens_in_string(source_text[start_index:end_index])
        #     )

        # # Look at the total number of tokens, and MAX_TOKENS_PER_CHUNK to figure out how many chunks we need
        # total_tokens = sum(
        #     tokens_in_sentence
        # )  # should be similar to num_tokens_in_text above
        # num_chunks = math.ceil(float(total_tokens) / MAX_TOKENS_PER_CHUNK)
        # print(f"Translating text as {num_chunks} chunks")

        # # The location of the breakpoints if we chopped the text into num_chunks equal-size chunks (equal number of tokens)
        # desired_length_per_chunk = float(total_tokens) / num_chunks
        # desired_breakpoints = [
        #     i * desired_length_per_chunk for i in range(num_chunks)
        # ]
        # desired_breakpoints.append(total_tokens)

        # # Pick the specific places where we'll break up the text into num_chunks
        # cum_tokens_count = [0] + list(itertools.accumulate(tokens_in_sentence))
        # actual_breakpoints = []
        # for i in desired_breakpoints:
        #     actual_breakpoints.append(index_of_closest_value(cum_tokens_count, i))

        # # print(actual_breakpoints)
        # # print([cum_tokens_count[i] for i in actual_breakpoints])

        # source_text_chunks = []
        # for i in range(num_chunks):
        #     source_text_chunks.append(
        #         source_text[
        #             potential_breakpoints[
        #                 actual_breakpoints[i]
        #             ] : potential_breakpoints[actual_breakpoints[i + 1]]
        #         ]
        #     )

        translation_2_chunks = multichunk_translation(
            source_lang, target_lang, source_text_chunks
        )

        return "".join(translation_2_chunks)
