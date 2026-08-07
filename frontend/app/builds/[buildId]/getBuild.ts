import { cacheTag } from "next/cache";


export const getBuild = async (buildId: string) => {
    "use cache";
    cacheTag("build");
    const buildResponse = await fetch(`http://127.0.0.1:5000/builds/${buildId}`);

    return (await buildResponse.json()).build;
}