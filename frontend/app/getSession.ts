import { cookies } from "next/headers";

export const getSession = async () => {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get('session')

  if (!sessionCookie)
    return null;

  const response = await fetch('http://127.0.0.1:5000/auth/me', {
    method: 'GET',
    headers: {
      Cookie: `session=${sessionCookie.value}`,
      'Content-Type': 'application/json',
    },
    cache: "reload"
  })

  if (!response.ok)
    return null

  return await response.json()
}