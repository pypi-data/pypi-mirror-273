from pytest import fixture, mark, raises


from lens import lens


@fixture
def complex_data_struct(list_based_struct):
    return {'a': 'aye', 'b_list': ['be', 'bee'],
            'c_list': [{'starts_with_c': ['cee', 'ce'], 'starts_with_s': ['see', 'sea']}],
            'nested_lists': [{'letters': ['a', 'b', 'c']}, {'letters': ['d', 'e', 'f']}, {'letters': ['g', 'h', 'i']},
                             {'letters': ['j', 'k', 'l']}, {'letters': ['m', 'n', 'o']}],
            'deeper_nest': list_based_struct}


@fixture
def list_based_struct():
    return [{'one': [{'two': [{'three': '123'}]}]}, {'one': [{'two': [{'three': '456'}]}]},
            {'one': [{'two': [{'three': '789'}]}]}, {'one': [{'two': [{'three': '101'}]}]},
            {'one': [{'two': [{'three': '112'}]}]}, {'one': [{'two': [{'three': '1314'}]}]}]


@fixture
def structure_with_objects():
    class Thing(object):
        pass
    a = Thing()
    b = Thing()
    c = Thing()
    d = Thing()
    a.yolo = [{'word': 'one'}, {'word': 'two'}]
    b.yolo = [{'word': 'three'}, {'word': 'four'}]
    c.yolo = [{'word': 'five'}, {'word': 'six'}]
    d.yolo = [{'word': 'seven'}, {'word': 'eight'}]
    return [{'object': a}, {'object': b}, {'object': c}, {'object': d}]


@fixture
def list_structure_with_int_keys():
    return [{0: ['zero', 'cero'], 1: ['one', 'uno']}]


def test_lens_simple(complex_data_struct):
    assert lens.lens(complex_data_struct, ['a']) == 'aye'


def test_lens_failure(complex_data_struct):
    with raises(lens.FocusingError):
        lens.lens(complex_data_struct, ['not', 'going', 'to', 'work'])


def test_lens_nested(complex_data_struct):
    result = lens.lens(complex_data_struct, ['nested_lists', 'letters'])
    expected = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
    assert result == expected


def test_lens_indexing(complex_data_struct):
    result = lens.lens(complex_data_struct, ['nested_lists', 0, 'letters'])
    expected = ['a', 'b', 'c']
    assert result == expected


def test_lens_forced_mapping(list_structure_with_int_keys):
    result = lens.lens(list_structure_with_int_keys, [(0, {'force_map': True}), 0])
    expected = 'zero'
    assert result == expected


def test_lens_deeper_nested(complex_data_struct):
    result = lens.lens(complex_data_struct, ['deeper_nest', 'one', 'two', 'three'])
    expected = ['123', '456', '789', '101', '112', '1314']
    assert result == expected


def test_list_based_lens(list_based_struct):
    result = lens.lens(list_based_struct, ['one', 'two', 'three'])
    expected = ['123', '456', '789', '101', '112', '1314']
    assert result == expected


def test_list_based_lens_with_dbl_flatten(list_based_struct):
    result = lens.lens(list_based_struct, [('one', {'flatten': True}), ('two', {'flatten': True}), 'three'])
    expected = ['123', '456', '789', '101', '112', '1314']
    assert result == expected


def test_list_based_lens_without_flattening(list_based_struct):
    result = lens.lens(list_based_struct, ['one', 'two', 'three'], False)
    expected = [[['123']], [['456']], [['789']], [['101']], [['112']], [['1314']]]
    assert result == expected


def test_list_based_lens_with_flatten_on_one(list_based_struct):
    result = lens.lens(list_based_struct, [('one', {'flatten': True}), 'two', 'three'], False)
    expected = [['123'], ['456'], ['789'], ['101'], ['112'], ['1314']]
    assert result == expected


def test_list_based_lens_with_flatten_on_two(list_based_struct):
    result = lens.lens(list_based_struct, ['one', ('two', {'flatten': True}), 'three'], False)
    expected = [['123'], ['456'], ['789'], ['101'], ['112'], ['1314']]
    assert result == expected


def test_list_based_lens_with_flatten_on_three(list_based_struct):
    result = lens.lens(list_based_struct, ['one', 'two', ('three', {'flatten': True})], False)
    expected = [['123'], ['456'], ['789'], ['101'], ['112'], ['1314']]
    assert result == expected


def test_list_based_lens_with_trpl_flatten(list_based_struct):
    result = lens.lens(list_based_struct, ['one', 'two', 'three'])
    expected = ['123', '456', '789', '101', '112', '1314']
    assert result == expected


def test_lens_with_objects(structure_with_objects):
    result = lens.lens(structure_with_objects, ['object', 'yolo', 'word'])
    expected = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
    assert result == expected


def test_lens_with_too_deep_key_chain(structure_with_objects):
    with raises(lens.FocusingError):
        lens.lens(structure_with_objects, ['object', 'yolo', 'word', 'more', 'i', 'want', 'more'])


def test_lens_empty_list():
    with raises(lens.FocusingError):
        lens.lens([], [0, 'something'])


def test_lens_empty_dict():
    with raises(lens.FocusingError):
        lens.lens({}, ['a', 'something'])


def test_lens_empty_tuple():
    with raises(lens.FocusingError):
        lens.lens(tuple(), [0, 'thing'])


@mark.parametrize('value,result', [(3, (3, {})), ('a', ('a', {})), (('yolo', {}), ('yolo', {})), (('a',), ('a', {})),
                                   ('id', ('id', {}))])
def test_unpack_element(result, value):
    assert lens.unpack_element(value) == result


def test_unpack_element_dict():
    with raises(ValueError):
        lens.unpack_element({'a': 'aye'})


def test_unpack_element_oversized_tuple():
    with raises(ValueError):
        lens.unpack_element(('yolo', 3, 2))


def test_unpack_empty_tuple():
    with raises(ValueError):
        lens.unpack_element(tuple())
