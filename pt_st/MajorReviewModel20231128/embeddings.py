import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import numpy as np
from collections import Counter

class allEmbeddingsCalculator:
    def __init__(self):
        # Initialize the BERT model and tokenizer
        self.model_name = 'bert-base-uncased'
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertModel.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load data and preprocess stop words
        self.df_all = pd.read_csv("/Users/kehaigen/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/alltext.csv", encoding='ISO-8859-1')
        self.tmp = []
        for item in self.df_all["reviews_lemmatized"].apply(lambda x: x.split()):
            self.tmp.extend(item)
        self.users_stop_words = []
        for _ in Counter(self.tmp).most_common(30):
            if _[0] in stopwords.words('english'):
                continue
            else:
                self.users_stop_words.append(_[0])
        self.stop_words = set(stopwords.words('english') + self.users_stop_words)

    def preprocess(self, text):
        words = self.tokenizer.tokenize(text.lower())
        return [w for w in words if w not in self.stop_words]

    def text_to_bert_embedding(self, text):
        self.model = self.model.to(self.device)
        try:
            tokens = self.tokenizer.encode(text, add_special_tokens=True)
            input_ids = torch.tensor(tokens).unsqueeze(0).to(self.device)
            with torch.no_grad():
                outputs = self.model(input_ids)
            # embedding = torch.mean(outputs.last_hidden_state, dim=1).cpu().numpy()
            embedding = torch.mean(outputs[0], dim=1).cpu().numpy()
            return embedding
        except:
            return [[]]
    def load_topic_data(self, file_path):
        data = np.load(file_path, allow_pickle=True).item()
        return data['topic_embeddings'], data['topic_rates']

    def load_precomputed_reviews(self, file_path):
        data = np.load(file_path, allow_pickle=True).item()
        return data['embeddings'], data['University'], data['reviews']

    def calculate_topic_probabilities(self, input_text, pre_saved_data='/Users/zhiyue/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/topic_data.npy'):
        saved_data = np.load(pre_saved_data, allow_pickle=True).item()
        topic_embeddings = saved_data['topic_embeddings']

        input_text_tokens = self.preprocess(input_text)
        input_text_embedding = self.text_to_bert_embedding(" ".join(input_text_tokens))

        similarities = []
        for sub_topic, sub_topic_embedding in topic_embeddings.items():
            similarity = cosine_similarity(input_text_embedding, sub_topic_embedding).squeeze()
            similarities.append(similarity)

        normalized_probabilities = np.array(similarities) / np.sum(similarities)
        probabilities_df = pd.DataFrame({
            'sub_topic': list(topic_embeddings.keys()),
            'topic_probability': normalized_probabilities
        })

        return probabilities_df
    def calculate_weighted_average_similarity(self, input_text, embedding_file='/Users/zhiyue/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/reviews_embedding_bert.npy', topic_data_file='/Users/zhiyue/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/topic_data.npy'):
        precomputed_embeddings, precomputed_universities, precomputed_reviews = self.load_precomputed_reviews(embedding_file)
        topic_embeddings, topic_rates = self.load_topic_data(topic_data_file)

        input_text_embedding = self.text_to_bert_embedding(input_text)
        topic_probabilities_df = self.calculate_topic_probabilities(input_text)

        universities = self.df_all['University'].unique()
        unnormalized_results = {}
        total_was = 0
        results = {}  # Initialize the results dictionary

        for university in universities:
            university_indices = np.where(precomputed_universities == university)[0]
            topics = self.df_all[self.df_all['University'] == university]['sub_topic'].unique()
            university_weighted_similarities = []
            max_similarity = 0
            most_relevant_review = ''
            highest_prob_topic = ''

            for topic in topics:
                topic_indices = self.df_all[(self.df_all['University'] == university) & (self.df_all['sub_topic'] == topic)].index
                relevant_indices = np.intersect1d(university_indices, topic_indices)
                similarities = []

                for i in relevant_indices:
                    review_embedding = precomputed_embeddings[i]
                    similarity = cosine_similarity(np.atleast_2d(input_text_embedding), np.atleast_2d(review_embedding))[0][0]
                    similarities.append(similarity)

                    if similarity > max_similarity:
                        max_similarity = similarity
                        most_relevant_review = precomputed_reviews[i]
                        highest_prob_topic = topic

                topic_probability = topic_probabilities_df[topic_probabilities_df['sub_topic'] == topic]['topic_probability'].values
                weighted_similarity = np.sum(topic_probability * similarities) if len(topic_probability) > 0 else 0
                university_weighted_similarities.append(weighted_similarity)

            was = np.mean(university_weighted_similarities) if university_weighted_similarities else 0
            unnormalized_results[university] = was
            total_was += was

            # Add results for the current university
            results[university] = {'WAS': unnormalized_results[university] / total_was if total_was > 0 else 0,
                                   'Highest_Prob_Topic': highest_prob_topic,
                                   'Most_Relevant_Review': most_relevant_review}

        return results

    def calculate_confidence_score(self, input_text, topic_data_file='/Users/zhiyue/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/topic_data.npy'):
        topic_embeddings, topic_rates = self.load_topic_data(topic_data_file)
        topic_probabilities_df = self.calculate_topic_probabilities(input_text)

        cs = sum(topic_probabilities_df['topic_probability'] * topic_probabilities_df['sub_topic'].map(topic_rates))

        return cs
    def general_scores(self, input_text):
        weighted_average_similarities = self.calculate_weighted_average_similarity(input_text)
        total_was = sum(was_info['WAS'] for was_info in weighted_average_similarities.values())
        for university, was_info in weighted_average_similarities.items():
            normalized_was = was_info['WAS'] / total_was if total_was > 0 else 0
            weighted_average_similarities[university]['WAS'] = normalized_was
        results_df = pd.DataFrame.from_dict(weighted_average_similarities, orient='index')
        results_df.columns = ['WAS', 'Highest_Prob_Topic', 'Most_Relevant_Review']  # Set column names explicitly
        cs = self.calculate_confidence_score(input_text)
        return results_df

