export async function forwardToBackend(
    path: string,
    request: Request
) {
    const backendUrl = process.env.BACKEND_URL;

    if (!backendUrl) {
        throw new Error("BACKEND_URL is not configured");
    }

    const headers = new Headers();

    const cookie = request.headers.get("cookie");
    if (cookie) headers.set("cookie", cookie);

    const url = new URL(path, backendUrl);

    const response = await fetch(url, {
        method: request.method,
        headers,
        body:
            request.method === "GET" || request.method === "HEAD"
                ? undefined
                : await request.arrayBuffer(),
        redirect: "manual",
        cache: "no-store",
    });

    const responseHeaders = new Headers();

    for (const name of ["location"]) {
        const value = response.headers.get(name);
        if (value) responseHeaders.set(name, value);
    }

    for (const cookie of response.headers.getSetCookie()) {
        responseHeaders.append("set-cookie", cookie);
    }

    return new Response(response.body, {
        status: response.status,
        headers: responseHeaders,
    });
}