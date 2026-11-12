import { getSession } from "@/app/getSession";
import { Suspense } from "react";
import BuildCreationSection from "./_components/BuildCreationSection";
import BuildsTable from "./_components/BuildsTable";

const BuildListPageSuspense = async () => {
  return (
    <Suspense fallback="Loading ...">
      <BuildListPage />
    </Suspense>
  );
};

const BuildListPage = async () => {
  const buildListResponse = await fetch("http://backend:5000/builds");
  const builds: Build[] = (await buildListResponse.json()).builds;
  const session = await getSession();

  return (
    <div className="flex flex-col gap-8">
      <BuildsTable builds={builds} />
      {session && <BuildCreationSection builds={builds} />}
    </div>
  );
};

export default BuildListPageSuspense;
