"use server"

import { apiFetch } from '@/lib/api/client';
import { updateTag } from 'next/cache';

export const setItemsObtained = async (buildId: string, itemsObtained: object) => {
  await apiFetch(`/builds/${buildId}/set_items_obtained`, {
    method: 'POST',
    body: JSON.stringify(itemsObtained),
  })

  updateTag("build")
}