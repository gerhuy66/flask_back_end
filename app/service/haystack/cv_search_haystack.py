from haystack.preprocessor.cleaning import clean_wiki_text
# from haystack.preprocessor.utils import convert_files_to_dicts, fetch_archive_from_http

# from haystack.reader.transformers import TransformersReader
# from haystack.utils import print_answers


from haystack.retriever.sparse import ElasticsearchRetriever
from haystack.pipeline import ExtractiveQAPipeline,DocumentSearchPipeline

from app.service.haystack import farm_reader,document_store



def search_cv(query):
    doc_store = document_store
    reader = farm_reader
    retriever = ElasticsearchRetriever(document_store=doc_store)
    pipe = ExtractiveQAPipeline(reader, retriever)
    prediction = pipe.run(query=query, top_k_retriever=5, top_k_reader=5)
    results = []

    for an in prediction.get('answers'):
        result_map = {}
        result_map['answer'] = an.get('answer')
        result_map['context'] = an.get('context')
        result_map['file_url'] = an.get('meta').get('name')
        result_map['prob'] = an.get('probability')
        results.append(result_map)

    return sorted(results,key=lambda k: k['prob'],reverse=True)

def search_document(query):
    retriever = ElasticsearchRetriever(document_store=document_store)
    pipe = DocumentSearchPipeline(retriever=retriever)
    rs = pipe.run(query=query,top_k_retriever=20)
    docs = rs.get('documents')
    results = []
    for an in docs:
        result_map = {}
        result_map['text'] = an.get('text')
        # result_map['score'] = an.get('score')
        # result_map['probability'] = an.get('probability')
        result_map['file_url'] = an.get('meta').get('name')
        results.append(result_map)

    return results