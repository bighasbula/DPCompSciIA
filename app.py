import streamlit as st
import random
from logic import get_topics, get_types, filter_problems
from problems import problems
st.title("📘 Math Task Finder")

st.write("Choose your preferences and get a math problem.")

# USER INPUT
time_available = st.slider(
    "How much time do you have? (minutes)",
    min_value=5,
    max_value=30,
    value=15
)
level_of_question = st.slider(
    "What level of question do you want?",
    min_value=1,
    max_value=10,
    value=5
)
topic_options = ["Any"] + get_topics()
selected_topic = st.selectbox("Select a topic", topic_options)

type_options = ["Any"] + get_types()
selected_type = st.selectbox("Select problem type", type_options)

timer_options = ["With timer"] + ["No timer"]
selected_timer = st.selectbox("Select your timer preferance", timer_options)

# ACTION
if st.button("Find a problem"):
    matching_problems = filter_problems(
        time_available,
        selected_topic,
        selected_type,
        level_of_question
    )

    if matching_problems:
        chosen = random.choice(matching_problems)
    else:
        st.warning("No problems match your criteria. We chose a random question for you")
        chosen = random.choice(problems)

    st.subheader(chosen["title"])
    st.write(chosen["question"])
    st.caption(
        f'{chosen["topic"]} • {chosen["type"]} • {chosen["time"]} min • level {chosen["level"]}'
    )

    st.session_state["selected_problem"] = chosen
    st.session_state["attempt_answer"] = ""
    st.session_state["submitted"] = False
    st.session_state["is_correct"] = None
    st.session_state["time_on_task"] = None

    if selected_timer == "With timer":
        st.session_state["mode"] = "With timer"
        st.session_state["minutes"] = int(chosen["time"])
    else:
        st.session_state["mode"] = "No timer"
        st.session_state.pop("minutes", None)

    
    st.session_state.pop("start_time", None)
    st.session_state.pop("deadline_ts", None)
    st.session_state.pop("time_up", None)

    st.switch_page("pages/page_1.py")
