import { apiFetch } from "@/lib/api/client";
import { redirect } from "next/navigation";

export const login = async () => {
  const response = await apiFetch("/auth/google/login", {
    method: 'GET'
  })

  if (!response.ok)
    return null

  redirect("/mechanics")
}