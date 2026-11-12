"use client";

import { Section } from "@/app/_components/section";
import { Suspense } from "react";
import { getSession } from "../getSession";
import { DefaultMechanicsColumn, UserMechanicsColumn } from "./_components/UserMechanicsColumn";
import { getMechanics } from "./getMechanics";

const MechanicsPage = async () => {
  const mechanics = await getMechanics();
  const session = await getSession();

  const currentUserId = session?.id;
  const currentUserPseudo = session?.pseudo;
  const owner_ids = mechanics.owner_ids;
  const mechanics_names: string[] = mechanics.league_mechanics;
  const mechanics_mappings: { owner_id: string; pseudo: string; loot_mechanics: object }[] =
    mechanics.mechanics_mappings;

  return (
    <Section name="League Mechanics">
      <div className="flex">
        <div className="flex flex-col">
          <div className="border-b">Mechanics</div>
          {mechanics_names.map((name) => (
            <div key={name}>{name}</div>
          ))}
        </div>
        {currentUserId && !owner_ids.includes(currentUserId) && (
          <DefaultMechanicsColumn
            ownerId={currentUserId}
            ownerPseudo={currentUserPseudo}
            mechanicsNames={mechanics_names}
          />
        )}
        {mechanics_mappings.map((mechanics_mapping) => (
          <UserMechanicsColumn
            key={mechanics_mapping.owner_id}
            updatable={mechanics_mapping.owner_id === currentUserId}
            ownerId={mechanics_mapping.owner_id}
            ownerPseudo={mechanics_mapping.pseudo}
            mechanicsMapping={mechanics_mapping.loot_mechanics}
          />
        ))}
      </div>
    </Section>
  );
};

const MechanicsPageSuspense = async () => {
  return (
    <Suspense fallback="Loading ...">
      <MechanicsPage />
    </Suspense>
  );
};

export default MechanicsPageSuspense;
