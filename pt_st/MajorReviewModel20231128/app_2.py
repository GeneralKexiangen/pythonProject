import streamlit as st
import pandas as pd
import random
from major_embeddings import EmbeddingsCalculator
from embeddings import allEmbeddingsCalculator

def get_mcs(input_text):
    ta = EmbeddingsCalculator(model_name='bert-base-uncased', csv_file='/MajorReviewModel20231128/majorreview.csv')
    # input_text = "make more friend with high academic performance"
    cs = ta.calculate_confidence_score(input_text)
    print(cs)
    return cs

def get_gcs(input_text):
    ta = allEmbeddingsCalculator()
    # input_text = "make more friend with high academic performance"
    cs = ta.calculate_confidence_score(input_text)
    print(cs)
    return cs

def get_ms(input_text):
    ta = EmbeddingsCalculator(model_name='bert-base-uncased', csv_file='/MajorReviewModel20231128/majorreview.csv')
    # input_text = "make more friend with high academic performance"
    major_scores = ta.major_scores(input_text)
    print(major_scores)
    return major_scores

def get_gs(input_text):
    ta = allEmbeddingsCalculator()
    # input_text = "make more friend with high academic performance"
    gs = ta.general_scores(input_text)
    print(gs)
    return gs


st.set_page_config(
    page_title="Reach Best LUR Bot", layout="centered", page_icon="logo.png", initial_sidebar_state="collapsed"
)
st.write(
    '<div style="text-align: center;">'
    '<h1 style="color: #E1930F;">Reach Best LUR Bot</h1>'
    '</div>',
    unsafe_allow_html=True)

description = """
<div style='font-size: 24px; text-align: center;'>
    Find Universities that match with you based on your ideal college life
</div>
"""
st.markdown(description, unsafe_allow_html=True)

ID_weight = pd.read_csv('/MajorReviewModel20231128/ID weight_review.csv')
# loaded_embeddings = np.load('../../../../Downloads/major review model/reviews_embedding_bert.npy', allow_pickle=True).item()
# loaded_embeddings_major = np.load('../../../../Downloads/major review model/reviews_embedding_major_bert.npy', allow_pickle=True).item()


# def preprocess(text, tokenizer):
#     stop_words = set(stopwords.words('english'))
#     words = tokenizer.tokenize(text.lower())
#     return [w for w in words if w not in stop_words]


# def text_to_bert_embedding(text, model, tokenizer):
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model = model.to(device)
#     try:
#         tokens = tokenizer.encode(text, add_special_tokens=True)
#         input_ids = torch.tensor(tokens).unsqueeze(0).to(device)
#         with torch.no_grad():
#             outputs = model(input_ids)
#         embedding = torch.mean(outputs.last_hidden_state, dim=1).cpu().numpy()
#         return embedding
#     except:
#         return [[]]

with st.sidebar:
    # with open("style.css") as f:  # change up the sidebar styling
    #    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.markdown(
           """
           <a href="https://app.reachbest.co/signup">
               <img src="https://i.imgur.com/CMfb6aI.png" style="max-width: 100%;">
           </a>
           """,
           unsafe_allow_html=True,
        )

    st.divider()
  
    st.info("To access the official chat bot trained for over 1000+ Universities, check out [Reach Best](https://app.reachbest.co/signup)!", icon="🧠")
# ID_weight = pd.read_csv('../../../../Downloads/major review model/ID weight_review.csv')
# loaded_embeddings = np.load('../../../../Downloads/major review model/reviews_embedding_bert.npy', allow_pickle=True).item()
# loaded_embeddings_major = np.load('../../../../Downloads/major review model/reviews_embedding_major_bert.npy', allow_pickle=True).item()
col4, col5 = st.columns([5, 5])
with col4:
    username = st.text_input(
        label="Save your personalized model",
        placeholder="Enter your name"
    )

with col5:
    major_options = ['architecture_design', 'biology', 'computer.science',
                     'electrical.engineering', 'english.language.and.literature',
                     'linguistics', 'history', 'development.studies', 'philosophy',
                     'physics', 'psychology', 'political.science', 'sociology',
                     'accounting.and.finance', 'communication_info', 'economics',
                     'archeology', 'agriculture_environment', 'education', 'arts',
                     'medicine_health', 'chemical.engineering', 'theology_theater',
                     'law', 'mechanical.engineering', 'sports.sciences.and.management',
                     'civil.engineering', 'geography']

    sorted_major_options = sorted(major_options)

    major = st.selectbox(
        'Select Major',
        sorted_major_options)
bullet_col1, bullet_col2 = st.columns(2, gap="large")

with bullet_col1:
    st.markdown("##### General Aspects:")
    bullet_list = """
    - <span class="copyable-text">Policy of Administration and Financial Aid</span>
    - <span class="copyable-text" >Career and Academic Opportunities</span>
    - <span class="copyable-text" >Academic Quality and online learning</span>
    - <span class="copyable-text" >Admission</span>
    - <span class="copyable-text">Diversity and Inclusion</span>
    - <span class="copyable-text">Technology and Computer Labs</span>
    """
    st.markdown(bullet_list, unsafe_allow_html=True)

major_topics = [
    "Academic Excellence and Opportunities",
    "Social networks and Campus Atmosphere",
    "Dynamics and individual experiences",
    "Campus Beauty and Resources",
    "Transfer Student Experience",
    "Career and Major Focus"
]

with bullet_col2:
    st.markdown("##### Major specific Aspects:")
    bullet_list = "\n".join(f"- <span class='copyable-text'>{topic}</span>" for topic in major_topics)
    st.markdown(bullet_list, unsafe_allow_html=True)

general_questions = [
    "What type of friends do you get along with and why?",
    "What’s your favorite season of the year and why? Do you prefer sunny, cloudy, rainy or snowy days?",
    "What do you like doing for fun? What type of places do you like hanging out at and why?",
    "What is the one thing you love the most about school and why?",
    "Do you prefer to dress casually or more formally and why?"
    # ... any other questions 
]
major_questions = [
    "Who is your favorite teacher and why?",
    "Do you prefer taking exams or writing research papers? Why?",
    "Would you rather be the only student in a super advanced class or be in a group class where you learn at the same rhythm with your classmates? Why?"
    # ... any other questions 
]
if 'random_question1' not in st.session_state:
    st.session_state['random_question1'] = random.choice(general_questions)
if 'random_question2' not in st.session_state:
    st.session_state['random_question2'] = random.choice(major_questions)
question = "Describe your ideal college in the above left side aspects:"
question2 = "Describe your ideal college in the above right side aspects:"
# answer1 = st.text_input(st.session_state['random_question1'], key="text_area1", placeholder="Write here")
answer1 = st.text_input(question, key="text_area1", placeholder="Write here")
if answer1:
    cs = get_mcs(answer1)
    # st.write('cs: '+str(cs))
    st.info(
        f'How confident is the model? \n\nBased on your major-specific answer, our confidence score is **{cs}%** ',
        icon="ℹ")
# answer2 = st.text_input(st.session_state['random_question2'], key="text_area2",placeholder='Write here')
answer2 = st.text_input(question2, key="text_area2",placeholder='Write here')
if answer2:
    cs = get_gcs(answer2)
    # st.write('cs: '+str(cs))
    st.info(
        f'How confident is the model? \n\nBased on your general ideal college answer, our confidence score is **{cs}%** .',
        icon="ℹ")

if username:
    if username in ID_weight["name"].tolist():
        user_data = ID_weight[ID_weight["name"] == username].iloc[-1]

        user_last_answers = pd.DataFrame({
            'Category': ['General College Life', 'Major Specific Life'],
            'Your Last Answer': [user_data["lastphrase1"], user_data["lastphrase2"]]
        })

        st.write(user_last_answers.to_html(index=False), unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)

        weight_flag = float(user_data["Model1weight"]) if 'Model1weight' in user_data and isinstance(user_data["Model1weight"], (int, float)) else 0.5
    else:
        weight_flag = 0.5
        st.write("No previous data found for user: {}".format(username))

    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        st.write("<p style='text-align: center'>Major specific</p>", unsafe_allow_html=True)
    with col2:
        weight = st.slider('Adjust your preference', 0.0, 1.0, weight_flag, label_visibility='collapsed')
    with col3:
        st.write("<p style='text-align: center'>General review</p>", unsafe_allow_html=True)


if st.button("Recommend"):
    if not username:
        st.warning("Please enter your name.")
    elif not answer1 or not answer2:
        st.warning("Please provide answers for both text inputs.")
    else:
        pd.concat([ID_weight, pd.DataFrame(
            [username, weight, 1 - weight,
             answer1, answer2], index=ID_weight.columns).T],
                  ignore_index=True).to_csv(
            '/MajorReviewModel20231128/ID weight_review.csv', index=False)
        with st.spinner('Running...'):

            df = get_gs(input_text=answer1)
            df = df.reset_index()
            df.columns = ['University', 'WAS', 'Highest_Prob_Topic', 'Most_Relevant_Review']

            df_major = get_ms(input_text=answer1)
            df_major = df_major.reset_index()
            df_major.columns = ['University', 'WAS', 'Highest_Prob_Topic', 'Most_Relevant_Review']

            df_copy = df.set_index('University')
            df_was2 = df_copy[['WAS']]
            df_was2.columns = ['WAS2']
            df_major_copy = df_major.set_index('University')
            df_was1 = df_major_copy[['WAS']]
            df_was1.columns = ['WAS1']

            df_final = pd.concat([df_was1,df_was2],axis=1).reset_index()
            df_final['WAS'] = df_final['WAS1']*weight+df_final['WAS2']*(1-weight)
            df_final = df_final.sort_values(by='WAS', ascending=False)[:7].reset_index().reset_index()

            # df = df.drop('reviews', axis=1).groupby('University').mean().sort_values(by='similarities')
            # df_major = df_major.drop('reviews', axis=1).groupby('University').mean().sort_values(by='similarities')
            # df_final = df+df_major
            # df_final = pd.concat([df_final.sort_values(by='similarities', ascending=False)[:7], df_major, df], axis=1)[:7].reset_index().reset_index()
            df_final["index"] = df_final["level_0"]+1
            df_final = df_final[['index','University','WAS1','WAS2','WAS']]
            df_final.columns = ["Rank", "University",  "Major Review Prob.", "General Review Prob.","Weighted Avg."]

            st.success("✅Recommend success")
            st.dataframe(df_final, use_container_width=True, hide_index=True)

            selected_university = st.selectbox("Select a University to view reviews:", df_final["University"].unique())
            # Display reviews for the selected university
            # if 'selected_university' not in st.session_state:
            #     st.session_state['selected_university'] = random.choice(selected_university)
            if selected_university:
                st.write(f"### Reviews for {selected_university}:")
                # general_review = df_copy.loc[selected_university].sort_values(by='WAS', ascending=False)['Most_Relevant_Review'].values[0]
                # major_review = df_major_copy.loc[selected_university].sort_values(by='WAS', ascending=False)['Most_Relevant_Review'].values[0]

                general_review = df[df['University'] == selected_university]['Most_Relevant_Review'].values[0]
                general_topic = df[df['University'] == selected_university]['Highest_Prob_Topic'].values[0]
                major_review = df_major[df_major['University'] == selected_university]['Most_Relevant_Review'].values[0]
                major_topic = df_major[df_major['University'] == selected_university]['Highest_Prob_Topic'].values[0]

                st.write("#### General Review:")
                st.write(general_review)
                st.write("#### General Topic:")
                st.write(general_topic)

                st.write("#### Major-Specific Review:")
                st.write(major_review)
                st.write("#### Major-Specific Topic:")
                st.write(major_topic)

#             st.success("✅Recommend success")
#             st.dataframe(df_final, use_container_width=True, hide_index=True)
#             selected_university = st.selectbox("Select a University to view reviews:", df_final["University"].unique())
#             def update_selected_university():
#                 st.session_state.selected_university = st.session_state.university_selector

#             # Dropdown for selecting a university
            if 'selected_university' not in st.session_state:
                st.session_state.selected_university = None

            st.session_state.university_selector = st.selectbox(
                "Select a University to view reviews:",
                df_final["University"].unique(),
                key='university_selector',
                on_change=update_selected_university
            )
            selected_university = st.session_state.selected_university

#             # Display reviews for the selected university
#
#             if selected_university:
#                 st.write(f"### Reviews for {selected_university}:")
#                 general_review = df_copy.loc[selected_university].sort_values(by='similarities', ascending=False)['reviews'].values[0]
#                 major_review = df_major_copy.loc[selected_university].sort_values(by='similarities', ascending=False)['reviews'].values[0]

#                 st.write("#### General Review:")
#                 st.write(general_review)

#                 st.write("#### Major-Specific Review:")
#                 st.write(major_review)

#             for name in df_final["University"]:
#                 with st.expander(name):
#                     st.write(df_copy.loc[name].sort_values(by='similarities', ascending=False)['reviews'].values[0])
#                     st.write(df_major_copy.loc[name].sort_values(by='similarities', ascending=False)['reviews'].values[0])
st.markdown(
    "<p style='text-align:center; color: #C5C5C5;'>Free prototype preview. AI may sometimes provide innacurate "
    "information. This model was trained on Nich reviews and Rate My Professors Reviews. "
    "</p>",
    unsafe_allow_html=True,
)
