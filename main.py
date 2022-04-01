import pandas as pd
import streamlit as st

from app import LabelingApp
from aws_repo import AWSRepository
import auth

# from components import vocab_dictionary
import components
from d0d1_annotations import D0D1Annotations


def initialize_state(**kwargs):
    for key, value in kwargs.items():
        if key not in st.session_state:
            st.session_state[key] = value


def unset_app():
    st.session_state["app"] = None


def main():

    initialize_state(validated_user=None, batch=None, app=None)
    validated_user = st.session_state["validated_user"]
    if not validated_user:
        auth.authentication(lambda u, p: auth.is_daupler_email(u))
        st.stop()
    # session_tag = st.session_state.get("session_tag", "test")
    session_tags = [f"group{n}" for n in [5, 9, 15, 16, 19]]
    with st.sidebar:
        components.session_info(None)
        components.profile_info(validated_user)
        session_tag = st.selectbox(
            "Session Tag", options=session_tags, on_change=unset_app
        )
    vocab = pd.read_csv("vocabulary_D0D1.csv")
    d0d1_inputs = D0D1Annotations(vocab)
    # Rather than passing the vocabulary, pass the annotation screen.
    app = st.session_state["app"]
    if st.session_state["app"] is None:
        repo = AWSRepository()
        app = LabelingApp(
            repo,
            validated_user,
            session_tag=session_tag,
            batch_size=10,
            annotation_inputs=d0d1_inputs.annotation_inputs,
        )
        st.session_state["app"] = app
    app.run()
    with st.expander("Label Dictionary"):
        vocab_dictionary(vocab)


if __name__ == "__main__":
    main()
