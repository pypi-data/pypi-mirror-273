import requests
class RetrieverVectorDB:

    def __init__(self, num_docs,url):
        self.num_docs = num_docs
        self.url = url
        
    def retriever(self,query):
        data = {'num_docs': self.num_docs, 'query': query}
        # Send the POST request
        response = requests.post(self.url, json=data)
        return response.json().get('relevant_documents')
