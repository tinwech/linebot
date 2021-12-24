import six
from google.cloud import translate_v2 as translate

def translate_text(target, text):
    translate_client = translate.Client()
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target, source_language='zh-TW')
    print(result)
    return result["translatedText"]

if __name__ == '__main__':
    translate_text('en', '桃園')