import datetime

my_requests = [
    {
        "id": "a93687a2-3366-4a8a-a75e-aa20e3f0cbc1",
        "description": "There is water in my basement",
        "city": "Miami, FL",
        "source": "scraped",
        "channel": "WEB APP",
    },
    {
        "id": "fdc95e7a-60f0-4cff-9051-b9fc42b113a9",
        "description": "She needs someone to call back about the construction",
        "city": "Loveland, CO",
        "source": "Production",
        "channel": "PHONE",
    },
    {
        "id": "097fbb3d-4b00-4f43-9dde-c1e397dc28df",
        "description": "Calling to see if they need a booster for their modem. Looses service on the TV.",
        "city": "Oakland, CA",
        "source": "Fictional",
        "channel": "FORM",
    },
]

my_labelers = [
    {"email": "carly@daupler.com", "display_name": "Carly"},
    {"email": "heather.grebe@daupler.com", "display_name": "Heather"},
    {"email": "ryan@daupler.com", "display_name": "Ryan"},
]

my_ontologies = [
    {
        "name": "Label Pairs",
        "version": "1.1.0",
        "notes": "This is the ontology currently used in production.",
    },
    {
        "name": "20 Questions",
        "version": "0.1.0",
        "notes": "An experimental idea to clarify the labeling scheme through flowcharts.",
    },
]

my_ont_label_relationships = [
    {"ontology_id": 1, "question_version_id": 1},
    {"ontology_id": 1, "question_version_id": 2},
]

my_questions = [{"name": "d0", "notes": ""}, {"name": "d1"}]

my_versions = [
    {"major": 1, "minor": 1, "patch": 0},
    {"major": 1, "minor": 3, "patch": 0},
]

my_releases = [{"last_editor": "Nick"}]

my_questions = [
    {
        "question_id": 1,
        "version_major": 1,
        "version_minor": 1,
        "version_patch": 0,
        "notes": "",
    },
    {
        "question_id": 2,
        "version_major": 1,
        "version_minor": 3,
        "version_patch": 0,
        "notes": "",
    },
]


my_labels = [
    {"question_version_id": 1, "name": "Defer", "definition": "A catch-all category."},
    {"question_version_id": 1, "name": "Water", "definition": "Water department"},
    {"question_version_id": 1, "name": "Power", "definition": "Power department"},
    {"question_version_id": 1, "name": "Gas", "definition": "Gas department"},
    {"question_version_id": 1, "name": "Internet", "definition": "Internet department"},
    {
        "question_version_id": 2,
        "name": "Service Interruption",
        "definition": "Interruption in service not due to billing or a shutoff request.",
    },
    {
        "question_version_id": 2,
        "name": "Water Leaking",
        "definition": "Water is leaking from a water main line.",
    },
]

my_tasks = [
    {
        "request_id": "a93687a2-3366-4a8a-a75e-aa20e3f0cbc1",
        "question_version_id": 1,
        "status": "selected",
        "training_label": None,
        "last_edited": datetime.datetime(2022, 1, 19, 16, 58, 7, 9534),
        "last_editor": "Carly M.",
    },
    {
        "request_id": "a93687a2-3366-4a8a-a75e-aa20e3f0cbc1",
        "question_version_id": 2,
        "status": "selected",
        "training_label": None,
        "last_edited": datetime.datetime(2022, 1, 19, 16, 58, 7, 9534),
        "last_editor": "Carly M.",
    },
    {
        "request_id": "fdc95e7a-60f0-4cff-9051-b9fc42b113a9",
        "question_version_id": 1,
        "status": "flagged",
        "training_label": "Defer",
        "last_edited": datetime.datetime(2021, 7, 15, 11, 35, 0, 0),
        "last_editor": "Carly M.",
    },
    {
        "request_id": "fdc95e7a-60f0-4cff-9051-b9fc42b113a9",
        "question_version_id": 2,
        "status": "OK",
        "training_label": "Question",
        "last_edited": datetime.datetime(2021, 7, 15, 11, 35, 0, 0),
        "last_editor": "Carly M.",
    },
]

my_proposals = [
    {
        "request_id": "a93687a2-3366-4a8a-a75e-aa20e3f0cbc1",
        "question_version_id": 1,
        "label": "Water",
        "labeler_id": 3,
        "when_labeled": datetime.datetime(2022, 1, 19, 16, 58, 7, 9534),
    },
    {
        "request_id": "a93687a2-3366-4a8a-a75e-aa20e3f0cbc1",
        "question_version_id": 2,
        "label": "Water Leaking",
        "labeler_id": 3,
        "when_labeled": datetime.datetime(2022, 1, 19, 16, 58, 7, 9534),
    },
    {
        "request_id": "fdc95e7a-60f0-4cff-9051-b9fc42b113a9",
        "question_version_id": 1,
        "label": "Defer",
        "labeler_id": 2,
        "when_labeled": datetime.datetime(2021, 7, 13, 10, 27, 0, 0),
        "notes": "Should this be code enforcement?",
    },
    {
        "request_id": "fdc95e7a-60f0-4cff-9051-b9fc42b113a9",
        "question_version_id": 2,
        "label": "Question",
        "labeler_id": 2,
        "when_labeled": datetime.datetime(2021, 7, 13, 10, 27, 0, 0),
    },
]

my_records = {
    "request": my_requests,
    "version": my_versions,
    "labeler": my_labelers,
    "question_version": my_questions,
    "label": my_labels,
    "question": my_questions,
    "ontology": my_ontologies,
    "ont_type_relation": my_ont_label_relationships,
    "task": my_tasks,
    "proposed": my_proposals,
}
