from api.jobstates import get_first_jobstate_failure, get_jobstate_before_failure


def test_get_first_jobstate_failure():
    jobstates = [
        {
            "created_at": "2020-06-30T18:22:43.024015",
            "status": "new",
        },
        {
            "created_at": "2020-06-30T18:22:45.436619",
            "status": "new",
        },
        {
            "created_at": "2020-06-30T18:23:51.520139",
            "status": "running",
        },
        {
            "created_at": "2020-06-30T18:24:28.818160",
            "status": "running",
        },
        {
            "created_at": "2020-06-30T18:54:10.115726",
            "status": "failure",
        },
        {
            "created_at": "2020-06-30T18:54:13.221898",
            "status": "failure",
        },
        {
            "created_at": "2020-06-30T18:23:28.500169",
            "status": "pre-run",
        },
    ]
    jobstate = get_first_jobstate_failure(jobstates)

    assert jobstate == {
        "created_at": "2020-06-30T18:54:10.115726",
        "status": "failure",
    }


def test_returns_jobstate_error():
    jobstates = [
        {
            "created_at": "2020-06-26T08:01:48.031811",
            "status": "running",
        },
        {
            "created_at": "2020-06-26T08:02:48.031811",
            "status": "error",
        }
    ]

    jobstate = get_first_jobstate_failure(jobstates)

    assert jobstate == {
        "created_at": "2020-06-26T08:02:48.031811",
        "status": "error",
    }


def test_returns_first_jobstate_in_error_or_failure():
    jobstates = [
        {
            "created_at": "2020-06-26T08:02:48.031811",
            "status": "error",
        },
        {
            "created_at": "2020-06-25T18:54:10.115726",
            "status": "failure",
        },
    ]

    jobstate = get_first_jobstate_failure(jobstates)

    assert jobstate == {
        "created_at": "2020-06-25T18:54:10.115726",
        "status": "failure",
    }


def test_get_jobstate_before_failure():
    jobstates = [
    {
        "created_at": "2020-08-07T11:09:33.979999",
        "files": [
            {
                "created_at": "2020-08-07T11:09:34.527725",
            }
        ],
        "status": "failure"
    },
    {
        "created_at": "2020-08-07T11:09:32.343146",
        "files": [
            {
                "created_at": "2020-08-07T11:09:33.679588",
            },
            {
                "created_at": "2020-08-07T11:09:33.126146",
            }
        ],
        "status": "error"
    },
    {
        "created_at": "2020-08-07T11:08:00.793797",
        "files": [
            {
                "created_at": "2020-08-07T11:08:01.938964",
            },
            {
                "created_at": "2020-08-07T11:08:01.343322",
            }
        ],
        "status": "pre-run"
    },
    {
        "created_at": "2020-08-07T11:07:24.110430",
        "files": [
            {
                "created_at": "2020-08-07T11:08:00.663023",
            },
            {
                "created_at": "2020-08-07T11:07:43.788959",
            },
            {
                "created_at": "2020-08-07T11:07:41.512700",
            }
        ],
        "status": "new"
    },
    {
        "created_at": "2020-08-07T11:07:20.606713",
        "files": [
            {
                "created_at": "2020-08-07T11:07:21.716214",
            },
            {
                "created_at": "2020-08-07T11:07:23.972373",
            },
            {
                "created_at": "2020-08-07T11:07:21.045457",
            },
            {
                "created_at": "2020-08-07T11:07:22.402847",
            }
        ],
        "status": "new"
    }
    ]
    jobstate = get_jobstate_before_failure(jobstates)

    assert jobstate ==  {
        "created_at": "2020-08-07T11:08:00.793797",
        "files": [
            {
                "created_at": "2020-08-07T11:08:01.938964",
            },
            {
                "created_at": "2020-08-07T11:08:01.343322",
            }
        ],
        "status": "pre-run"
    }


