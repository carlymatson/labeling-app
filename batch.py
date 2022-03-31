import uuid

import streamlit as st


class Batch:  # Can add error-handling in this class
    def __init__(self, items):
        self.items = items
        self.current_index = 0
        self.id = uuid.uuid4()

    def __len__(self):
        return len(self.items)

    def increment_index(self, value):
        self.current_index += value

    def navigation(self):
        col1, col2, _ = st.columns((1, 1, 4))
        if self.current_index > 0:
            with col1:
                st.button("Previous", on_click=self.increment_index, args=[-1])
        if self.current_index < len(self.items) - 1:
            with col2:
                st.button("Next", on_click=self.increment_index, args=[1])

    def get_current(self):
        return self.items[self.current_index]

    def show_progress(self):
        st.progress((self.current_index + 1.0) / len(self.items))
