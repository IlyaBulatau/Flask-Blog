from whoosh import fields, index, qparser
import os


class Schema(fields.SchemaClass):
    text = fields.TEXT(stored=True, sortable=True)

        
class SearchText:

    def __init__(self, search_text):
        self.search_text = search_text
        self.dirname = 'whooshee'
        if not os.path.isdir(self.dirname):
            os.mkdir('whooshee')
        self.ix = index.create_in('./whooshee', schema=Schema())

    def __call__(self, available_text):
        with self.ix.writer() as writer:
            writer.add_document(text=available_text)
        
        with self.ix.searcher() as search:
            parser = qparser.QueryParser('text', schema=self.ix.schema).parse(self.search_text)
            result = search.search(parser)
            for item in result:
                return item['text']
            
    def __len__(self):
        text = self.__call__()
        if text:
            return text
    
    





