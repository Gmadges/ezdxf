# Copyright (c) 2014-2019, Manfred Moitzi
# License: MIT License
import pytest

from ezdxf.sections.acdsdata import AcDsDataSection
from ezdxf import DXFKeyError
from ezdxf.lldxf.tags import internal_tag_compiler, group_tags
from ezdxf.lldxf.tagwriter import TagCollector, basic_tags_from_text


@pytest.fixture
def section():
    entities = group_tags(internal_tag_compiler(ACDSSECTION))
    return AcDsDataSection(None, entities)


def test_loader(section):
    assert "ACDSDATA" == section.name.upper()
    assert len(section.entities) > 0


def test_acds_record(section):
    records = [
        entity
        for entity in section.entities
        if entity.dxftype() == "ACDSRECORD"
    ]
    assert len(records) > 0
    record = records[0]
    assert record.has_section("ASM_Data") is True
    assert record.has_section("AcDbDs::ID") is True
    assert record.has_section("mozman") is False
    with pytest.raises(DXFKeyError):
        _ = record.get_section("mozman")

    asm_data = record.get_section("ASM_Data")
    binary_data = (tag for tag in asm_data if tag.code == 310)
    length = sum(len(tag.value) for tag in binary_data)
    assert asm_data[2].value == length


def test_write_dxf(section):
    result = TagCollector.dxftags(section)
    expected = basic_tags_from_text(ACDSSECTION)
    assert result[:-1] == expected


ACDSSECTION = """0
SECTION
2
ACDSDATA
70
2
71
6
0
ACDSSCHEMA
90
0
1
AcDb3DSolid_ASM_Data
2
AcDbDs::ID
280
10
91
8
2
ASM_Data
280
15
91
0
101
ACDSRECORD
95
0
90
2
2
AcDbDs::TreatedAsObjectData
280
1
291
1
101
ACDSRECORD
95
0
90
3
2
AcDbDs::Legacy
280
1
291
1
101
ACDSRECORD
1
AcDbDs::ID
90
4
2
AcDs:Indexable
280
1
291
1
101
ACDSRECORD
1
AcDbDs::ID
90
5
2
AcDbDs::HandleAttribute
280
7
282
1
0
ACDSSCHEMA
90
1
1
AcDb_Thumbnail_Schema
2
AcDbDs::ID
280
10
91
8
2
Thumbnail_Data
280
15
91
0
101
ACDSRECORD
95
1
90
2
2
AcDbDs::TreatedAsObjectData
280
1
291
1
101
ACDSRECORD
95
1
90
3
2
AcDbDs::Legacy
280
1
291
1
101
ACDSRECORD
1
AcDbDs::ID
90
4
2
AcDs:Indexable
280
1
291
1
101
ACDSRECORD
1
AcDbDs::ID
90
5
2
AcDbDs::HandleAttribute
280
7
282
1
0
ACDSSCHEMA
90
2
1
AcDbDs::TreatedAsObjectDataSchema
2
AcDbDs::TreatedAsObjectData
280
1
91
0
0
ACDSSCHEMA
90
3
1
AcDbDs::LegacySchema
2
AcDbDs::Legacy
280
1
91
0
0
ACDSSCHEMA
90
4
1
AcDbDs::IndexedPropertySchema
2
AcDs:Indexable
280
1
91
0
0
ACDSSCHEMA
90
5
1
AcDbDs::HandleAttributeSchema
2
AcDbDs::HandleAttribute
280
7
91
1
284
1
0
ACDSRECORD
90
0
2
AcDbDs::ID
280
10
320
339
2
ASM_Data
280
15
94
1088
310
414349532042696E61727946696C652855000000000000020000000C00000007104175746F6465736B204175746F434144071841534D203231392E302E302E3536303020556E6B6E6F776E071853756E204D61792020342031353A34373A3233203230313406000000000000F03F068DEDB5A0F7C6B03E06BBBDD7D9DF7CDB
310
3D0D0961736D6865616465720CFFFFFFFF04FFFFFFFF070C3231392E302E302E35363030110D04626F64790C0200000004FFFFFFFF0CFFFFFFFF0C030000000CFFFFFFFF0CFFFFFFFF110E067265665F76740E036579650D066174747269620CFFFFFFFF04FFFFFFFF0CFFFFFFFF0CFFFFFFFF0C010000000C040000000C05
310
000000110D046C756D700C0600000004FFFFFFFF0CFFFFFFFF0CFFFFFFFF0C070000000C01000000110D0E6579655F726566696E656D656E740CFFFFFFFF04FFFFFFFF070567726964200401000000070374726904010000000704737572660400000000070361646A040000000007046772616404000000000709706F7374
310
636865636B0400000000070463616C6304010000000704636F6E760400000000070473746F6C06000000E001FD414007046E746F6C060000000000003E4007046473696C0600000000000000000708666C61746E6573730600000000000000000707706978617265610600000000000000000704686D617806000000000000
310
0000070667726964617206000000000000000007056D6772696404B80B0000070575677269640400000000070576677269640400000000070A656E645F6669656C6473110D0F7665727465785F74656D706C6174650CFFFFFFFF04FFFFFFFF0403000000040000000004010000000408000000110E067265665F76740E0365
310
79650D066174747269620CFFFFFFFF04FFFFFFFF0CFFFFFFFF0CFFFFFFFF0C030000000C040000000C05000000110D057368656C6C0C0800000004FFFFFFFF0CFFFFFFFF0CFFFFFFFF0CFFFFFFFF0C090000000CFFFFFFFF0C03000000110E067265665F76740E036579650D066174747269620CFFFFFFFF04FFFFFFFF0CFF
310
FFFFFF0CFFFFFFFF0C070000000C040000000C05000000110D04666163650C0A00000004FFFFFFFF0CFFFFFFFF0CFFFFFFFF0CFFFFFFFF0C070000000CFFFFFFFF0C0B0000000B0B110E05666D6573680E036579650D066174747269620CFFFFFFFF04FFFFFFFF0C0C0000000CFFFFFFFF0C09000000110E05746F7275730D
310
07737572666163650CFFFFFFFF04FFFFFFFF0CFFFFFFFF131D7B018BA58BA7C0600EB0424970BC4000000000000000001400000000000000000000000000000000000000000000F03F065087D2E2C5418940066050CEE5F3CA644014000000000000F03F000000000000000000000000000000000B0B0B0B0B110E06726566
310
5F76740E036579650D066174747269620CFFFFFFFF04FFFFFFFF0CFFFFFFFF0C0A0000000C090000000C040000000C05000000110E03456E640E026F660E0341534D0D0464617461
"""
