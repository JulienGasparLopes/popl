import { apiFetch } from "@/lib/api/client"

export const createBuild = async (pobCode: string, buildSetId: string) => {

  const body = {
    "pob_code": pobCode,
    "build_set_id": buildSetId,
  }

  const response = await apiFetch("/pob/create_build", {
    method: 'POST',
    body: JSON.stringify(body),
  })

  const data = await response.json()
  return data.build_id
}