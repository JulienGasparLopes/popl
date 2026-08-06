import BuildListContent from "./content";

export default async function BuildListPage() {
  const buildListResponse = await fetch("http://127.0.0.1:5000/builds");
  const builds: object[] = (await buildListResponse.json()).builds;

  return <BuildListContent builds={builds} />;
}
