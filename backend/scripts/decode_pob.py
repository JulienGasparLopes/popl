import base64
import zlib
from typing import Any
from xml.etree import ElementTree

from domain.build.model.build import Build, CharacterAttributes, Equipment
from log import get_logger

logger = get_logger(__name__)

OUTPUT_TO_FILE = False

ITEM_SLOT_TO_EQUIPMENT_ATTR = {
    "Ring 1": "left_ring",
    "Ring 2": "right_ring",
    "Boots": "boots",
    "gloves": "gloves",
    "Body Armour": "body",
    "Helmet": "helmet",
    "Belt": "belt",
    "Amulet": "amulet",
    "Weapon 1": "left_hand",
    "Weapon 2": "right_hand",
    "Flask 1": "Flask",
    "Flask 2": "Flask",
    "Flask 3": "Flask",
    "Flask 4": "Flask",
    "Flask 5": "Flask",
    "Jewel": "jewels",
}


def main() -> None:
    pob_code = ""
    with open("scripts/input.txt") as f:
        pob_code = f.read()

    base64_decode = base64.urlsafe_b64decode(pob_code)
    decompressed_xml = zlib.decompress(base64_decode).decode("utf-8")
    xml_obj = ElementTree.fromstring(decompressed_xml)

    def get_stat(stat_name: str) -> Any:
        return xml_obj.find(f'Build/PlayerStat[@stat="{stat_name}"]').attrib["value"]

    attributes = CharacterAttributes(
        life=get_stat("Life"),
        mana=get_stat("Mana"),
        strength=get_stat("Str"),
        dexterity=get_stat("Dex"),
        intelligence=get_stat("Int"),
        armour=get_stat("Armour"),
        energy_shield=get_stat("EnergyShield"),
        evasion=get_stat("Evasion"),
        power_charges=get_stat("PowerChargesMax"),
        endurance_charges=get_stat("EnduranceChargesMax"),
        frenzy_charges=get_stat("FrenzyChargesMax"),
    )

    item_name_by_id = {}

    for item_tag in xml_obj.findall("Items/Item"):
        rarity, name, *_ = [a.strip() for a in item_tag.text.strip().split("\n")]
        # Process only unique items
        if "UNIQUE" not in rarity:
            continue
        item_name_by_id[item_tag.attrib["id"]] = name

    item_id_to_slot_name = {}

    item_set_tags = xml_obj.findall("Items/ItemSet")
    item_set_tag = item_set_tags[0]
    if len(item_set_tags) > 1:
        logger.warning(
            f"Found more than one ItemSet. Using set with id {item_set_tag.attrib["id"]}"
        )
    for slot in item_set_tag.findall("Slot"):
        if (item_id := slot.attrib["itemId"]) != "0":
            item_id_to_slot_name[item_id] = slot.attrib["name"]

    for socket_slot in xml_obj.findall("Tree/Spec/Sockets/Socket"):
        item_id_to_slot_name[socket_slot.attrib["itemId"]] = "Jewel"

    # Equipment object is not frozen, we use that in our advantage (may change in the future)
    equipment = Equipment()
    jewels = []
    for item_id, item_name in item_name_by_id.items():
        slot_name = item_id_to_slot_name[item_id]

        if slot_name not in ITEM_SLOT_TO_EQUIPMENT_ATTR:
            logger.warning(
                f"Object of type {slot_name} is not supported. Skipping {item_name}"
            )
            continue

        attr_name = ITEM_SLOT_TO_EQUIPMENT_ATTR[slot_name]

        if attr_name == "Flask":
            logger.warning(f"Flaks are not supported. Skipping {item_name}")
            continue

        if attr_name == "jewels":
            jewels.append(item_name)
        else:
            equipment.__setattr__(attr_name, item_name)

    build = Build(
        character_class="",
        character_ascendancy="",
        character_attributes=attributes,
        equipment=equipment,
        gems=[],
        jewels=jewels,
    )

    logger.info(build)

    if OUTPUT_TO_FILE:
        with open("scripts/output.xml", mode="w") as f:
            f.write(decompressed_xml)
        logger.info("Saved to file output.xml")


if __name__ == "__main__":
    main()
