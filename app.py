from typing import Dict
from enum import Enum

import pandas as pd
import streamlit as st

import components
from batch import Batch


class AppMode(Enum):
    propose = "PROPOSE"
    assign = "ASSIGN"
    review = "REVIEW"


class LabelingApp:
    def __init__(
        self,
        repo,
        labeler_id,
        session_tag: str = "",
        batch_size: int = 10,
        annotation_inputs: Dict = None,
        labeler_is_reviewer: bool = False,
    ):
        self.repo = repo
        self.session_tag = session_tag
        self.batch_size = batch_size
        self.labeler_id = labeler_id
        self.labeler_is_reviewer = labeler_is_reviewer
        self.mode = AppMode.propose
        # Info on current batch
        self.batch = None
        self.batch_submitted = False
        self.annotation_inputs = annotation_inputs

    def get_new_batch(self):
        for_review = self.mode == AppMode.review
        batch = self.repo.get_batch(
            batch_size=self.batch_size,
            session_tag=self.session_tag,
            labeler_id=self.labeler_id,
            for_review=for_review,
        )
        self.batch = batch

    def batch_pulling_screen(self):
        if self.batch_submitted:
            st.header("Batch submitted! You rule.")
            components.random_gif()
            st.write("Ready for more?")
        action_word = "Review" if self.mode == AppMode.review else "Label"
        st.button(
            f"Pull a Batch to {action_word}",
            on_click=self.get_new_batch,
        )
        st.stop()

    def annotate_batch(self):
        if len(self.batch) == 0:
            st.write("There is nothing to label.")
            st.stop()
        self.batch.show_progress()
        # Display inputs for current request
        request_id, description = self.batch.get_current()
        old_item_annotations = self.batch.annotations.get(
            str(request_id), dict(labels=dict())
        )
        others_annotations = self.batch.proposals.get(str(request_id), [])
        item_annotations = self.annotation_inputs(
            item_id=request_id,
            description=description,
            defaults=old_item_annotations,
            proposals=others_annotations,
        )
        self.batch.annotations[str(request_id)] = item_annotations
        self.batch.navigation()

    def review_and_submit(self):
        # FIXME Not all cols make sense with training data.
        records = [
            dict(ID=id, **data["labels"], Notes=data["notes"], Tags=data["tags"])
            for id, data in self.batch.annotations.items()
        ]
        df = pd.DataFrame.from_records(records)
        st.table(df)
        submit = st.button("Submit", on_click=self.submit_and_clear)
        if submit:
            self.batch_pulling_screen()

    def submit_and_clear(self):
        st.balloons()
        proposals = [
            dict(request_id=id, **data) for id, data in self.batch.annotations.items()
        ]
        self.repo.propose_batch(
            labeler_id=self.labeler_id,
            proposals=proposals,
            session_tag=self.session_tag,
        )
        self.batch_submitted = True
        self.batch = None

    def run(self):
        # with st.sidebar:
        # components.profile_info(self.labeler_id)
        # components.session_info(self.repo)
        if self.labeler_is_reviewer:
            with st.sidebar:
                modes = [m for m in AppMode]
                mode = st.radio(
                    "Labeling Mode",
                    options=modes,
                    format_func=lambda m: m.name.title(),
                )
                self.mode = mode
        if self.batch is None:
            self.batch_pulling_screen()  # Stops after this screen plays.
        self.annotate_batch()
        with st.expander("Review and Submit"):
            self.review_and_submit()
