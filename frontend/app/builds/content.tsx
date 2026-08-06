"use client";

import { formEventToData } from "@/helpers";
import { redirect } from "next/navigation";
import { SubmitEvent, useState } from "react";
import { createBuild } from "./create_build";
import { getBuildSets } from "./get_build_sets";

export default function BuildListContent({ builds }) {
  const [buildSetIdToName, setBuildSetIdToName] = useState({});
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
    <>
      <div>Build List</div>
      {builds.map((build, index) => {
        return (
          <div key={index}>
            <a href={`/builds/${build.id}`}>
              {build.character_class} - {build.character_ascendancy}
            </a>
          </div>
        );
      })}

      <div>Import Build</div>

      <form onSubmit={onSubmitPoBCode}>
        <div>PoB Code:</div>
        <input
          type="text"
          name="pob_code"
          onChange={(event) => {
            setPobCode(event.target.value);
          }}
        />
        <button type="submit">Load PoB Code</button>
      </form>

      {Object.entries(buildSetIdToName).length > 0 && (
        <div>
          <div>Select Build Set to use</div>
          <form onSubmit={onSubmitCreateBuild}>
            <select name="build_set_id">
              {Object.entries(buildSetIdToName).map(([buildSetId, buildSetName]) => (
                <option value={buildSetId} key={buildSetId}>
                  [{buildSetId}] {buildSetName}
                </option>
              ))}
            </select>
            <input type="text" name="pob_code" hidden={true} value={pobCode} readOnly></input>
            <button type="submit">Create Build</button>
          </form>
        </div>
      )}
    </>
  );
}
