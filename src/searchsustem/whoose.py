from whoosh import fields, index, qparser


class Schema(fields.SchemaClass):
    text = fields.TEXT(stored=True, sortable=True)



def full_text_search(search_text, available_text):
    """
    Функция ищет совпадения в тексте поста по тексту запроса
    """
    ix = index.create_in('./whooshee', schema=Schema())
    with ix.writer() as w:
        w.add_document(text=available_text)
        
        ix = index.open_dir('./whooshee')

        
    with ix.searcher() as s:
        qp = qparser.QueryParser('text', schema=ix.schema)
        q = qp.parse(search_text)
        res = s.search(q)
        for item in res:
            return (item['text'])



