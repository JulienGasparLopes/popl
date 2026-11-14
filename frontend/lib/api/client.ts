function getBackendUrl() {
    const url = process.env.BACKEND_URL;

    if (!url) {
        throw new Error("BACKEND_URL is not configured");
    }

    return url;
}

export async function apiFetch(
    endpoint: string,
    options?: RequestInit
) {
    return fetch(`${getBackendUrl()}${endpoint}`, options);
}