"use client";

import { formEventToData } from "@/helpers";
import { redirect } from "next/navigation";
import { SubmitEvent, useState } from "react";
import { Button } from "../_components/inputs";
import { Section } from "../_components/section";
import { SubTitle } from "../_components/titles";
import { createBuild } from "./createBuild";
import { getBuildSets } from "./getBuildSets";

export default function BuildListContent({ builds }: { builds: Build[] }) {
  const [buildSetIdToName, setBuildSetIdToName] = useState<Record<string, string>>({});
  const [pobCode, setPobCode] = useState<string>("");

  const onSubmitPoBCode = async (event: SubmitEvent<HTMLFormElement>) => {
    const data = formEventToData(event);
    const buildSetIdToName = await getBuildSets(data.pob_code);
    const buildIds = Object.keys(buildSetIdToName);

    if (buildIds.length == 1) {
      const buildId = await createBuild(data.pob_code, buildIds[0]);
      redirect(`/builds/${buildId}`);
    }

    setBuildSetIdToName(buildSetIdToName);
  };

  const onSubmitCreateBuild = async (event: SubmitEvent<HTMLFormElement>) => {
    const data = formEventToData(event);
    const buildId = await createBuild(data.pob_code, data.build_set_id);
    redirect(`/builds/${buildId}`);
  };

  return (
    <div className="flex flex-col gap-8">
      <Section name="Builds List">
        {builds.map((build, index) => {
          return (
            <div key={index}>
              <a href={`/builds/${build.id}`}>
                {build.character_class} - {build.character_ascendancy}
              </a>
              <hr></hr>
            </div>
          );
        })}
      </Section>

      <Section name="Import New Build">
        <div className="mb-4">
          <form onSubmit={onSubmitPoBCode}>
            <SubTitle subtitle="PoB Code" />
            <div className="outline-1 -outline-offset-1 outline-gray-600 border rounded-sm w-fit">
              <input
                type="text"
                name="pob_code"
                onChange={(event) => {
                  setPobCode(event.target.value);
                }}
                className="outline-gray-500 focus:outline-blue-500"
              />
            </div>
            <Button title="Load PoB Code" />
          </form>
        </div>

        {Object.entries(buildSetIdToName).length > 0 && (
          <div>
            <SubTitle subtitle="Select Build Set to use" />
            <form onSubmit={onSubmitCreateBuild}>
              <div className="outline-1 -outline-offset-1 outline-gray-600 border rounded-sm w-fit">
                <select name="build_set_id">
                  {Object.entries(buildSetIdToName).map(([buildSetId, buildSetName]) => (
                    <option value={buildSetId} key={buildSetId}>
                      [{buildSetId}] {buildSetName}
                    </option>
                  ))}
                </select>
              </div>
              <input type="text" name="pob_code" hidden={true} value={pobCode} readOnly />
              <Button title="Create Build" />
            </form>
          </div>
        )}
      </Section>
    </div>
  );
}
