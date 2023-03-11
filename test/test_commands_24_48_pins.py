import pytest

from src.escp import Commands_24_48_Pin, CharacterTable


@pytest.fixture
def commands():
    return Commands_24_48_Pin()


@pytest.mark.parametrize(
    'ct,expected_buffer', [(0, b'\x1bt\x00'), (1, b'\x1bt\x01'), (2, b'\x1bt\x02'), (3, b'\x1bt\x03')]
)
def test_select_character_table(commands, ct, expected_buffer):
    assert commands.select_character_table(ct).buffer == expected_buffer


def test_select_character_table_invalid(commands):
    with pytest.raises(ValueError):
        commands.select_character_table(5)


@pytest.mark.parametrize(
    'table,character_table,expected_buffer',
    [
        (0, CharacterTable.ITALIC, b'\x1b\x28\x74\x03\x00\x00\x00\x00'),
        (0, CharacterTable.PC437_US, b'\x1b\x28\x74\x03\x00\x00\x01\x00'),
        (1, CharacterTable.PC437_US, b'\x1b\x28\x74\x03\x00\x01\x01\x00'),
        (2, CharacterTable.PC_AR864, b'\x1b\x28\x74\x03\x00\x02\x0d\x20'),
    ]
)
def test_assign_character_table(commands, table, character_table, expected_buffer):
    assert commands.assign_character_table(table, character_table).buffer == expected_buffer
