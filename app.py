import pandas as pd
import streamlit as st

# from components import *
import components

from batch import Batch


class LabelingApp:
    def __init__(
        self,
        repo,
        labeler_id,
        session_tag="",
        batch_size=10,
        annotation_inputs=None,
    ):
        self.repo = repo
        self.session_tag = session_tag
        self.batch_size = batch_size
        self.labeler_id = labeler_id
        # Info on current batch
        self.batch = None
        self.annotations = dict()
        self.batch_submitted = False
        self.annotation_inputs = annotation_inputs

    def get_new_batch(self):
        batch_items = self.repo.get_batch(
            batch_size=self.batch_size,
            session_tag=self.session_tag,
            labeler_id=self.labeler_id,
        )
        self.batch = Batch(batch_items)
        self.annotations = dict()

    def batch_pulling_screen(self):
        if self.batch_submitted:
            st.header("Batch submitted! You rule.")
            components.random_gif()
            st.write("Ready for more?")
        st.button(
            "Pull a Batch to Label",
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
        item_annotations = self.annotation_inputs(
            item_id=request_id, annotations=self.annotations, description=description
        )
        self.annotations[str(request_id)] = item_annotations
        self.batch.navigation()

    def review_and_submit(self):
        records = [
            dict(ID=id, **data["labels"], Notes=data["notes"], Tags=data["tags"])
            for id, data in self.annotations.items()
        ]
        df = pd.DataFrame.from_records(records)
        st.table(df)
        submit = st.button("Submit", on_click=self.submit_and_clear)
        if submit:
            self.batch_pulling_screen()

    def submit_and_clear(self):
        st.balloons()
        proposals = [
            dict(request_id=id, **data) for id, data in self.annotations.items()
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
        if self.batch is None:
            self.batch_pulling_screen()  # Stops after this screen plays.
        self.annotate_batch()
        with st.expander("Review and Submit"):
            self.review_and_submit()
