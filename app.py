from typing import Callable, Optional, Iterable, Dict
import uuid
import pyperclip
import re

import pandas as pd
import streamlit as st
from aws_repo import AWSRepository

import utils
import auth
from info import *

SESSION_TAG = "test-session"


def increment_index(value):
    st.session_state["batch_index"] += value


# Refactor: Should pass labeler ID.
def get_new_batch(repo, batch_size, session_tag: Optional[str] = None):
    batch = repo.get_batch(
        batch_size=batch_size,
        session_tag=session_tag,
        labeler_id=st.session_state["validated_user"],
    )
    st.session_state["batch"] = batch
    st.session_state["batch_index"] = 0
    st.session_state["batch_annotations"] = dict()
    st.session_state["batch_id"] = uuid.uuid4()


def batch_pulling_screen(batch_size, session_tag: str = "", repo=None):
    if "batch_submitted" in st.session_state:
        st.header("Batch submitted! You rule.")
        utils.random_gif()
        st.write("Ready for more?")
    st.button(
        "Pull a Batch to Label",
        on_click=get_new_batch,
        args=[repo, batch_size, session_tag],
    )
    st.stop()


def show_request(id, description):
    st.write(f"Request ID: {id}")
    col1, col2 = st.columns((10, 1))
    text_to_display = re.sub("\n", "", description)
    with col1:
        st.subheader(f'Description: "{text_to_display}"')
    with col2:
        copy_it = st.button("📋", help="Copy to Clipboard")
        if copy_it:
            pyperclip.copy(description)


def get_d0_d1_inputs(
    vocabulary, key_suffix: str = "", defaults: Optional[Dict] = dict()
):
    placeholder = "-"
    d0_options = [placeholder] + sorted(set(vocabulary["D0"]))
    d0_default = defaults.get("D0", placeholder)
    d0 = st.selectbox(
        "D0: Agency",
        [placeholder] + sorted(set(vocabulary["D0"])),
        key="input_D0" + key_suffix,
        index=d0_options.index(d0_default),
    )
    if d0 is not placeholder:
        filtered_df = vocabulary[vocabulary.D0 == d0]
    else:
        filtered_df = vocabulary
    d1_options = [placeholder] + sorted(set(filtered_df["D1"]))
    d1_default = defaults.get("D1", placeholder)
    d1 = st.selectbox(
        "D1: Incident Type",
        d1_options,
        key="input_D1" + key_suffix,
        index=d1_options.index(d1_default),
    )
    return dict(D0=d0, D1=d1)


def annotation_inputs(
    vocabulary,
    get_question_labels: Callable,
    tags: Iterable[str] = [
        "Confusing",
        "Weird",
        "Funny",
        "Multiple Issues",
        "More Info Needed",
        "Needs Review",
    ],
    suffix: str = "",
):
    request_id = suffix[1:]
    existing_labels = st.session_state["batch_annotations"]
    if str(request_id) in existing_labels:
        defaults = existing_labels[str(request_id)]
    else:
        defaults = dict(labels=dict())
    col1, col2 = st.columns(2)
    with col1:
        labels = get_question_labels(
            vocabulary, key_suffix=suffix, defaults=defaults["labels"]
        )
    with col2:
        tags = st.multiselect(
            "Tags", tags, key="input_tags" + suffix, default=defaults.get("tags", [])
        )
        notes = st.text_area(
            "Notes", key="input_notes" + suffix, value=defaults.get("notes", "")
        )
    return dict(labels=labels, tags=tags, notes=notes)


def annotate_batch(batch, vocabulary):
    idx = st.session_state["batch_index"]
    batch_annotations = st.session_state["batch_annotations"]
    with st.container():
        st.progress((idx + 1.0) / len(batch))
        request_id, description = batch[int(idx)]
        show_request(request_id, description)
        annotations = annotation_inputs(
            vocabulary, get_d0_d1_inputs, suffix=f"_{request_id}"
        )
        batch_annotations[str(request_id)] = annotations
        col1, col2, _ = st.columns((1, 1, 4))
        if idx > 0:
            with col1:
                st.button("Previous", on_click=increment_index, args=[-1])
        if idx < len(batch) - 1:
            with col2:
                st.button("Next", on_click=increment_index, args=[1])


def submit_and_clear(repo, proposals):
    st.balloons()
    labeler_id = st.session_state["validated_user"]
    repo.propose_batch(
        labeler_id=labeler_id, proposals=proposals, session_tag=SESSION_TAG
    )
    st.session_state["batch_submitted"] = True
    st.session_state["batch"] = None


def review_and_submit(repo):
    with st.container():
        annotations = st.session_state["batch_annotations"]
        proposals = [dict(request_id=id, **data) for id, data in annotations.items()]
        records = [
            dict(ID=id, **data["labels"], Notes=data["notes"], Tags=data["tags"])
            for id, data in annotations.items()
        ]
        df = pd.DataFrame.from_records(records)
        st.table(df)
        submit = st.button("Submit", on_click=submit_and_clear, args=[repo, proposals])
        if submit:
            utils.random_gif()
            batch_pulling_screen(10, session_tag=None, repo=repo)


def labeling_app(user, vocab, repo, batch_size=10, session_tag="test"):
    with st.sidebar:
        profile_info(user)
        session_info(repo)
    batch = st.session_state["batch"]
    if batch is None:
        batch = batch_pulling_screen(batch_size, session_tag=session_tag, repo=repo)
    if len(batch) == 0:
        st.write("Nothing left to label!")
        st.stop()
    annotate_batch(batch, vocab)
    with st.expander("Review and Submit"):
        review_and_submit(repo)
    with st.expander("Label Dictionary"):
        vocab_dictionary(vocab)


# Consider refactoring this to be object-oriented
def main():
    utils.initialize_state(validated_user=None, batch=None)
    validated_user = st.session_state["validated_user"]
    if not validated_user:
        auth.authentication(lambda u, p: auth.is_daupler_email(u))
    vocab = pd.read_csv("vocabulary_D0D1.csv")
    repo = AWSRepository()
    labeling_app(validated_user, vocab, repo, batch_size=10, session_tag=SESSION_TAG)


if __name__ == "__main__":
    main()
