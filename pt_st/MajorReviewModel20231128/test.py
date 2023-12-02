import streamlit as st
import pandas as pd

if 'test' not in st.session_state:
    st.session_state.test = 0
sslist = ['selected_university','df','df_major','df_final']
for ss in sslist:
    if ss not in st.session_state:
        st.session_state[ss] = None

question = "Describe your ideal college in the above left side aspects:"
question2 = "Describe your ideal college in the above right side aspects:"
answer1 = st.text_input(question, key="text_area1", placeholder="Write here")

# answer2 = st.text_input(st.session_state['random_question2'], key="text_area2",placeholder='Write here')
answer2 = st.text_input(question2, key="text_area2",placeholder='Write here')

if st.button("Recommend"):
    with st.spinner('Running...'):

        df = [['Boston University',50,'hello world','hellp streamlit'],['Yale University',30,'hello world1','hellp streamlit1']]
        # df = df.reset_index()
        df = pd.DataFrame(df)
        df.columns = ['University', 'WAS', 'Highest_Prob_Topic', 'Most_Relevant_Review']

        df_major = [['Yale University',60,'hello world','hellp streamlit'],['Boston University',65,'hello world2','hellp streamlit2']]
        # df_major = df_major.reset_index()
        df_major = pd.DataFrame(df_major)
        df_major.columns = ['University', 'WAS', 'Highest_Prob_Topic', 'Most_Relevant_Review']

        df_copy = df.set_index('University')
        df_was2 = df_copy[['WAS']]
        df_was2.columns = ['WAS2']
        df_major_copy = df_major.set_index('University')
        df_was1 = df_major_copy[['WAS']]
        df_was1.columns = ['WAS1']

        df_final = pd.concat([df_was1, df_was2], axis=1).reset_index()
        df_final['WAS'] = df_final['WAS1'] * 0.6 + df_final['WAS2'] * (1 - 0.4)
        df_final = df_final.sort_values(by='WAS', ascending=False)[:7].reset_index().reset_index()

        df_final["index"] = df_final["level_0"] + 1
        df_final = df_final[['index', 'University', 'WAS1', 'WAS2', 'WAS']]
        df_final.columns = ["Rank", "University", "Major Review Prob.", "General Review Prob.", "Weighted Avg."]

        st.success("✅Recommend success")
        if df_final is not None:
            st.session_state.df_final = df_final
            st.session_state.test += 1
        if df is not None:
            st.session_state.df = df
        if df_major is not None:
            st.session_state.df_major = df_major
if st.session_state.test >= 1:
    st.dataframe(st.session_state.df_final, use_container_width=True, hide_index=True)
    st.info(
        f'How confident is the model? \n\nBased on your major-specific answer, our topic related weight average accuracy is  **{100 * round((0.28 * (1 - 0.5) + 0.38 * 0.5), 2)}%** ',
        icon="ℹ")
    # cs1 = get_mcs(answer1)
    # cs2 = get_gcs(answer2)
    # st.info(
    #     f'The relevance of your major-specific to our reviews data is **{round(cs2 * 100, 2)}%**\n\nThe relevance of your major-specific to our reviews data is **{round(cs2 * 100, 2)}%**',
    #     icon="ℹ")
    selected_university = st.selectbox("Select a University to view reviews:",
                                       st.session_state.df_final["University"].unique())
    st.session_state.selected_university = selected_university

    if st.session_state.selected_university:
            general_review = \
            st.session_state.df[st.session_state.df['University'] == st.session_state.selected_university][
                'Most_Relevant_Review'].values[0]
            general_topic = \
            st.session_state.df[st.session_state.df['University'] == st.session_state.selected_university][
                'Highest_Prob_Topic'].values[0]
            major_review = st.session_state.df_major[
                st.session_state.df_major['University'] == st.session_state.selected_university][
                'Most_Relevant_Review'].values[0]
            major_topic = st.session_state.df_major[
                st.session_state.df_major['University'] == st.session_state.selected_university][
                'Highest_Prob_Topic'].values[0]

            st.write("🎓" + general_topic)
            st.write("- \"" + general_review + "\"\n")
            st.write("📚" + major_topic)
            st.write("- \"" + major_review + "\"\n")
