type ItemInfo = { name: string, obtained: boolean, };

type Build = {
    id: string; character_class: string; character_ascendancy: string,
    character_attributes: {
        life: number
        mana: number,
        strength: number,
        dexterity: number,
        intelligence: number,
    },
    equipment: {
        right_ring: ItemInfo,
        amulet: ItemInfo,
        belt: ItemInfo,
        left_hand: ItemInfo,
        right_hand: ItemInfo,
        helmet: ItemInfo,
        body: ItemInfo,
        gloves: ItemInfo,
        boots: ItemInfo,
        left_ring: ItemInfo,
    }
    jewels: ItemInfo[],
    gems: string[]
};
