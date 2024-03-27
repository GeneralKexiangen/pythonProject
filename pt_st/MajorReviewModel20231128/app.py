import streamlit as st
import pandas as pd
import random
from major_embeddings import EmbeddingsCalculator
from embeddings import allEmbeddingsCalculator
# embeddings_calculator = allEmbeddingsCalculator()


def get_mcs(input_text):
    ta = EmbeddingsCalculator(model_name='bert-base-uncased')
    cs = ta.calculate_confidence_score(input_text)
    print(cs)
    return cs

def get_gcs(input_text):
    ta = allEmbeddingsCalculator()
    cs = ta.calculate_confidence_score(input_text)
    print(cs)
    return cs

def get_ms(input_text):
    ta = EmbeddingsCalculator(model_name='bert-base-uncased')
    major_scores = ta.major_scores(input_text)
    print(major_scores)
    return major_scores

# def get_gs(input_text):
#     ta = allEmbeddingsCalculator()
#     gs = ta.general_scores(input_text)
#     print(gs)
#     return gs
# def weighted_accuracy(input_text, embeddings_calculator):
#     topic_probabilities_df = embeddings_calculator.calculate_topic_probabilities(input_text)
#     topic_probabilities_df = topic_probabilities_df[topic_probabilities_df['sub_topic'] != 'Student opportunities']
#     total_probability = topic_probabilities_df['topic_probability'].sum()
#     topic_probabilities_df['normalized_probability'] = topic_probabilities_df['topic_probability'] / total_probability
#     accuracy_df = pd.read_csv('accuracy_per_sub_topic.csv')
#     accuracy_df['Accuracy'] = pd.to_numeric(accuracy_df['Accuracy'], errors='coerce')
#     accuracy_dict = accuracy_df.set_index('Sub_Topic')['Accuracy'].to_dict()
#     weighted_avg_accuracy = sum(
#         topic_probabilities_df['normalized_probability'] *
#         topic_probabilities_df['sub_topic'].apply(lambda topic: accuracy_dict.get(topic, 0))
#     )
#     return weighted_avg_accuracy

st.set_page_config(
    page_title="Reach Best LUR Bot", layout="centered", page_icon="logo.png", initial_sidebar_state="expanded"
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

ID_weight = pd.read_csv('/Users/kehaigen/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/ID weight_review.csv')


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

    # st.divider()
  
    st.info("To access the official chat bot trained for over 1000+ Universities, check out [Reach Best](https://app.reachbest.co/signup)!", icon="🧠")
    bullet_col1, bullet_col2 = st.columns(2, gap="large")
    major_topics = [
        "Academic Excellence and Opportunities",
        "Social networks and Campus Atmosphere",
        "Dynamics and individual experiences",
        "Campus Beauty and Resources",
        "Transfer Student Experience",
        "Career and Major Focus"
    ]

    bullet_col1, bullet_col2 = st.columns(2)

    with bullet_col1:
        with st.expander("General Aspects:", expanded=False):
            general_aspects = """
            - <span class="copyable-text">Policy of Administration and Financial Aid</span>
            - <span class="copyable-text" >Career and Academic Opportunities</span>
            - <span class="copyable-text" >Academic Quality and online learning</span>
            - <span class="copyable-text" >Admission</span>
            - <span class="copyable-text">Diversity and Inclusion</span>
            - <span class="copyable-text">Technology and Computer Labs</span>
            """
            st.markdown(general_aspects, unsafe_allow_html=True)

    with bullet_col2:
        with st.expander("Major Specific Aspects:", expanded=False):
            major_specific_aspects = "\n".join(f"- <span class='copyable-text'>{topic}</span>" for topic in major_topics)
            st.markdown(major_specific_aspects, unsafe_allow_html=True)




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


general_questions = [
    "What type of friends do you get along with and why?",
    "What’s your favorite season of the year and why? Do you prefer sunny, cloudy, rainy or snowy days?",
    "What do you like doing for fun? What type of places do you like hanging out at and why?",
    "What is the one thing you love the most about school and why?",
    "Do you prefer to dress casually or more formally and why?"
]
major_questions = [
    "Who is your favorite teacher and why?",
    "Do you prefer taking exams or writing research papers? Why?",
    "Would you rather be the only student in a super advanced class or be in a group class where you learn at the same rhythm with your classmates? Why?"
]
if 'random_question1' not in st.session_state:
    st.session_state['random_question1'] = random.choice(general_questions)
if 'random_question2' not in st.session_state:
    st.session_state['random_question2'] = random.choice(major_questions)
question = "Describe your ideal college in the above left side aspects:"
question2 = "Describe your ideal college in the above right side aspects:"
answer1 = st.text_input(question, key="text_area1", placeholder="Write here")

# answer2 = st.text_input(st.session_state['random_question2'], key="text_area2",placeholder='Write here')
answer2 = st.text_input(question2, key="text_area2",placeholder='Write here')

if username:
    if username in ID_weight["name"].tolist():
        user_data = ID_weight[ID_weight["name"] == username].iloc[-1]

        user_last_answers = pd.DataFrame({
            'Category': ['General College Life', 'Major Specific Life'],
            'Your Last Answer': [user_data["lastphrase1"], user_data["lastphrase2"]]
        })

        st.write(user_last_answers.to_html(index=False), unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)

        weight_flag= float(user_data["Model1weight"]) if 'Model1weight' in user_data and isinstance(user_data["Model1weight"], (int, float)) else 0.5
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

if 'test' not in st.session_state:
    st.session_state.test = 0
sslist = ['selected_university','df','df_major','df_final','weight','cs1','cs2']
for ss in sslist:
    if ss not in st.session_state:
        st.session_state[ss] = None
# if 'selected_university' not in st.session_state:
#     st.session_state.selected_university = None
# if 'df' not in st.session_state:
#     st.session_state.df = None
# if 'df_major' not in st.session_state:
#     st.session_state.df_major = None
# if 'df_final' not in st.session_state:
#     st.session_state.df_final = None
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
            '/Users/kehaigen/PycharmProjects/pythonProject/pt_st/MajorReviewModel20231128/ID weight_review.csv', index=False)
        with st.spinner('Running...'):

            df = get_ms(input_text=answer1)
            df = df.reset_index()
            df.columns = ['University', 'WAS', 'Highest_Prob_Topic', 'Most_Relevant_Review']

            df_major = get_ms(input_text=answer2)
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

            df_final["index"] = df_final["level_0"]+1
            df_final = df_final[['index','University','WAS1','WAS2','WAS']]
            df_final.columns = ["Rank", "University",  "Major Review Prob.", "General Review Prob.","Weighted Avg."]
            st.success("✅Recommend success")
            cs1 = get_mcs(answer1)
            cs2 = get_gcs(answer2)

            if df_final is not None:
                st.session_state.df_final = df_final
                st.session_state.test += 1
            if df is not None:
                st.session_state.df = df
            if df_major is not None:
                st.session_state.df_major = df_major
            if weight is not None:
                st.session_state.weight = weight
            if cs1 is not None:
                st.session_state.cs1 = cs1
            if cs2 is not None:
                st.session_state.cs2 = cs2

if st.session_state.test >= 1:
    st.dataframe(st.session_state.df_final, use_container_width=True, hide_index=True)
    st.info(
        f'How confident is the model? \n\nBased on your major-specific answer, our topic related weight average accuracy is  **{100 * round((0.28 * (1 - st.session_state.weight) + 0.38 * st.session_state.weight), 2)}%** ',
        icon="ℹ")
    st.info(
        f'The relevance of your major-specific to our reviews data is **{round(st.session_state.cs1 * 100, 2)}%**\n\nThe relevance of your major-specific to our reviews data is **{round(st.session_state.cs2 * 100, 2)}%**',
        icon="ℹ")

    selected_university = st.selectbox("Select a University to view reviews:", st.session_state.df_final["University"].unique())
    st.session_state.selected_university=selected_university

    if st.session_state.selected_university:
        general_review = st.session_state.df[st.session_state.df['University'] == st.session_state.selected_university]['Most_Relevant_Review'].values[0]
        general_topic = st.session_state.df[st.session_state.df['University'] == st.session_state.selected_university]['Highest_Prob_Topic'].values[0]
        major_review = st.session_state.df_major[st.session_state.df_major['University'] == st.session_state.selected_university]['Most_Relevant_Review'].values[0]
        major_topic = st.session_state.df_major[st.session_state.df_major['University'] == st.session_state.selected_university]['Highest_Prob_Topic'].values[0]

        st.write("🎓"+general_topic)
        st.write("- \"" + general_review + "\"\n")
        st.write("📚"+major_topic)
        st.write("- \"" + major_review + "\"\n")


st.markdown(
    "<p style='text-align:center; color: #C5C5C5;'>Free prototype preview. AI may sometimes provide innacurate "
    "information. This model was trained on Nich reviews and Rate My Professors Reviews. "
    "</p>",
    unsafe_allow_html=True,
)
