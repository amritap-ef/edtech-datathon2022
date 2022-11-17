import streamlit as st
# from content_recomm.paraphrase import load_paraphrase_model, get_paraphrases
from content_recomm.es_recomm_content import _get_elasticsearch_url, recomm_content
from content_recomm.question_answering import get_question_answers

st.set_page_config(page_title="ACR Generation | Datathon 2022", layout="wide")

st.header("After Class Report Generator")

if "elasticsearch_url" not in st.session_state:
    st.session_state.elasticsearch_url = _get_elasticsearch_url()
# if "paraphrase_model" not in st.session_state:
#     st.session_state.paraphrase_model = load_paraphrase_model()

student_name = st.sidebar.text_input("Student Name")
student_cefr_level = st.sidebar.selectbox(
    "Select Student's CEFR Level",
    options=("a1", "a2", "b1", "b2", "c1", "c2")
)
lesson_date = st.sidebar.date_input("Lesson Date")
lesson_topics = st.sidebar.multiselect("Select topics", ["Greeting", "Ordering Food"])

st.sidebar.subheader("\nFeedback Generator")


st.sidebar.subheader("\nHomework Generator")
# st.markdown(
#     """
#     Please enter in the phrases the student struggled with, separated by a new line for each phrase.
# """
# )
phrase_struggled = st.sidebar.text_input("Enter a phrase/topic the student struggled with")

if st.sidebar.button("Generate After Class Report"):
    st.text(f"Student: {student_name}")
    st.text(f"Date: {lesson_date}")
    st.text(f"Lesson Topics: {lesson_topics}")

    st.text(" \n")

    st.subheader("Lesson Feedback")
    feedback = "lorem et ipsum sfsdfs dfsdf sdf sdf sdf sdf sdf sdf "
    st.markdown(feedback)
    st.text(" \n")
    st.subheader("Homework Tasks")

    results = recomm_content(phrase_struggled, student_cefr_level, st.session_state.elasticsearch_url)
    if len(results) == 0:
        st.error("Sorry, was unable to find any content matching the specific phrase.")
    else:
        st.markdown("""---""")
        # st.text(results)
        for i, res in enumerate(results):
            metadata = res["_source"]["metadata"]
            author = metadata["author"]
            headline = metadata["headline"]
            url = metadata["url"]
            cefr = res["_source"]["cefr"]["pred"]
            title = res["_source"]["metadata"]["headline"]
            # topic_1 = res["inner_hits"]["topic_classification"]["hits"]["hits"]

            col1, col2 = st.columns([1,3])
            # col1, col2 = st.columns(2)
            is_article = "youtube" not in url
            with col1:
                if is_article: # TODO
                    icon_fpath = "assets/article_icon.png"
                else:
                    icon_fpath = "assets/video_icon.png"

                st.image(icon_fpath, width=180)
            with col2:
                st.header(headline)
                if author is not None:
                    st.markdown(f"*By: {author}*")
                    # topics = '(' + ', '.join(topic_1_l) + ')'
                    # st.write('**' + cefr + '**', ' - ', '*' + topics + '*')
                st.markdown(f"**{cefr}** - *topics*")
                st.markdown(url)
            st.markdown("\n")

            if is_article:
                article_body_html = metadata["article_body_html"]
                get_question_answers(article_body_html)

            st.markdown("""---""")




# phrases_struggled = st.text_area('Enter phrases', height=275)
# if st.button('Retrieve alternative phrases'):
#     phrases_struggled = phrases_struggled
#     st.write(phrases_struggled)
#     get_paraphrases(st.session_state.paraphrase_model, phrases_struggled)