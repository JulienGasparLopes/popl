"use server"


import { updateTag } from "next/cache";

export const updateUserMechanics = async (userId: string, mechanicsMapping: object) => {
    const body = mechanicsMapping;
    await fetch(`http://127.0.0.1:5000/mechanics/${userId}`, {
        method: 'POST',
        body: JSON.stringify(body),
        headers: {
            'Content-Type': 'application/json',
        }

    })
    updateTag("mechanics")
}