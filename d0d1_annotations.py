from typing import Callable, Iterable, Optional, Dict
import pyperclip
import re

import pandas as pd
import streamlit as st

TAGS = [
    "Confusing",
    "Unusual",
    "Multiple Issues",
    "More Info Needed",
    "Needs Review",
    "New Label Needed",
]


def show_request(id, description):
    st.write(f"Request ID: {id}")
    col1, col2 = st.columns((10, 1))
    text_to_display = re.sub("\n", "", description)
    with col1:
        st.subheader(f'Description: "{text_to_display}"')
    with col2:
        # copy_it = st.button("📋", help="Copy to Clipboard")
        # if copy_it:
        # pyperclip.copy(description)
        pass


class D0D1Annotations:
    def __init__(self, vocabulary, tags: Iterable = TAGS):
        self.vocabulary = vocabulary
        self.tags = tags

    def get_d0_d1_inputs(
        self, vocabulary, key_suffix: str = "", defaults: Optional[Dict] = dict()
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
        self,
        item_id: str = "",
        description: str = "Description",
        defaults=None,
        proposals=None,
    ):
        show_request(item_id, description)
        if proposals is not None:
            item_proposals = proposals.get(str(item_id), [])
            df = pd.DataFrame.from_records(data=item_proposals, index="labeler_id")
            st.table(df)
        suffix = f"_{item_id}"
        col1, col2 = st.columns(2)
        with col1:
            labels = self.get_d0_d1_inputs(
                self.vocabulary, key_suffix=suffix, defaults=defaults["labels"]
            )
        with col2:
            tags_selected = st.multiselect(
                "Tags",
                self.tags,
                key="input_tags" + suffix,
                default=defaults.get("tags", []),
            )
            notes = st.text_area(
                "Notes", key="input_notes" + suffix, value=defaults.get("notes", "")
            )
        item_annotations = dict(labels=labels, tags=tags_selected, notes=notes)
        return item_annotations
