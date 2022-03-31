from datetime import date
from pathlib import Path
import random

import streamlit as st


def profile_info(user):
    st.write(f"Username: {user}")


def session_info(repo, goals: str = ""):
    session_num = 2
    session_title = "Wifi, Downed Poles, and Debris, Oh My!"
    st.header(f"Labeling Session #{session_num}: {session_title}")
    today = date.today()
    st.subheader(today.strftime("%B %d, %Y"))
    if goals != "":
        with st.expander("Session Goals"):
            st.write("Goals...")


def vocab_dictionary(vocab):
    filter_phrase = st.text_input("Search", "")
    d0_contains = vocab["D0"].str.contains(filter_phrase, case=False)
    d1_contains = vocab["D1"].str.contains(filter_phrase, case=False)
    def_contains = vocab["Definition"].str.contains(filter_phrase, case=False)
    prefix = "Description whose central theme"
    filtered_df = vocab[d0_contains | d1_contains | def_contains]
    df_display = filtered_df.rename(columns={"Definition": f"Definition: {prefix}..."})
    df_display = df_display.replace(prefix + " ", "...", regex=True)
    st.table(df_display)


def random_gif(display=True):
    path = Path("celebration_gifs.txt")
    with path.open("r") as f:
        gif_urls = f.readlines()
    random_url = random.choice(gif_urls)
    if display:
        st.image(random_url)
    return random_url
