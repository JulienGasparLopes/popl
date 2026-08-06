export default async function BuildPage({ params }: { params: Promise<{ buildId: number }> }) {
  const { buildId } = await params;

  const buildResponse = await fetch(`http://127.0.0.1:5000/builds/${buildId}`);
  const build = (await buildResponse.json()).build;

  return (
    <div>
      <a href="/builds">Builds list</a>
      <h1>Build {buildId}</h1>
      <div>{JSON.stringify(build)}</div>
    </div>
  );
}
