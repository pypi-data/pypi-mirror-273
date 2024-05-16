import typing
from dataclasses import dataclass
import datetime
from uuid import uuid4
import xml.etree.ElementTree as ET
from kywy.client.kawa_client import KawaClient as K


@dataclass
class TreeNode:
    id: str
    children: list['TreeNode']
    value: typing.Optional[str | int | float | bool | datetime.datetime | datetime.date] = None
    to_xml_func: any = None
    column_index = {}

    def to_xml(self, sheet):

        column_index = {}

        for column in sheet.get('indicatorColumns', []) + sheet.get('computedColumns', []):
            column_index[column.get('displayInformation').get('displayName')] = column.get('columnId')

        self._inject_column_ids(column_index)
        raw_xml = '<xml>' + self._to_xml() + '</xml>'
        element = ET.XML(raw_xml)
        ET.indent(element)
        return ET.tostring(element, encoding='unicode')

    def _inject_column_ids(self, column_index: dict[str, str]):
        for child in self.children:
            # In-place mutate the identifiers
            if child.id == 'identifier':
                column_name = child.value.strip()
                column_id = column_index.get(column_name)
                if not column_id:
                    raise ValueError(f'The column with name "{column_name}" was not found')
                child.value = column_id
            else:
                child._inject_column_ids(column_index)

    def _to_xml(self):
        node = self
        return self.to_xml_func(node)

    def binary_expression_xml(self):
        return f'''
        <block type="BINARY_EXPRESSION" id="{uuid4()}">
            <field name="operation_id">{self.id}</field>
            <value name="left">{self.children[0]._to_xml()}</value>
            <value name="right">{self.children[1]._to_xml()}</value>
        </block>'''

    def call_expression_xml(self):
        inputs = []
        input_counter = 0
        for child in self.children:
            input_counter += 1
            inputs.append(f'<value name="input{input_counter}">{child._to_xml()}</value>')

        inputs_xml = '\n'.join(inputs)
        return f'''
            <block type="CALL_EXPRESSION" id="{uuid4()}">
                <field name="operation_id">{self.id}</field>
                {inputs_xml}
            </block>'''

    def literal_xml(self):
        # TODO
        if isinstance(self.value, str):
            kawa_type = 'text'
        else:
            kawa_type = 'integer'

        return f'''
            <block type="LITERAL" id="{uuid4()}">
                <field name="type">{kawa_type}</field>
                <field name="value">{self.value}</field>
            </block>
        '''

    def identifier_xml(self):
        return f'''
              <block type="IDENTIFIER" id="{uuid4()}">
                <field name="type">text</field>
                <field name="reference">{self.value}</field>
            </block>
           '''


def binary_expression(operation_id: str, node1: TreeNode, node2: TreeNode) -> TreeNode:
    return TreeNode(
        id=operation_id,
        children=[node1, node2],
        to_xml_func=lambda node: node.binary_expression_xml(),
    )


def call_expression(operation_id: str, children: list[TreeNode]) -> TreeNode:
    return TreeNode(
        id=operation_id,
        children=children,
        to_xml_func=lambda node: node.call_expression_xml(),
    )


def val(value: str | int | float | bool | datetime.datetime | datetime.date) -> TreeNode:
    if value == ' ':
        return space()
    else:
        return TreeNode(
            id='val',
            children=[],
            value=value,
            to_xml_func=lambda node: node.literal_xml(),
        )


def identifier(identifier_value: str) -> TreeNode:
    return TreeNode(
        id='identifier',
        children=[],
        value=identifier_value,
        to_xml_func=lambda node: node.identifier_xml(),
    )


def col(column_name: str): return call_expression('COLUMN', [identifier(column_name)])


def length(input_node: TreeNode): return call_expression('LEN', [input_node])


def str_(input_node: TreeNode): return call_expression('TEXT', [input_node])


def extract(input_text: TreeNode, regexp: TreeNode):
    return call_expression('EXTRACT', [input_text, regexp])


def add(node1: TreeNode, node2: TreeNode): return binary_expression('ADDITION', node1, node2)


def sub(node1: TreeNode, node2: TreeNode): return binary_expression('SUBTRACTION', node1, node2)


def mul(node1: TreeNode, node2: TreeNode): return binary_expression('MULTIPLICATION', node1, node2)


def div(node1: TreeNode, node2: TreeNode): return binary_expression('DIVISION', node1, node2)


def ge(node1: TreeNode, node2: TreeNode): return binary_expression('GREATER_THAN_OR_EQUAL', node1, node2)


def gt(node1: TreeNode, node2: TreeNode): return binary_expression('STRICTLY_GREATER_THAN', node1, node2)


def le(node1: TreeNode, node2: TreeNode): return binary_expression('LESSER_THAN_OR_EQUAL', node1, node2)


def lt(node1: TreeNode, node2: TreeNode): return binary_expression('STRICTLY_LESSER_THAN', node1, node2)


def eq(node1: TreeNode, node2: TreeNode): return binary_expression('EQUAL', node1, node2)


def ne(node1: TreeNode, node2: TreeNode): return binary_expression('NOT_EQUAL', node1, node2)


def space(): return call_expression('SPACE', [])


def power(node1: TreeNode, node2: TreeNode): return call_expression('POWER', [node1, node2])


def starts_with(node1: TreeNode, node2: TreeNode): return call_expression('BEGINS_WITH', [node1, node2])


def ends_with(node1: TreeNode, node2: TreeNode): return call_expression('ENDS_WITH', [node1, node2])


def contains(node1: TreeNode, node2: TreeNode): return call_expression('CONTAINS', [node1, node2])


def left(node1: TreeNode, node2: TreeNode): return call_expression('LEFT', [node1, node2])


def right(node1: TreeNode, node2: TreeNode): return call_expression('RIGHT', [node1, node2])


def find(node1: TreeNode, node2: TreeNode): return call_expression('FIND', [node1, node2])


def substring(node1: TreeNode, node2: TreeNode): return call_expression('SUBSTRING', [node1, node2])


def replace_all(node1: TreeNode, node2: TreeNode, node3: TreeNode):
    return call_expression('SUBSTITUTE_ALL', [node1, node2, node3])


def replace_first(node1: TreeNode, node2: TreeNode, node3: TreeNode):
    return call_expression('SUBSTITUTE', [node1, node2, node3])


def abs_(node1: TreeNode): return call_expression('ABS', [node1])


def not_(node1: TreeNode): return call_expression('NOT', [node1])


def in_list(*nodes: list[TreeNode]): return call_expression('IN_LIST', list(nodes))


def largest(node1: TreeNode, node2: TreeNode): return call_expression('LARGEST', [node1, node2])


def smallest(node1: TreeNode, node2: TreeNode): return call_expression('SMALLEST', [node1, node2])


def lower(node1: TreeNode): return call_expression('LOWER', [node1])


def upper(node1: TreeNode): return call_expression('UPPER', [node1])


def trim(node1: TreeNode): return call_expression('TRIM', [node1])


def concat(*nodes: list[TreeNode]): return call_expression('CONCAT', list(nodes))


def if_then_else(*nodes: list[TreeNode]): return call_expression('IF', list(nodes))


def or_(*nodes: list[TreeNode]): return call_expression('OR', list(nodes))


def and_(*nodes: list[TreeNode]): return call_expression('AND', list(nodes))


if __name__ == '__main__':
    if_then_else(val(1), val(2), val(3))

    # workspace_id = 14
    # sheet_id = 973
    # kawa = K.load_client_from_environment()
    # kawa.set_active_workspace_id(workspace_id)
    # current_sheet = kawa.entities.sheets().get_entity_by_id(id=sheet_id)
    #
    # json_content = '''
    # {
    #   "output": "<xml>\n            <block type=\"CALL_EXPRESSION\" id=\"65740101-151a-42ff-ac0e-48d73d847ba1\">\n                <field name=\"operation_id\">EXTRACT</field>\n                <value name=\"input1\">\n            <block type=\"CALL_EXPRESSION\" id=\"a6f18fc3-716e-4a9c-8ecd-1020b8571e7c\">\n                <field name=\"operation_id\">COLUMN</field>\n                <value name=\"input1\">\n              <block type=\"IDENTIFIER\" id=\"e16d5f45-d4d1-4938-90aa-34aaf821c72a\">\n                <field name=\"type\">text</field>\n                <field name=\"reference\">1003⟶description</field>\n            </block>\n           </value>\n            </block></value>\n<value name=\"input2\">\n            <block type=\"LITERAL\" id=\"74e14f50-9698-4ba1-b4c6-e0359b1ad968\">\n                <field name=\"type\">text</field>\n                <field name=\"value\">\\b[0-9]{4}\\b</field>\n            </block>\n        </value>\n            </block></xml>"
    # }
    # '''
    # import json
    #
    # xml = json.load(json_content)
    #
    # print(xml)

    # kawa.commands.run_command(
    #     command_name='updateColumnXmlSyntacticTree',
    #     command_parameters={
    #         "sheetId": str(sheet_id),
    #         "columnId": "analysis",
    #         "xmlSyntacticTree": xml,
    #         "parameters": [],
    #         "editorParameters": []
    #     }
    # )

    print()
