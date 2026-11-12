import { updateTag } from 'next/cache';

export const setItemsObtained = async (buildId: string, itemsObtained: object) => {
  await fetch(`http://backend:5000/builds/${buildId}/set_items_obtained`, {
    method: 'POST',
    credentials: "include",
    body: JSON.stringify(itemsObtained),
    headers: {
      'Content-Type': 'application/json',
    }
  })

  updateTag("build")
}