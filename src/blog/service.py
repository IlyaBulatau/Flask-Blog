import re

def replace_tag_in_text(text):
    """
    Удаляет html теги в начале и конце строки
    """
    result = re.sub(r'^<.+?>', '', text)
    result = re.sub(r'</\w+?>$', '', result)
    return result


