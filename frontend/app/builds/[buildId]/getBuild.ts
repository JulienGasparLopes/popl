import { cacheTag } from "next/cache";


type getBuildType = (buildId: string) => Promise<Build>;

export const getBuild: getBuildType = async (buildId: string) => {
    "use cache";
    cacheTag("build");
    const buildResponse = await fetch(`http://backend:5000/builds/${buildId}`);

    return (await buildResponse.json()).build;
}