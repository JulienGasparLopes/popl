import { apiFetch } from "@/lib/api/client";

export const updateUserMechanics = async (userId: string, mechanicsMapping: object) => {

    const body = mechanicsMapping;
    await apiFetch(`/mechanics/${userId}`, {
        method: 'POST',
        credentials: "include",
        body: JSON.stringify(body),
        headers: {
            'Content-Type': 'application/json',
        }
    })
}