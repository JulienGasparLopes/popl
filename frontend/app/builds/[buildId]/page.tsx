import { Card } from "@/app/_components/card";
import { Section } from "@/app/_components/section";

export default async function BuildPage({ params }: { params: Promise<{ buildId: number }> }) {
  const { buildId } = await params;

  const buildResponse = await fetch(`http://127.0.0.1:5000/builds/${buildId}`);
  const build = (await buildResponse.json()).build;

  return (
    <Section name={`${build.character_class} - ${build.character_ascendancy}`}>
      <div className="flex gap-4">
        <div className="flex flex-col gap-4 grow">
          <Card title="Informations">
            <h3>Id: {buildId}</h3>
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
            <h3>Helmet: {build.equipment.helmet}</h3>
            <h3>Body: {build.equipment.body}</h3>
            <h3>Gloves: {build.equipment.gloves}</h3>
            <h3>Boots: {build.equipment.boots}</h3>
          </Card>
          <Card title="Jewellery">
            <h3>Left Ring: {build.equipment.left_ring}</h3>
            <h3>Right Ring: {build.equipment.right_ring}</h3>
            <h3>Amulet: {build.equipment.amulet}</h3>
            <h3>Belt: {build.equipment.belt}</h3>
          </Card>
          <Card title="Weapons">
            <h3>Left Hand: {build.equipment.left_hand}</h3>
            <h3>Right Hand: {build.equipment.right_hand}</h3>
          </Card>
        </div>
        <div className="flex flex-col gap-4 grow">
          <Card title="Jewels">
            {build.jewels.map((jewel_name: string, index: number) => {
              return <h3 key={index}>{jewel_name}</h3>;
            })}
          </Card>
          {/* <Card title="Flasks">
            {build.flasks.map((flask_name: string) => {
              return <h3>{flask_name}</h3>;
            })}
          </Card> */}
          {/* <div className="w-80">{JSON.stringify(build, null, 2)}</div> */}
        </div>
      </div>
    </Section>
  );
}
