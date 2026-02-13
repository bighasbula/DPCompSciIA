from problems import problems
import random

def get_topics():
    topics = set()
    for problem in problems:
        topics.add(problem["topic"])
    return sorted(list(topics))

def get_types():
    types = set()
    for problem in problems:
        types.add(problem["type"])
    return sorted(list(types))

def filter_problems(max_time, topic, type, level):
    filtered=[]
    for problem in problems:
        if(problem["time"]<=max_time):
            if(problem["topic"]=="Any" or problem["topic"]==topic):
                if(problem["type"]=="Any" or problem["type"]==type):
                    if(problem["level"]<=level):
                        filtered.append(problem)
    return filtered