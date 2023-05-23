from whoosh import fields, index, qparser
import os


class Schema(fields.SchemaClass):
    """
    Схема по которой будет происходить поиск текста
    """
    text = fields.TEXT(stored=True, sortable=True)

        
class SearchText:
    """
    Класс для поиска подтекста в полном текстк
    """

    def __init__(self, search_text):
        self.search_text = search_text # текст который ищут
        self.dirname = 'whooshee' # директория дляя файлов whooshee
        if not os.path.isdir(self.dirname):
            os.mkdir('whooshee')
        self.ix = index.create_in('./whooshee', schema=Schema()) # индекс с схемой

    def __call__(self, available_text):
        with self.ix.writer() as writer: # создание обьекта читающего текст
            writer.add_document(text=available_text) # добавление текста по которму идет поиск
        
        with self.ix.searcher() as search: # создание поисковика
            parser = qparser.QueryParser('text', schema=self.ix.schema).parse(self.search_text) # определение поиска по схема
            result = search.search(parser) # поиск
            for item in result:
                return item['text'] # если что то есть вернуть
            
    def __len__(self):
        text = self.__call__()
        if text:
            return text
    
    





