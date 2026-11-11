import { Card } from "@/app/_components/card";
import { Section } from "@/app/_components/section";
import { getSession } from "@/app/getSession";
import { Suspense } from "react";
import { getBuild } from "./getBuild";
import { RequiredItem } from "./item";

const BuildPageSuspense = async ({ params }: { params: Promise<{ buildId: string }> }) => {
  return (
    <Suspense fallback="Loading ...">
      <BuildPage params={params} />
    </Suspense>
  );
};

const BuildPage = async ({ params }: { params: Promise<{ buildId: string }> }) => {
  const { buildId } = await params;
  const build = await getBuild(buildId);
  const session = await getSession();
  console.log(session, build);
  const updatable = session && session.id === build.owner.id;

  return (
    <Section name={`${build.character_class} - ${build.character_ascendancy}`}>
      <div className="flex gap-4">
        <div className="flex flex-col gap-4 grow">
          <Card title="Informations">
            <h3>Id: {build.id}</h3>
            <h3>Life: {build.character_attributes.life}</h3>
            <h3>Mana: {build.character_attributes.mana}</h3>
            <h3>Strength: {build.character_attributes.strength}</h3>
            <h3>Dexterity: {build.character_attributes.dexterity}</h3>
            <h3>Intelligence: {build.character_attributes.intelligence}</h3>
          </Card>
          <Card title="Gems">
            {build.gems.map((gem_name: string) => {
              return <h3>{gem_name}</h3>;
            })}
          </Card>
        </div>
        <div className="flex flex-col gap-4 grow">
          <Card title="Armors">
            <RequiredItem
              updatable={updatable}
              buildId={build.id}
              name="Helmet"
              itemKey="helmet"
              itemInfo={build.equipment.helmet}
            />
            <RequiredItem
              updatable={updatable}
              buildId={build.id}
              name="Body"
              itemKey="body"
              itemInfo={build.equipment.body}
            />
            <RequiredItem
              updatable={updatable}
              buildId={build.id}
              name="Gloves"
              itemKey="gloves"
              itemInfo={build.equipment.gloves}
            />
            <RequiredItem
              updatable={updatable}
              buildId={build.id}
              name="Boots"
              itemKey="boots"
              itemInfo={build.equipment.boots}
            />
          </Card>
          <Card title="Jewellery">
            <RequiredItem
              updatable={updatable}
              buildId={build.id}
              name="Left Ring"
              itemKey="left_ring"
              itemInfo={build.equipment.left_ring}
            />
            <RequiredItem
              updatable={updatable}
              buildId={build.id}
              name="Right Ring"
              itemKey="right_ring"
              itemInfo={build.equipment.right_ring}
            />
            <RequiredItem
              updatable={updatable}
              buildId={build.id}
              name="Amulet"
              itemKey="amulet"
              itemInfo={build.equipment.amulet}
            />
            <RequiredItem
              updatable={updatable}
              buildId={build.id}
              name="Belt"
              itemKey="belt"
              itemInfo={build.equipment.belt}
            />
          </Card>
          <Card title="Weapons">
            <RequiredItem
              updatable={updatable}
              buildId={build.id}
              name="Left Hand"
              itemKey="left_hand"
              itemInfo={build.equipment.left_hand}
            />
            <RequiredItem
              updatable={updatable}
              buildId={build.id}
              name="Right Hand"
              itemKey="right_hand"
              itemInfo={build.equipment.right_hand}
            />
          </Card>
        </div>
        <div className="flex flex-col gap-4 grow">
          <Card title="Jewels">
            {build.jewels.map((jewelInfo: { name: string; obtained: boolean }, index: number) => {
              return (
                <RequiredItem
                  updatable={updatable}
                  buildId={build.id}
                  key={index}
                  itemKey={`jewels${index}`}
                  itemInfo={jewelInfo}
                />
              );
            })}
          </Card>
          {/* <Card title="Flasks">
            {build.flasks.map((flask_name: string) => {
              return <h3>{flask_name}</h3>;
            })}
          </Card> */}
        </div>
      </div>
    </Section>
  );
};

export default BuildPageSuspense;
