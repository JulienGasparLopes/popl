"use client";

import { Section } from "../../_components/section";

export default function BuildsTable({ builds }: { builds: Build[] }) {
  return (
    <Section name="Builds List">
      {builds.map((build, index) => {
        return (
          <div key={index}>
            <a className="flex gap-8" href={`/builds/${build.id}`}>
              {build.character_class} - {build.character_ascendancy}
              <div>{build.owner.pseudo}</div>
            </a>
            <hr></hr>
          </div>
        );
      })}
    </Section>
  );
}
