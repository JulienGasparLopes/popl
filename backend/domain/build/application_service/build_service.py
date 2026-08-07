import base64
import uuid
import zlib
from typing import Any
from xml.etree import ElementTree

from connectors.mongo_connector import MongoConnector
from domain.build.model.build import Build, CharacterAttributes, Equipment, RequiredItem
from domain.build.ports.build_service import BuildServicePort, ItemsObtained
from log import get_logger

logger = get_logger(__name__)

_OUTPUT_TO_FILE = True

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


class BuildService(BuildServicePort):

    def __init__(self):
        conn = MongoConnector()
        self._repository = conn.get_collection("builds")

    def get_builds(self, *, build_id: uuid.UUID | None = None) -> list[Build]:
        filters = {}
        if build_id is not None:
            filters["id"] = str(build_id)
        raw_builds = self._repository.find(filters)
        return [Build.model_validate(raw_build) for raw_build in raw_builds]

    def save_build(self, *, build: Build) -> str:
        data = {**build.model_dump(exclude=["id"]), "id": str(build.id)}
        self._repository.update_one({"id": str(build.id)}, {"$set": data}, upsert=True)

    def delete_builds(self, *, build_ids: list[uuid.UUID]) -> None:
        self._repository.delete_many({"id": {"$in": [str(b) for b in build_ids]}})

    def set_item_obtained(
        self, *, build_id: uuid.UUID, items_obtained: ItemsObtained
    ) -> None:
        build = self.get_builds(build_id=build_id)[0]

        if items_obtained.helmet is not None:
            build.equipment.helmet.obtained = items_obtained.helmet
        if items_obtained.body is not None:
            build.equipment.body.obtained = items_obtained.body
        if items_obtained.gloves is not None:
            build.equipment.gloves.obtained = items_obtained.gloves
        if items_obtained.boots is not None:
            build.equipment.boots.obtained = items_obtained.boots
        if items_obtained.left_hand is not None:
            build.equipment.left_hand.obtained = items_obtained.left_hand
        if items_obtained.right_hand is not None:
            build.equipment.right_hand.obtained = items_obtained.right_hand
        if items_obtained.left_ring is not None:
            build.equipment.left_ring.obtained = items_obtained.left_ring
        if items_obtained.right_ring is not None:
            build.equipment.right_ring.obtained = items_obtained.right_ring
        if items_obtained.amulet is not None:
            build.equipment.amulet.obtained = items_obtained.amulet
        if items_obtained.belt is not None:
            build.equipment.belt.obtained = items_obtained.belt

        self.save_build(build=build)

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

    def parse_pob_code(self, *, pob_code: str, build_set_id: str) -> Build:
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
                jewels.append(RequiredItem(name=item_name, obtained=False))
            else:
                equipment.__setattr__(
                    attr_name, RequiredItem(name=item_name, obtained=False)
                )

        return Build(
            id=uuid.uuid4(),
            character_class=character_class,
            character_ascendancy=character_ascendancy,
            character_attributes=attributes,
            equipment=equipment,
            gems=[],
            jewels=jewels,
        )


def make_build_service() -> BuildServicePort:
    return BuildService()
