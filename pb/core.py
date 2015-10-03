import pkgutil

from characteristic import Attribute, attributes
from parsley import makeGrammar as make_grammar

from pb import types


@attributes(
    [
        Attribute(name="bindings", default_factory=dict),
    ],
)
class Protobuf(object):
    @classmethod
    def from_bytes(cls, bytes):
        return _GRAMMAR(bytes).proto()


@attributes(
    [
        Attribute(name="name"),
        Attribute(name="fields", default_factory=list),
    ],
)
class Message(object):
    pass


@attributes(
    [
        Attribute(name="name"),
        Attribute(name="type"),
    ],
)
class Field(object):
    pass


_GRAMMAR = make_grammar(
    source=pkgutil.get_data(__package__, "protobuf.parsley"),
    bindings={
        "Protobuf" : Protobuf,
        "Message" : Message,
        "Field" : Field,
        "types" : types,
    },
)
