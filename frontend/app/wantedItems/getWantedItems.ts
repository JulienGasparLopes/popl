import { apiFetch } from "@/lib/api/client"

export const getWantedItems = async () => {
  const response = await apiFetch('/wanted_items', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  })

  return (await response.json())
}