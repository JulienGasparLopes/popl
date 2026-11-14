import { apiFetch } from "@/lib/api/client";
import { connection } from "next/server";


type getBuildsType = () => Promise<Build[]>;

export const getBuilds: getBuildsType = async () => {
    connection();

    const buildResponse = await apiFetch("/builds");

    return (await buildResponse.json()).build;
}