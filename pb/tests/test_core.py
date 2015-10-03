from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import text

from pb import core, types


class TestSerialization(TestCase):

    Person = core.Message(
        name="Person",
        fields=[core.Field(name="name", type=types.STRING)],
    )

    @given(text())
    def test_serialization_round_trips(self, name):
        person = self.Person(name=name)
        self.assertEqual(self.Person.deserialize(person.serialize()), person)


class TestParser(TestCase):
    def test_empty(self):
        protobuf = core.Protobuf.from_bytes(
            """
            syntax = "proto3";
            """,
        )

        self.assertEqual(protobuf, core.Protobuf())

    def test_simple_message(self):
        protobuf = core.Protobuf.from_bytes(
            """
            syntax = "proto3";
            message Person {
                string name = 1;
            }
            """,
        )

        self.assertEqual(
            protobuf, core.Protobuf(
                bindings={
                    "Person" : core.Message(
                        name="Person",
                        fields=[core.Field(name="name", type=types.STRING)],
                    ),
                },
            ),
        )

    # def test_nested_message(self):
    #     protobuf = core.Protobuf.from_bytes(
    #         """
    #         syntax = "proto3";
    #         message Outer {
    #             option (my_option).a = true;
    #             message Inner {   // Level 2
    #                 int64 ival = 1;
    #             }
    #             map<int32, string> my_map = 2;
    #         }
    #         """,
    #     )
    #
    #     self.assertEqual(
    #         protobuf, core.Protobuf(
    #             bindings={
    #                 "Outer" : core.Message(
    #                     name="Outer",
    #                     fields=[core.Field(name="name", type=types.STRING)],
    #                 ),
    #             },
    #         ),
    #     )
