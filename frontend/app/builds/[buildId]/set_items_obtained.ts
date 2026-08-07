"use server"

import { updateTag } from 'next/cache'

export const setItemsObtained = async (buildId: string, itemsObtained: object) => {

  await fetch(`http://127.0.0.1:5000/builds/${buildId}/set_items_obtained`, {
    method: 'POST',
    body: JSON.stringify(itemsObtained),
    headers: {
      'Content-Type': 'application/json',
    }
  })

  updateTag("build")
}