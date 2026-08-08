import { Suspense } from "react";
import BuildListContent from "./content";

const BuildListPageSuspense = async () => {
  return (
    <Suspense fallback="Loading ...">
      <BuildListPage />
    </Suspense>
  );
};

const BuildListPage = async () => {
  const buildListResponse = await fetch("http://127.0.0.1:5000/builds");
  const builds: Build[] = (await buildListResponse.json()).builds;

  return <BuildListContent builds={builds} />;
};

export default BuildListPageSuspense;
