import streamlit as st
# from content_recomm.paraphrase import load_paraphrase_model, get_paraphrases
from feedback_generator.keyword_text_gen_inference import generate_feedback_comments
from content_recomm.es_recomm_content import _get_elasticsearch_url, index_exact_search_relevance_metadata, index_exact_search_relevance_captions
from content_recomm.question_answering import get_question_answers
from streamlit_player import st_player
from demo.helpers import load_obs_topics_data, get_url_caption_youtube

st.set_page_config(page_title="ACR Generation | Datathon 2022", layout="wide")

st.header("After Class Report Generator")

if "elasticsearch_url" not in st.session_state:
    st.session_state.elasticsearch_url = _get_elasticsearch_url()

obs_topics_data = load_obs_topics_data("data/obs_topics_id_processed.csv")
if "unit_titles" not in st.session_state:
    st.session_state.unit_titles = obs_topics_data["unit_title"]
# if "paraphrase_model" not in st.session_state:
#     st.session_state.paraphrase_model = load_paraphrase_model()

student_name = st.sidebar.text_input("Student Name")
student_grade = st.sidebar.number_input("Student Grade", min_value=0, max_value=100)


lesson_date = st.sidebar.date_input("Lesson Date")

student_cefr_level = st.sidebar.selectbox(
    "Select Student's CEFR Level",
    options=("a1", "a2", "b1", "b2", "c1", "c2")
)
lesson_unit = st.sidebar.selectbox("Select unit", st.session_state.unit_titles)
# lesson_topics = st.sidebar.multiselect("Select topics", ["Greeting", "Ordering Food"])

st.sidebar.subheader("\nFeedback Generator")
feedback_topic = st.sidebar.text_input("Topic for feedback")
feedback_keywords = st.sidebar.text_area("Enter keywords, each separated by a line", height=120)
feedback_sentiment = st.sidebar.selectbox("Enter sentiment", options=["Positive", "Negative"])

st.sidebar.subheader("\nHomework Generator")

phrase_struggled = st.sidebar.text_input("Enter a phrase/topic the student struggled with", value=lesson_unit)
content_type = st.sidebar.multiselect("Select content type", ["video", "news"], default=["video", "news"])


# if st.sidebar.button("Generate After Class Report"):
if True:
    lesson_data = obs_topics_data.loc[
            obs_topics_data["unit_title"]==lesson_unit
        ]
    lesson_vocab = "\n\n".join(lesson_data["Vocabulary"].item())
    lesson_objective = lesson_data["Lesson_can-do_(Compass)"].item()
    lesson_topic = lesson_data["lesson_topic"].item()

    st.text(f"Student: {student_name}")
    st.text(f"Date: {lesson_date}")
    st.text(f"Lesson Unit: {lesson_unit}")
    st.text(f"Lesson Topic: {lesson_topic}")
    st.text(f"Lesson Objective: {lesson_objective}")
    st.markdown("""---""")

    st.subheader(f"**Vocabulary of Focus**")
    st.info(lesson_vocab)

    st.text(" \n")

    st.markdown("""---""")
    st.subheader("Lesson Feedback")

    if student_name != "" and student_grade is not None and feedback_topic != "" and feedback_keywords != "" and feedback_sentiment != "":
        # st.markdown("""---""")
        # st.subheader("Lesson Feedback")
        feedback_keywords = feedback_keywords.split("\n")
        feedback = generate_feedback_comments(student_name, student_grade, feedback_topic, feedback_keywords, feedback_sentiment)
        st.markdown(feedback)

    st.markdown("""---""")

    st.text(" \n")
    st.subheader("Homework Tasks")
    st.markdown("**Task 1**")
    st.markdown("Watch the clips below and note how the vocab from this lesson is used in different contexts.")


    display_results = []
    vocab_index = 0
    vocab = lesson_data["Vocabulary"].item()
    max_len_display_results = 3

    for i, keyword in enumerate(vocab):
        results = index_exact_search_relevance_captions(keyword, student_cefr_level, st.session_state.elasticsearch_url)
        if len(results) > 0:
            res = results[0]
            res["vocab"] = keyword
            display_results.append(res)
        if len(results) == max_len_display_results:
            break


    for res in display_results:
        metadata = res["_source"]["metadata"]
        author = metadata["author"]
        headline = metadata["headline"]
        url = metadata["url"]
        cefr = res["_source"]["cefr"]["pred"]

        inner_hits = res["inner_hits"]["captions"]["hits"]["hits"]
        keyword = res['vocab']
        st.markdown("""---""")

        col1, col2 = st.columns(2)

        if len(inner_hits) != 0:
            # display one of each video
            inner_hit = inner_hits[0]
            highlight = inner_hit["highlight"]["captions.text"]
            start_caption_time = inner_hit["_source"]["start"]

            with col2:
                st.header(headline)
                if author is not None:
                    st.markdown(f"*By: {author}*")
                st.markdown(f"**{keyword}**")
                for c in highlight:
                    st.markdown('**' + 'Sentence:' + '** ' + '*' + c + ' *', unsafe_allow_html=True)
            with col1:
                st_player(get_url_caption_youtube(url=url, start=start_caption_time))

    st.markdown("""---""")


    results = index_exact_search_relevance_metadata(phrase_struggled, student_cefr_level, content_type, st.session_state.elasticsearch_url)

    if len(results) == 0:
        st.error("Sorry, was unable to find any content matching the specific phrase.")
    else:
        st.markdown("\n\n")
        st.markdown("**Task 2**")
        st.markdown(
            f"Suggested phrase to work on for the next lesson: *{phrase_struggled}*. \n\n Suggested exercises in your own time: please view/read the following content and answer the comprehension questions.")
        st.markdown("""---""")

        for i, res in enumerate(results):
            metadata = res["_source"]["metadata"]
            author = metadata["author"]
            headline = metadata["headline"]
            url = metadata["url"]
            cefr = res["_source"]["cefr"]["pred"]
            content_type = metadata["type"]
            if "topic_classification" in res["_source"]:
                topics = [t["topic"] for t in res["_source"]["topic_classification"]]
            else:
                topics = []

            col1, col2 = st.columns([2,3])

            st.markdown("""---""")

            with col1:
                if content_type == "news":
                    icon_fpath = "assets/article_icon.png"
                    st.image(icon_fpath, width=180)
                else:
                    st_player(url=url)

            with col2:
                st.header(headline)
                if author is not None:
                    st.markdown(f"*By: {author}*")
                if len(topics) != 0:
                    topics = "(" + ", ".join(topics) + ")"
                    st.markdown(f"**{cefr}** - *{topics}*")
                else:
                    st.markdown(f"**{cefr}**")

                st.markdown(url)

            st.markdown("\n")

            if content_type == "news":
                article_body_html = metadata["article_body_html"]
                get_question_answers(article_body_html)

            # st.markdown("""---""")




# phrases_struggled = st.text_area('Enter phrases', height=275)
# if st.button('Retrieve alternative phrases'):
#     phrases_struggled = phrases_struggled
#     st.write(phrases_struggled)
#     get_paraphrases(st.session_state.paraphrase_model, phrases_struggled)