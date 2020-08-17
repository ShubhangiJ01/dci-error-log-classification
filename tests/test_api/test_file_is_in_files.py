from api.file_is_in_files import check_if_file_is_in_files

def test_check_if_file_is_in_files_returns_true():
    files = [
        {
            "name": "Upload hooks directory contents",
        },
        {
            "name": "Upload settings yml file",
        },
        {
            "name": "Gathering Facts",
        }
    ]
    result = check_if_file_is_in_files(files, "Upload settings yml file")

    assert result == True


def test_check_if_file_is_in_files_returns_false():
    files = [
        {
            "name": "Upload hooks directory contents",
        },
        {
            "name": "Upload settings yml file",
        },
        {
            "name": "Gathering Facts",
        }
    ]
    result = check_if_file_is_in_files(files, "Upload settings yml file file")

    assert result == False

