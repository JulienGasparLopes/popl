import base64
import uuid
import zlib
from typing import Any
from xml.etree import ElementTree

from log import get_logger
from src.backend.domain.build.model.build import (
    Build,
    CharacterAttributes,
    Equipment,
    RequiredItem,
)
from src.backend.domain.build.ports.pob_build_service import PoBBuildServicePort
from src.backend.domain.items.application_service.service import make_item_service
from src.backend.domain.items.ports.service import ItemFilters

logger = get_logger(__name__)

_OUTPUT_TO_FILE = True

_ITEM_SLOT_TO_EQUIPMENT_ATTR = {
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


class PoBBuildService(PoBBuildServicePort):
    def __init__(self):
        self._item_service = make_item_service()

    def get_build_sets_from_pob_code(self, *, pob_code: str) -> dict[str, str]:
        base64_decode = base64.urlsafe_b64decode(pob_code)
        decompressed_xml = zlib.decompress(base64_decode).decode("utf-8")
        xml_obj = ElementTree.fromstring(decompressed_xml)
        item_set_tags = xml_obj.findall("Items/ItemSet")

        if len(item_set_tags) == 1 and "title" not in item_set_tags[0].attrib:
            return {item_set_tags[0].attrib["id"]: "popl_default_item_set_tag"}

        return {
            item_set_tag.attrib["id"]: item_set_tag.attrib["title"]
            for item_set_tag in item_set_tags
        }

    def parse_pob_code(
        self, *, pob_code: str, build_set_id: str, owner_id: uuid.UUID
    ) -> Build:
        base64_decode = base64.urlsafe_b64decode(pob_code)
        decompressed_xml = zlib.decompress(base64_decode).decode("utf-8")

        if _OUTPUT_TO_FILE:
            with open("scripts/output.xml", mode="w") as f:
                f.write(decompressed_xml)
            logger.info("Saved to file output.xml")

        xml_obj = ElementTree.fromstring(decompressed_xml)

        build_tag = xml_obj.find("Build")
        character_class = build_tag.attrib["className"]
        character_ascendancy = build_tag.attrib["ascendClassName"]

        def get_stat(stat_name: str) -> Any:
            return xml_obj.find(f'Build/PlayerStat[@stat="{stat_name}"]').attrib[
                "value"
            ]

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

        item_set_tag = xml_obj.find(f'Items/ItemSet[@id="{build_set_id}"]')

        for slot in item_set_tag.findall("Slot"):
            if (item_id := slot.attrib["itemId"]) != "0":
                item_id_to_slot_name[item_id] = slot.attrib["name"]

        for socket_slot in xml_obj.findall("Tree/Spec/Sockets/Socket"):
            item_id_to_slot_name[socket_slot.attrib["itemId"]] = "Jewel"

        unknown_items: list[str] = []
        # Equipment object is not frozen, we use that in our advantage (may change in the future)
        equipment = Equipment()
        jewels = []
        for item_id, item_name in item_name_by_id.items():
            if item_id not in item_id_to_slot_name:
                logger.warning(
                    f"Unable to find item {item_name} ({item_id}) relative slot. Skip."
                )
                continue
            slot_name = item_id_to_slot_name[item_id]

            if slot_name not in _ITEM_SLOT_TO_EQUIPMENT_ATTR:
                logger.warning(
                    f"Object of type {slot_name} is not supported. Skipping {item_name}"
                )
                continue

            attr_name = _ITEM_SLOT_TO_EQUIPMENT_ATTR[slot_name]

            if attr_name == "Flask":
                logger.warning(f"Flaks are not supported. Skipping {item_name}")
                continue

            matching_item = self._item_service.get_items(
                filters=ItemFilters(name={item_name})
            )
            if len(matching_item) < 1:
                unknown_items.append(f"[{attr_name}] {item_name}")
            else:
                if attr_name == "jewels":
                    jewels.append(RequiredItem(name=item_name, obtained=False))
                else:
                    equipment.__setattr__(
                        attr_name, RequiredItem(name=item_name, obtained=False)
                    )

        return Build(
            id=uuid.uuid4(),
            owner_id=owner_id,
            character_class=character_class,
            character_ascendancy=character_ascendancy,
            character_attributes=attributes,
            equipment=equipment,
            gems=[],
            jewels=jewels,
            notes=(
                f"Unrecognized items: {", ".join(unknown_items)}"
                if len(unknown_items) > 0
                else ""
            ),
        )


def make_pob_build_service() -> PoBBuildServicePort:
    return PoBBuildService()
