import { Section } from "@/app/_components/section";
import { Suspense } from "react";
import { getMechanics } from "./getMechanics";
import { DefaultMechanicsColumn, UserMechanicsColumn } from "./UserMechanicsColumn";

const CURRENT_USER = "Cawat"

const MechanicsPage = async () => {
    const mechanics = await getMechanics();
    const users = mechanics.users_names
    const mechanics_names = mechanics.league_mechanics

    return <Section name="League Mechanics">
        <div className="flex">
            <div className="flex flex-col">
                <div className="border-b">Mechanics</div>
                {
                    mechanics_names.map(name => <div key={name}>{name}</div>)
                }
            </div>
            {!users.includes(CURRENT_USER) && <DefaultMechanicsColumn userId={CURRENT_USER} mechanicsNames={mechanics_names} />
            }
            {
                mechanics.mechanics_mappings.map(mechanics_mapping => <UserMechanicsColumn key={mechanics_mapping.user_id} userId={mechanics_mapping.user_id} mechanicsMapping={mechanics_mapping.loot_mechanics} />)
            }
        </div>
    </Section>
}

const MechanicsPageSuspense = async () => {
    return <Suspense fallback="Loading ...">
        <MechanicsPage />
    </Suspense>
}


export default MechanicsPageSuspense;