import re
from urllib.parse import quote

import statistic_mgr

def extract_movie_name(text):
    result = re.search(r'<<(.*?)>>', text)

    if result:
        extracted_text = result.group(1)
        return extracted_text
    else:
        return None


def url_translation(chinese_url):
    encoded_url = quote(chinese_url, safe=':/')
    return (encoded_url)


def load_prompt(user_id, prefix_text):

    prompt_str = "History:"
    if user_id in statistic_mgr.user_input:
        for statement in statistic_mgr.user_input[user_id]:
            prompt_str = prompt_str + statement + "。"
    prompt_str = prefix_text + "。"

    try:
        with open('./prompt.txt', 'r', encoding='utf-8') as file:
            prompt_str = prompt_str + file.read()
        with open('./movies_for_prompt.txt', 'r', encoding='utf-8') as file:
            prompt_str = prompt_str + file.read()
    except FileNotFoundError:
        print("No such file")
    except IOError:
        print("Reading error")

    
    return prompt_str

