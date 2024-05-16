from bs4 import BeautifulSoup
from googletrans import Translator

def translate_html(html_content, src_lang='en', dest_lang='es'):
    translator = Translator()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for h1 in soup.find_all('h1'):
        h1.string = translator.translate(h1.text, src=src_lang, dest=dest_lang).text
    
    for p in soup.find_all('p'):
        p.string = translator.translate(p.text, src=src_lang, dest=dest_lang).text
    
    for td in soup.find_all('td'):
        strongs = td.find_all('strong')
        for strong in strongs:
            original_text = strong.text
            if not '{{' in original_text and not '}}' in original_text:
                translated_text = translator.translate(original_text, src=src_lang, dest=dest_lang).text
                strong.string = translated_text
    
    return str(soup)
