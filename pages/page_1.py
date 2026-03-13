import time

import streamlit as st
import streamlit.components.v1 as components

from logic import check_answer


def format_time(seconds: int) -> str:
    mins, secs = divmod(max(0, int(seconds)), 60)
    hours, mins = divmod(mins, 60)
    return f"{int(hours):02}:{int(mins):02}:{int(secs):02}"


if "selected_problem" not in st.session_state:
    st.warning("No problem selected yet.")
    if st.button("Back to main page"):
        st.switch_page("app.py")
    st.stop()

problem = st.session_state["selected_problem"]
mode = st.session_state.get("mode", "No timer")

if "attempt_answer" not in st.session_state:
    st.session_state["attempt_answer"] = ""
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.time()

if mode == "With timer":
    if "deadline_ts" not in st.session_state:
        minutes = int(st.session_state.get("minutes", problem.get("time", 0)))
        st.session_state["deadline_ts"] = st.session_state["start_time"] + minutes * 60
    if "time_up" not in st.session_state:
        st.session_state["time_up"] = False

st.title("📘 Your math task")
st.subheader(problem.get("title", "Problem"))
st.write(problem["question"])
st.caption(f'{problem["topic"]} • {problem["type"]} • {problem["time"]} min • level {problem["level"]}')

timer_col, stats_col = st.columns([1, 2])

elapsed = int(time.time() - st.session_state["start_time"])
with stats_col:
    st.write(f"Time on task: **{format_time(elapsed)}**")

running_timer = (mode == "With timer") and (not st.session_state.get("submitted", False))
remaining = None
if mode == "With timer":
    remaining = int(st.session_state["deadline_ts"] - time.time())
    if remaining <= 0:
        remaining = 0
        st.session_state["time_up"] = True

with timer_col:
    if mode == "With timer":
        st.write("Timer")
        st.metric("Remaining", format_time(remaining))
        if st.session_state.get("time_up", False) and not st.session_state.get("submitted", False):
            st.error("Time is up. Submission is locked.")
    else:
        st.write("Timer")
        st.metric("Mode", "No timer")

st.divider()

answer_disabled = bool(st.session_state.get("submitted", False)) or bool(st.session_state.get("time_up", False))
st.text_input("Your answer", key="attempt_answer", disabled=answer_disabled)

submit_disabled = answer_disabled or (not str(st.session_state.get("attempt_answer", "")).strip())
if st.button("Submit a solution", disabled=submit_disabled):
    now = time.time()
    lapsed_time = int(now - st.session_state["start_time"])
    st.session_state["time_on_task"] = format_time(lapsed_time)

    is_correct = check_answer(st.session_state.get("attempt_answer", ""), problem["answer"])
    st.session_state["is_correct"] = bool(is_correct)
    st.session_state["submitted"] = True

    st.switch_page("pages/page_2.py")

nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    if st.button("Back to main page"):
        st.switch_page("app.py")
with nav_col2:
    if st.button("Reset this problem"):
        for k in ["start_time", "deadline_ts", "time_up", "submitted", "is_correct", "time_on_task"]:
            st.session_state.pop(k, None)
        st.session_state["attempt_answer"] = ""
        st.rerun()

# Non-blocking timer: refresh the script once per second while the timer is running.
if running_timer and remaining is not None and remaining > 0 and not st.session_state.get("time_up", False):
    components.html("<meta http-equiv='refresh' content='1'>", height=0, width=0)

