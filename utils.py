from typing import Callable, Tuple
from pathlib import Path
import random
import re

import streamlit as st


def initialize_state(**kwargs):
    for key, value in kwargs.items():
        if key not in st.session_state:
            st.session_state[key] = value


def table_paginator(df, num_per_page):
    num_rows = len(df)
    num_pages = num_rows / num_per_page
    page_num = st.slider("Page", min_value=0, max_value=num_pages)
    page_df = df.iloc[page_num * num_per_page : (page_num + 1) * num_per_page, :]
    st.table(page_df)


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
    password = st.text_input("Enter a password:")  # , type="password")
    st.button("Sign In", on_click=validate, args=(validation_func, username, password))
    st.stop()


def random_gif(display=True):
    path = Path("celebration_gifs.txt")
    with path.open("r") as f:
        gif_urls = f.readlines()
    random_url = random.choice(gif_urls)
    if display:
        st.image(random_url)
    return random_url
