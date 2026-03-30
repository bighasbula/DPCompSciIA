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
        # mark time up; if not submitted yet, record timed-out result and go to page_2
        if not st.session_state.get("submitted", False) and not st.session_state.get("timed_out_handled", False):
            st.session_state["time_up"] = True
            problem_obj = st.session_state.get("selected_problem", {})
            st.session_state["last_result"] = {
                "correct": False,
                "user_answer": None,
                "correct_answer": problem_obj.get("answer") if problem_obj else None,
                "time_on_task": format_time(int(st.session_state.get("deadline_ts", time.time()) - st.session_state.get("start_time", time.time()))),
                "lapsed_seconds": int(st.session_state.get("deadline_ts", time.time()) - st.session_state.get("start_time", time.time())),
                "problem": problem_obj,
                "timed_out": True,
            }
            st.session_state["timed_out_handled"] = True
            st.switch_page("pages/page_2.py")
        else:
            st.session_state["time_up"] = True

with timer_col:
    if mode == "With timer":
        st.write("Timer")
        # Styled client-side countdown that updates every second.
        deadline_ms = int(float(st.session_state.get("deadline_ts", time.time())) * 1000)
        html = f"""
<style>
  #countdown-wrap {{ display:flex; flex-direction:column; align-items:center; gap:6px; }}
  #countdown-title {{ font-size:13px; color:#666; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }}
  #countdown {{ font-size:28px; font-weight:600; color:#111; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; background:transparent; }}
  #countdown.small-warning {{ color: #b91c1c; }}
</style>
<div id='countdown-wrap'>
  <div id='countdown-title'>Remaining</div>
  <div id='countdown'>--:--:--</div>
</div>
<script>
const deadline = {deadline_ms};
function pad(n) {{ return String(n).padStart(2,'0'); }}
function update() {{
  const now = Date.now();
  let diff = Math.max(0, Math.floor((deadline - now) / 1000));
  let hrs = Math.floor(diff / 3600);
  let mins = Math.floor((diff % 3600) / 60);
  let secs = diff % 60;
  const el = document.getElementById('countdown');
  el.innerText = pad(hrs) + ':' + pad(mins) + ':' + pad(secs);
  if (diff <= 10) {{ el.classList.add('small-warning'); }} else {{ el.classList.remove('small-warning'); }}
  if (diff <= 0) {{ if (!window._reloaded_on_timeout) {{ window._reloaded_on_timeout = true; window.location.reload(); }} }}
}}
update();
setInterval(update, 1000);
</script>
"""
        components.html(html, height=110)
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

    # record last result for page_2
    st.session_state["last_result"] = {
        "correct": st.session_state["is_correct"],
        "user_answer": st.session_state.get("attempt_answer"),
        "correct_answer": problem.get("answer"),
        "time_on_task": st.session_state.get("time_on_task"),
        "lapsed_seconds": lapsed_time,
        "problem": problem,
        "timed_out": False,
    }

    st.switch_page("pages/page_2.py")

nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    if st.button("Back to main page"):
        st.switch_page("app.py")
with nav_col2:
    if st.button("Reset this problem"):
        for k in ["start_time", "deadline_ts", "time_up", "submitted", "is_correct", "time_on_task", "timed_out_handled"]:
            st.session_state.pop(k, None)
        st.session_state["attempt_answer"] = ""
        st.rerun()

# end

