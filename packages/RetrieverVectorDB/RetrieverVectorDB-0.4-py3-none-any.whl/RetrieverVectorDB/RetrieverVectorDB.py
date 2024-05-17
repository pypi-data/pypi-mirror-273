import requests
class RetrieverVectorDB:

    @staticmethod
    def retriever(num_docs,url,query):
        data = {'num_docs': num_docs, 'query': query}
        # Send the POST request
        response = requests.post(url, json=data)
        return response.json().get('relevant_documents')
