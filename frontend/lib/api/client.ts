"use server"

import { cookies } from "next/headers";

export async function apiFetch(
    endpoint: string,
    options?: RequestInit
) {
    const url = process.env.BACKEND_URL;
    if (!url) {
        throw new Error("BACKEND_URL is not configured");
    }

    const cookieStore = await cookies();
    const sessionCookie = cookieStore.get('session')

    const headers: { 'Content-Type': string, Cookie?: string } = {
        'Content-Type': 'application/json',
    }
    if (sessionCookie)
        headers["Cookie"] = `session=${sessionCookie.value}`

    return fetch(`${url}${endpoint}`, { ...options, headers });
}