from relation import Relation1, Relation2, Relation3, from_list, from_triples, from_pairs


and_: Relation3[bool, bool, bool] = from_triples([
    (True,  True,  True),
    (True,  False, False),
    (False, True,  False),
    (False, False, False)
])

or_: Relation3[bool, bool, bool] = from_triples([
    (True,  True,  True),
    (True,  False, True),
    (False, True,  True),
    (False, False, False)
])

xor: Relation3[bool, bool, bool] = from_triples([
    (True,  True,  False),
    (True,  False, True),
    (False, True,  True),
    (False, False, False)
])

not_: Relation2[bool, bool] = from_pairs([
    (True, False),
    (False, True)
])

is_bool: Relation1[bool] = from_list("is_bool", [
    True,
    False
])