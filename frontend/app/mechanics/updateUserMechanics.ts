"use server"

import { updateTag } from "next/cache";
import { cookies } from "next/headers";

export const updateUserMechanics = async (userId: string, mechanicsMapping: object) => {
    const cookieStore = await cookies();
    const sessionCookie = cookieStore.get('session')

    const body = mechanicsMapping;
    await fetch(`http://127.0.0.1:5000/mechanics/${userId}`, {
        method: 'POST',
        body: JSON.stringify(body),
        headers: {
            Cookie: `session=${sessionCookie!.value}`,
            'Content-Type': 'application/json',
        }

    })
    updateTag("mechanics")
}