import re
from typing import Optional, Dict
import json
import toml
import os

import boto3
import streamlit as st


def write_credentials_if_needed():
    if "credentials_file_written" in st.session_state:
        print("Credentials file has already been written.")
        return
    print("Writing credentials file...")
    access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
    secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    shared_creds_file = os.environ.get("AWS_SHARED_CREDENTIALS_FILE", "")
    write_creds(access_key_id, secret_access_key, shared_creds_file)
    st.session_state["credentials_file_written"] = True
    print("File written.")


def write_creds(access_key_id, secret_key, filename):
    default = dict(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_key,
        region="us-east-1",
    )
    role = dict(
        role_arn="arn:aws:iam::240316015535:role/developers",
        source_profile="default",
        region="us-east-1",
    )
    data = {"default": default, "daupler-production": role}
    s = toml.dumps(data)
    with open(filename, "w") as f:
        stripped_of_quotes = re.sub('"', "", s)
        f.write(stripped_of_quotes)


class AWSRepository:
    def __init__(self):
        write_credentials_if_needed()
        session = boto3.Session(profile_name="daupler-production")
        lambda_client = session.client("lambda")
        self.lambda_client = lambda_client

    # FIXME Add retries on timeout
    def invoke(
        self, lambda_func: str, params: Dict, invocation_type: str = "Event"
    ) -> Dict:
        payload = json.dumps(params).encode("utf-8")
        response = self.lambda_client.invoke(
            FunctionName="daupler_annotation_" + lambda_func,
            InvocationType=invocation_type,
            Payload=payload,
        )
        if invocation_type == "RequestResponse":
            payload = response["Payload"].read().decode("utf-8")
            return json.loads(payload)
        return response

    def get_batch(
        self,
        batch_size: int = 20,
        session_tag: Optional[str] = None,
        labeler_id: str = "",
    ):
        batch = self.invoke(
            "PullBatchForLabeling",
            params=dict(
                session_tag=session_tag, labeler_id=labeler_id, batch_size=batch_size
            ),
            invocation_type="RequestResponse",
        )
        return batch

    def propose_batch(self, labeler_id: str, proposals, session_tag: str = ""):
        for label in proposals:
            hashtags = [f"#{tag}" for tag in label["tags"]]
            tag_string = " ".join(hashtags)
            if len(tag_string) > 0:
                label["notes"] = label["notes"] + " " + tag_string
        self.invoke(
            "ProposeLabel",
            params=dict(
                labeler_id=labeler_id, session_tag=session_tag, labeled_data=proposals
            ),
        )
