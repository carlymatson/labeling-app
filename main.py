import pandas as pd
import streamlit as st

from app import LabelingApp
from aws_repo import AWSRepository
import utils
import auth
from info import vocab_dictionary
from d0d1_annotations import D0D1Annotations


def main():
    utils.initialize_state(validated_user=None, batch=None)
    validated_user = st.session_state["validated_user"]
    if not validated_user:
        auth.authentication(lambda u, p: auth.is_daupler_email(u))
    repo = AWSRepository()
    session_tag = st.session_state.get("session_tag", "test")
    vocab = pd.read_csv("vocabulary_D0D1.csv")
    d0d1_inputs = D0D1Annotations(vocab)
    # Rather than passing the vocabulary, pass the annotation screen.
    if "app" not in st.session_state:
        app = LabelingApp(
            repo,
            validated_user,
            vocab,
            session_tag,
            batch_size=10,
            annotation_inputs=d0d1_inputs.annotation_inputs,
        )
        st.session_state["app"] = app
    else:
        app = st.session_state["app"]
    app.run()
    with st.expander("Label Dictionary"):  # Or should this be after the app?
        vocab_dictionary(vocab)


if __name__ == "__main__":
    main()
