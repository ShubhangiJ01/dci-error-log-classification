from api.main import get_values
from api.main import enhance_job


def test_job_get_values():

    enhanced_job = {
        "id": "1045bf09-f0c1-408f-812d-d90f5c7386f7",
        "content": "non-zero return code\nStderr:\nDEBUG:root:Status for task /distribution/check-install: Waiting\nDEBUG:root:Waiting for 5s ...\nDEBUG:root:Status for task /distribution/check-install: Waiting",
        "stage_of_failure": "Wait system to be installed",
        "is_user_text": 0,
        "is_sut": 0,
        "is_install": 0,
        "is_logs": 0,
        "is_dci-rhel-cki": 0,
        "error_type": "DCI",

    }
    values = get_values(enhanced_job)

    assert values == [
        "https://www.distributed-ci.io/jobs/1045bf09-f0c1-408f-812d-d90f5c7386f7",
        "1045bf09-f0c1-408f-812d-d90f5c7386f7",
        """non-zero return code
Stderr:
DEBUG:root:Status for task /distribution/check-install: Waiting
DEBUG:root:Waiting for 5s ...
DEBUG:root:Status for task /distribution/check-install: Waiting""",
        "Wait system to be installed", '0', '0', '0', '0', '0', 'DCI',
    ]