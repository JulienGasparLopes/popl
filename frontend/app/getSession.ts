import { apiFetch } from "@/lib/api/client";

export const getSession = async () => {
  const response = await apiFetch("/auth/me", {
    method: 'GET',
    cache: "reload"
  })

  if (!response.ok)
    return null

  return await response.json()
}