from caia.circrequests.diff import diff, DiffResult


def test_diff():
    entry1 = {"barcode": "123", "item": "abc"}
    entry2 = {"barcode": "234", "item": "bcd"}
    entry3 = {"barcode": "345", "item": "cde"}

    modified_entry1 = {"barcode": "123", "item": "ABC123"}

    empty_list = []
    list1 = [entry1, entry2]
    list2 = [entry2, entry3]
    modified_list1 = [modified_entry1, entry2]

    key_field = "barcode"

    diff_result_empty_to_list1 = diff(key_field, empty_list, list1)
    assert len(diff_result_empty_to_list1.new_entries) == 2
    assert len(diff_result_empty_to_list1.modified_entries) == 0
    assert len(diff_result_empty_to_list1.deleted_entries) == 0

    diff_result_list1_to_list2 = diff(key_field, list1, list2)
    assert len(diff_result_list1_to_list2.new_entries) == 1
    assert entry3 in diff_result_list1_to_list2.new_entries
    assert len(diff_result_list1_to_list2.modified_entries) == 0
    assert len(diff_result_list1_to_list2.deleted_entries) == 1
    assert entry1 in diff_result_list1_to_list2.deleted_entries

    diff_result_list1_to_modified_list1 = diff(key_field, list1, modified_list1)
    assert len(diff_result_list1_to_modified_list1.new_entries) == 0
    assert len(diff_result_list1_to_modified_list1.modified_entries) == 1
    assert modified_entry1 in diff_result_list1_to_modified_list1.modified_entries
    assert len(diff_result_list1_to_modified_list1.deleted_entries) == 0


def test_diff_result():
    new_entries = [{"barcode": "345", "item": "cde"}]
    modified_entries = [{"barcode": "123", "item": "ABC123"}]
    deleted_entries = [{"barcode": "123", "item": "abc"}]

    diff_result = DiffResult(new_entries, modified_entries, deleted_entries)

    expected_dict = {"new_entries": new_entries, "modified_entries": modified_entries,
                     "deleted_entries": deleted_entries}
    assert expected_dict == diff_result.as_dict()

    diff_result2 = DiffResult.from_dict(expected_dict)
    assert diff_result2.new_entries == expected_dict["new_entries"]
    assert diff_result2.modified_entries == expected_dict["modified_entries"]
    assert diff_result2.deleted_entries == expected_dict["deleted_entries"]
