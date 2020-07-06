import datetime
from caia.circrequests.diff import denied_keys_to_resubmit, diff, DiffResult


def test_diff():
    entry1 = {"barcode": "123", "item": "abc"}
    entry2 = {"barcode": "234", "item": "bcd"}
    entry3 = {"barcode": "345", "item": "cde"}

    modified_entry1 = {"barcode": "123", "item": "ABC123"}

    empty_list = []
    list1 = [entry1, entry2]
    list2 = [entry2, entry3]
    modified_list1 = [modified_entry1, entry2]
    denied_keys = {}

    key_field = "barcode"

    current_time = datetime.datetime.now()
    denied_items_wait_interval = 2 * 24 * 60 * 60  # 2 days

    # list1 compared against empty list
    diff_result_empty_to_list1 = diff(key_field, empty_list, list1, denied_keys,
                                      current_time, denied_items_wait_interval)
    assert len(diff_result_empty_to_list1.new_entries) == 2
    assert len(diff_result_empty_to_list1.modified_entries) == 0
    assert len(diff_result_empty_to_list1.deleted_entries) == 0

    # list2 compared against list1
    diff_result_list1_to_list2 = diff(key_field, list1, list2, denied_keys,
                                      current_time, denied_items_wait_interval)
    assert len(diff_result_list1_to_list2.new_entries) == 1
    assert entry3 in diff_result_list1_to_list2.new_entries
    assert len(diff_result_list1_to_list2.modified_entries) == 0
    assert len(diff_result_list1_to_list2.deleted_entries) == 1
    assert entry1 in diff_result_list1_to_list2.deleted_entries

    # list1 compared against modified_list1
    diff_result_list1_to_modified_list1 = diff(key_field, list1, modified_list1, denied_keys,
                                               current_time, denied_items_wait_interval)
    assert len(diff_result_list1_to_modified_list1.new_entries) == 0
    assert len(diff_result_list1_to_modified_list1.modified_entries) == 1
    assert modified_entry1 in diff_result_list1_to_modified_list1.modified_entries
    assert len(diff_result_list1_to_modified_list1.deleted_entries) == 0


def test_denied_keys_to_resubmit():
    june22 = datetime.datetime.fromisoformat('2020-06-22T11:36:33.032362')
    denied_items_wait_interval = 3 * 24 * 60 * 60  # 3 days

    denied_keys = {}
    possible_keys = {}
    denied_keys_to_add = denied_keys_to_resubmit(possible_keys, denied_keys, june22, denied_items_wait_interval)
    assert len(denied_keys_to_add) == 0

    denied_keys = {
        'key_june15': '2020-06-15T11:36:33.032362',
        'key_june20': '2020-06-20T11:36:33.032362',
        'key_june22': '2020-06-22T11:36:33.032362',
    }
    possible_keys = set(denied_keys.keys())
    denied_keys_to_add = denied_keys_to_resubmit(possible_keys, denied_keys, june22, denied_items_wait_interval)
    assert len(denied_keys_to_add) == 1
    assert 'key_june15' in denied_keys_to_add

    june25_midnight = datetime.datetime.fromisoformat('2020-06-25T00:00:00.000000')
    denied_keys_to_add = denied_keys_to_resubmit(possible_keys, denied_keys,
                                                 june25_midnight, denied_items_wait_interval)
    assert len(denied_keys_to_add) == 2
    assert 'key_june15' in denied_keys_to_add
    assert 'key_june20' in denied_keys_to_add

    june25_noon = datetime.datetime.fromisoformat('2020-06-25T12:00:00.000000')
    denied_keys_to_add = denied_keys_to_resubmit(possible_keys, denied_keys, june25_noon, denied_items_wait_interval)
    assert len(denied_keys_to_add) == 3
    assert 'key_june15' in denied_keys_to_add
    assert 'key_june20' in denied_keys_to_add
    assert 'key_june22' in denied_keys_to_add


def test_diff_with_denied_keys():
    key_field = "barcode"

    entry1 = {"barcode": "entry1", "item": "abc"}
    entry2 = {"barcode": "entry2", "item": "bcd"}
    entry3 = {"barcode": "entry3", "item": "cde"}

    # Diff result not should include "denied" entry, as it is not in the
    # current list
    previous_list = [entry1, entry2]
    current_list = [entry2, entry3]

    june22 = datetime.datetime.fromisoformat('2020-06-22T11:36:33.032362')
    june23 = datetime.datetime.fromisoformat('2020-06-23T11:36:33.032362')
    june30 = datetime.datetime.fromisoformat('2020-06-30T11:36:33.032362')

    denied_keys = {
        entry1["barcode"]: june22.isoformat()
    }

    denied_items_wait_interval = 2 * 24 * 60 * 60  # 2 days
    diff_result = diff(key_field, previous_list, current_list, denied_keys,
                       june30, denied_items_wait_interval)
    assert len(diff_result.new_entries) == 1
    assert len(diff_result.modified_entries) == 0
    assert len(diff_result.deleted_entries) == 1
    assert len(diff_result.denied_keys_to_persist) == 0
    assert entry3 in diff_result.new_entries

    # Diff result should include "denied" entry in the "new" entries,
    # as it is in the current list, and the denied_items_wait_interval has
    # expired
    previous_list = [entry1, entry2]
    current_list = [entry2, entry3]
    denied_keys = {
        entry2["barcode"]: june22.isoformat()
    }

    diff_result = diff(key_field, previous_list, current_list, denied_keys,
                       june30, denied_items_wait_interval)
    assert len(diff_result.new_entries) == 2
    assert len(diff_result.modified_entries) == 0
    assert len(diff_result.deleted_entries) == 1
    assert len(diff_result.denied_keys_to_persist) == 0
    assert entry2 in diff_result.new_entries
    assert entry3 in diff_result.new_entries

    # Diff result have the "denied" entry in the modified list
    # as it is in the current list, and the denied_items_wait_interval has
    # expired
    modified_entry2 = {"barcode": entry2['barcode'], "item": "ABC123"}
    previous_list = [entry1, entry2]
    current_list = [modified_entry2, entry3]

    denied_keys = {
        modified_entry2["barcode"]: june22.isoformat()
    }
    diff_result = diff(key_field, previous_list, current_list, denied_keys,
                       june30, denied_items_wait_interval)
    assert len(diff_result.new_entries) == 1
    assert len(diff_result.modified_entries) == 1
    assert len(diff_result.deleted_entries) == 1
    assert len(diff_result.denied_keys_to_persist) == 0
    assert modified_entry2 in diff_result.modified_entries
    assert entry3 in diff_result.new_entries

    # Diff result will not have a "denied" entry as the
    # denied_items_wait_interval has not expired
    previous_list = [entry1, entry2]
    current_list = [entry1, entry3]

    denied_keys = {
        entry1["barcode"]: june22.isoformat()
    }

    diff_result = diff(key_field, previous_list, current_list, denied_keys,
                       june23, denied_items_wait_interval)
    assert len(diff_result.new_entries) == 1
    assert entry3 in diff_result.new_entries
    assert len(diff_result.modified_entries) == 0
    assert len(diff_result.deleted_entries) == 1
    assert entry2 in diff_result.deleted_entries
    assert len(diff_result.denied_keys_to_persist) == 1
    assert entry1["barcode"] in diff_result.denied_keys_to_persist


def test_diff_result():
    new_entries = [{"barcode": "345", "item": "cde"}]
    modified_entries = [{"barcode": "456", "item": "ABC123"}]
    deleted_entries = [{"barcode": "789", "item": "abc"}]
    denied_keys_to_persist = {
        '987': '2020-06-22T11:36:33.032362',
        '765': '2020-06-23T11:36:33.032362',
    }

    diff_result = DiffResult(new_entries, modified_entries, deleted_entries, denied_keys_to_persist)

    # as_dict method
    expected_dict = {"new_entries": new_entries, "modified_entries": modified_entries,
                     "deleted_entries": deleted_entries, "denied_keys_to_persist": denied_keys_to_persist}
    assert expected_dict == diff_result.as_dict()

    # from_dict method
    diff_result2 = DiffResult.from_dict(expected_dict)
    assert diff_result2.new_entries == expected_dict["new_entries"]
    assert diff_result2.modified_entries == expected_dict["modified_entries"]
    assert diff_result2.deleted_entries == expected_dict["deleted_entries"]
    assert diff_result2.denied_keys_to_persist == expected_dict["denied_keys_to_persist"]

    # str method
    str = diff_result.__str__()
    assert new_entries.__str__() in str
    assert modified_entries.__str__() in str
    assert deleted_entries.__str__() in str
    assert denied_keys_to_persist.__str__() in str
