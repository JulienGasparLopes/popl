import { apiFetch } from "@/lib/api/client";


type getBuildsType = () => Promise<Build[]>;

export const getBuilds: getBuildsType = async () => {

    const buildResponse = await apiFetch("/builds");

    return (await buildResponse.json()).builds;
}