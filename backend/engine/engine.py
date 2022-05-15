from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import faiss


class Engine:

    def __init__(self):
        self.model = self.__create_model()

    def start(self, all_sentences, sentence_to_check, number_of_results):
        sentences_vectors = self.__encode_text(all_sentences)
        index = self.__create_index(sentences_vectors)
        vector_of_sentence_to_search = self.__encode_text(sentence_to_check)
        similar_results, ids = self.__search_similarity(
            index, vector_of_sentence_to_search, sentences_vectors, int(number_of_results))
        result = self.__calculate_similarity(vector_of_sentence_to_search, similar_results)

        return ids, result

    @staticmethod
    def prepare_results(ids, prepared_results, calculation_result):
        counter = 0
        result = []

        for elem in ids[0]:
            result.append({
                'name': prepared_results[elem]['name'],
                'result': calculation_result[0][counter]
            })
            counter += 1

        return result

    def __encode_text(self, sentences):
        return self.model.encode(sentences)

    @staticmethod
    def __create_index(vectors_of_all_sentences):
        num_of_sentences = vectors_of_all_sentences.shape[0]

        if num_of_sentences < 50:
            cells = num_of_sentences
        else:
            cells = 50

        dimension = vectors_of_all_sentences.shape[1]
        quantizer = faiss.IndexFlatL2(dimension)
        index_ivf = faiss.IndexIVFFlat(quantizer, dimension, cells)
        index_ivf.nprobe = 10
        index_ivf.train(vectors_of_all_sentences)
        index_ivf.add(vectors_of_all_sentences)

        return index_ivf

    @staticmethod
    def __search_similarity(index, vector_of_sentence_to_search, vectors_of_all_sentences, number_of_results):
        print(vector_of_sentence_to_search.shape)
        distances, indexes = index.search(vector_of_sentence_to_search, number_of_results)

        counter = 0
        ids = indexes[0]
        similar_results = np.zeros((len(indexes[0]), vector_of_sentence_to_search.shape[1]))

        for i in ids:
            similar_results[counter] = vectors_of_all_sentences[i]
            counter += 1

        return similar_results, indexes

    @staticmethod
    def __calculate_similarity(vector_of_sentence_to_search, vectors_of_all_sentences):
        return cosine_similarity(vector_of_sentence_to_search, vectors_of_all_sentences)

    @staticmethod
    def __create_model():
        return SentenceTransformer('bert-base-nli-mean-tokens')
