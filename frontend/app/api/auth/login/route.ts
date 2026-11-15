import { forwardToBackend } from "@/lib/api/forwardToBackend";

export async function GET(request: Request) {
    return forwardToBackend("/auth/google/login", request);
}