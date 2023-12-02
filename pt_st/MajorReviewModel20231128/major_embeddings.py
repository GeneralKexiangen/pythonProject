import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import numpy as np
from collections import Counter
class EmbeddingsCalculator:
    def __init__(self, model_name='bert-base-uncased', csv_file='./majorreview.csv'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.df = pd.read_csv(csv_file)
        self.df['reviews_lemmatized'] = self.df['reviews_lemmatized'].astype(str)

        texts = self.df["reviews_lemmatized"].drop_duplicates()
        tmp = []
        for item in texts.apply(lambda x: x.split()):
            tmp.extend(item)

        users_stop_words = []
        for word, _ in Counter(tmp).most_common(30):
            if word not in stopwords.words('english'):
                users_stop_words.append(word)

        self.stop_words = set(stopwords.words('english') + users_stop_words)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
            embedding = torch.mean(outputs[0], dim=1).cpu().numpy()
            return embedding
        except Exception as e:
            print(f"Error in text_to_bert_embedding: {e}")
            return [[]]

    def load_combined_major_data(self, file_path='/Users/zhiyue/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/combined_major_data.npy'):
        saved_data = np.load(file_path, allow_pickle=True).item()
        return saved_data

    def calculate_topic_probabilities_for_major(self, input_text, pre_saved_data='/Users/zhiyue/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/combined_major_data.npy'):
        saved_data = self.load_combined_major_data(pre_saved_data)
        topic_embeddings = saved_data['topic_embeddings']

        input_text_tokens = self.preprocess(input_text)
        input_text_embedding = self.text_to_bert_embedding(" ".join(input_text_tokens))

        similarities = []
        for _, sub_topic_embedding in topic_embeddings.items():
            similarity = cosine_similarity(input_text_embedding, sub_topic_embedding).squeeze()
            similarities.append(similarity)

        probabilities = np.exp(similarities) / np.sum(np.exp(similarities))

        probabilities_df = pd.DataFrame({
            'sub_topic': list(topic_embeddings.keys()),
            'topic_probability': probabilities
        })

        return probabilities_df

    def calculate_weighted_average_similarity(self, input_text, embedding_file='/Users/zhiyue/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/combined_major_data.npy'):
        saved_data = self.load_combined_major_data(embedding_file)

        input_text_embedding = self.text_to_bert_embedding(input_text)

        probabilities_df = self.calculate_topic_probabilities_for_major(input_text)

        unnormalized_results = {}
        total_was = 0
        results = {}

        for university in set(saved_data['universities']):
            university_indices = [i for i, uni in enumerate(saved_data['universities']) if uni == university]
            university_weighted_similarities = []
            max_similarity = 0
            most_relevant_review = ''
            highest_prob_topic = ''

            for i in university_indices:
                review_embedding = saved_data['review_embeddings'][i]
                assigned_topic = saved_data['assigned_topics'][i]

                if assigned_topic not in saved_data['topic_embeddings']:
                    continue

                similarity = cosine_similarity(np.atleast_2d(input_text_embedding), np.atleast_2d(review_embedding))[0][0]

                topic_probability = probabilities_df[probabilities_df['sub_topic'] == assigned_topic]['topic_probability'].values
                if len(topic_probability) > 0:
                    weighted_similarity = topic_probability[0] * similarity
                    university_weighted_similarities.append(weighted_similarity)

                    if similarity > max_similarity:
                        max_similarity = similarity
                        most_relevant_review = saved_data['reviews'][i]
                        highest_prob_topic = assigned_topic

            was = np.mean(university_weighted_similarities) if university_weighted_similarities else 0
            unnormalized_results[university] = was
            total_was += was
            results[university] = {'WAS': unnormalized_results[university] / total_was if total_was > 0 else 0,
                                   'Highest_Prob_Topic': highest_prob_topic,
                                   'Most_Relevant_Review': most_relevant_review}
        return results

    def calculate_confidence_score(self, input_text, embedding_file='/Users/zhiyue/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/combined_major_data.npy'):
        saved_data = self.load_combined_major_data(embedding_file)
        topic_probabilities_df = self.calculate_topic_probabilities_for_major(input_text)

        cs = sum(topic_probabilities_df['topic_probability'] * topic_probabilities_df['sub_topic'].map(saved_data['topic_rates']))

        return cs

    def major_scores(self, input_text):
        major_weighted_average_similarities = self.calculate_weighted_average_similarity(input_text)
        total_was = sum(was_info['WAS'] for was_info in major_weighted_average_similarities.values())
        for university, was_info in major_weighted_average_similarities.items():
            normalized_was = was_info['WAS'] / total_was if total_was > 0 else 0
            major_weighted_average_similarities[university]['WAS'] = normalized_was
        results_df = pd.DataFrame.from_dict(major_weighted_average_similarities, orient='index')
        results_df.columns = ['WAS', 'Highest_Prob_Topic', 'Most_Relevant_Review']
        cs = self.calculate_confidence_score(input_text)

        return results_df


