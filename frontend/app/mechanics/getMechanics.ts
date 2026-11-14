import { apiFetch } from "@/lib/api/client";

export const getMechanics = async () => {
  const response = await apiFetch('/mechanics', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  })

  if (!response.ok)
    return null;

  return (await response.json())
}