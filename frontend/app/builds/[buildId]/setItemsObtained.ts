"use server"

import { updateTag } from 'next/cache';
import { cookies } from 'next/headers';

export const setItemsObtained = async (buildId: string, itemsObtained: object) => {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get('session')

  await fetch(`http://127.0.0.1:5000/builds/${buildId}/set_items_obtained`, {
    method: 'POST',
    body: JSON.stringify(itemsObtained),
    headers: {
      Cookie: `session=${sessionCookie!.value}`,
      'Content-Type': 'application/json',
    }
  })

  updateTag("build")
}