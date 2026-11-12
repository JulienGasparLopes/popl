"use server"

import { cacheTag } from "next/cache";

export const getMechanics = async () => {
  "use cache";
  cacheTag("mechanics");

  const response = await fetch('http://127.0.0.1:5000/mechanics', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  })

  if (!response.ok)
    return null;

  return (await response.json())
}