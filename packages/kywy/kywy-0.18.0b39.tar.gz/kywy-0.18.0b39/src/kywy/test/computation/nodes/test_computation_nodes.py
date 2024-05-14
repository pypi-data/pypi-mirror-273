import unittest

from ....client.computation_nodes import *


class TestComputationDsl(unittest.TestCase):

    def test_that_computation_dsl_is_built(self):
        # given
        node = add(col('foo'), val(2))

        # when
        actual = node.to_serializable()

        # then
        self.assertDictEqual(
            actual,
            {
                'id': 'add',
                'children': [
                    {
                        'id': 'col',
                        'children': [
                            {
                                'id': 'val',
                                'children': [],
                                'value': 'foo'
                            }
                        ]
                    },
                    {
                        'id': 'val',
                        'children': [],
                        'value': 2
                    }
                ]
            }
        )
