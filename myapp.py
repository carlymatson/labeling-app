class LabelingApp:
    def __init__(self, repo, session_tag="", batch_size=""):
        self.repo = repo
        self.session_tag = session_tag
        self.batch_size = batch_size

    def get_new_batch(self):
        pass

    def propose_batch(self):
        pass

    def show_request(self):
        pass

    def annotation_inputs(self):
        pass

    def annotate_batch(self):
        pass
