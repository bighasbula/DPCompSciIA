import streamlit as st


st.title("📊 Result")

if "selected_problem" not in st.session_state:
    st.warning("No active attempt found.")
    if st.button("Back to main page"):
        st.switch_page("app.py")
    st.stop()

problem = st.session_state["selected_problem"]
is_correct = st.session_state.get("is_correct", None)
time_on_task = st.session_state.get("time_on_task", None)
user_answer = st.session_state.get("attempt_answer", "")

st.subheader(problem.get("title", "Problem"))
st.write(problem["question"])
st.divider()

if is_correct is True:
    st.success("Correct!")
elif is_correct is False:
    st.error("Not quite.")
    st.write(f'Correct answer: **{problem["answer"]}**')
else:
    st.info("No submission recorded yet.")

st.write(f"Your answer: **{user_answer if str(user_answer).strip() else '(empty)'}**")
if time_on_task:
    st.write(f"Time on task: **{time_on_task}**")

st.divider()

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("Try again (same problem)"):
        for k in ["start_time", "deadline_ts", "time_up", "submitted", "is_correct", "time_on_task"]:
            st.session_state.pop(k, None)
        st.session_state["attempt_answer"] = ""
        st.switch_page("pages/page_1.py")

with col2:
    if st.button("Pick a new problem"):
        for k in [
            "selected_problem",
            "attempt_answer",
            "submitted",
            "is_correct",
            "time_on_task",
            "start_time",
            "deadline_ts",
            "time_up",
            "minutes",
            "mode",
        ]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")

with col3:
    if st.button("View problem again"):
        st.switch_page("pages/page_1.py")
