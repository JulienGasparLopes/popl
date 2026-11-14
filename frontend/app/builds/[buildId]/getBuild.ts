import { apiFetch } from "@/lib/api/client";


type getBuildType = (buildId: string) => Promise<Build>;

export const getBuild: getBuildType = async (buildId: string) => {
    const buildResponse = await apiFetch(`/builds/${buildId}`);

    return (await buildResponse.json()).build;
}