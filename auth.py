from typing import Callable, Tuple
import re

import streamlit as st


def is_daupler_email(s) -> bool:
    is_match = re.match("([a-z0-9_.]+)@daupler\.com", s)
    return is_match


def convert_username(s: str) -> str:
    s = re.sub("[.@]", "_", s)
    return s


def validate(validation_func, username, password):
    is_valid = validation_func(username, password)
    if is_valid:
        st.session_state["validated_user"] = convert_username(username)


def authentication(validation_func: Callable) -> Tuple[bool, str]:
    username = st.text_input("Enter your email:")
    # password = st.text_input("Enter a password:")  # , type="password")
    password = "asdf"
    st.button("Sign In", on_click=validate, args=(validation_func, username, password))


def is_reviewer(user):
    with open("static/reviewers.txt", "r") as f:
        reviewers = [s.strip() for s in f.readlines()]
    is_in_reviewer_list = user in reviewers
    return is_in_reviewer_list
