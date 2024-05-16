from lens import focus


def test_focus():
    collection = {'a': ['aye', 'ah'], 'b': ('be', 'bee'), 'c': {'words': ['sea', 'see']}}
    assert focus(collection, ['a', 0]) == 'aye'
    assert focus(collection, ['b', 1]) == 'bee'
    assert focus(collection, ['c', 'words', 0]) == 'sea'
