from bq_iterate import __version__, batchify_iterator


def test_version():
    assert __version__ == "0.1.5"

def test_batchify_iterator():
    batches = batchify_iterator([i for i in range(10)], batch_slice=2)
    test_list = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
    assert all([el == test_list[idx] for idx,el in enumerate(batches)])
