from typing import Optional
from typing import Dict
import json

import boto3

session = boto3.Session(profile_name="daupler-annotation")
lambda_client = session.client("lambda")


def invoke(lambda_func: str, params: Dict, invocation_type: str = "Event") -> Dict:
    payload = json.dumps(params).encode("utf-8")
    response = lambda_client.invoke(
        FunctionName=lambda_func, InvocationType=invocation_type, Payload=payload
    )
    if invocation_type == "RequestResponse":
        payload = response["Payload"].read().decode("utf-8")
        return json.loads(payload)
    return response


class AWSRepository:
    def get_batch(
        self,
        batch_size: int = 20,
        session_tag: Optional[str] = None,
        labeler_id: str = "",
    ):
        batch = invoke(
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
        invoke(
            "ProposeLabel",
            params=dict(
                labeler_id=labeler_id, session_tag=session_tag, proposals=proposals
            ),
        )
