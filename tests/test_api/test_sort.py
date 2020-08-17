from api.sort import sort_by_created_at

def test_sort_by_created_at():
    items = [
        {"created_at": "2020-04-03T17:18:21.370311", "id": "f1"},
        {"created_at": "2020-04-03T17:18:25.660819", "id": "f4"},
        {"created_at": "2020-04-03T17:18:21.893311", "id": "f2"},
        {"created_at": "2020-04-03T17:18:24.972299", "id": "f3"},
    ]

    sorted_items = sort_by_created_at(items)

    assert sorted_items == [
        {"created_at": "2020-04-03T17:18:21.370311", "id": "f1"},
        {"created_at": "2020-04-03T17:18:21.893311", "id": "f2"},
        {"created_at": "2020-04-03T17:18:24.972299", "id": "f3"},
        {"created_at": "2020-04-03T17:18:25.660819", "id": "f4"},
    ]