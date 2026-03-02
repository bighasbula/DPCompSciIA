import streamlit as st
from logic import check_answer
import time
import datetime



if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time() 

if 'tab_start_times' not in st.session_state:
    st.session_state.tab_start_times = {}

def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{int(hours):02}:{int(mins):02}:{int(secs):02}"

def count_down(ts):
    with st.empty():

        while ts:
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.header(f"{time_now}")
            time.sleep(1)
            ts -= 1
        st.write("Time Up!")

        
        


if st.session_state["mode"]=="With timer":
    mode = "With timer"
    
else:
    mode = "No timer"


    
st.title("📘 Your math task")
problem = st.session_state["selected_problem"]
st.write(problem["question"])



math_answer = st.text_input("Your answer")

if st.button("Submit a solution"):
    if mode == "No timer":
        current_time = time.time()
        lapsed_time = current_time - st.session_state.start_time
    st.session_state["time_on_task"]= format_time(lapsed_time)
    

    

    if check_answer(math_answer, problem["answer"]):
        st.success("correct")

    else:
        st.error("Wrong")
        st.write("Correct answer:", problem["answer"])

if st.button("back to main page"):
    st.switch_page("app.py")

if mode == "With timer":
    time_in_seconds = st.session_state["minutes"]*60
    count_down(int(time_in_seconds))

