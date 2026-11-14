"use server"

import { apiFetch } from "@/lib/api/client";

export const updateUserMechanics = async (userId: string, mechanicsMapping: object) => {
    await apiFetch(`/mechanics/${userId}`, {
        method: 'POST',
        body: JSON.stringify(mechanicsMapping),
    })
}