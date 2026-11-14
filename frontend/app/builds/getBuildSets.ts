import { apiFetch } from "@/lib/api/client";

export const getBuildSets = async (pobCode: string) => {
  const body = {
    "pob_code": pobCode,
  };
  const response = await apiFetch("/pob/parse_build_sets", {
    method: 'POST',
    body: JSON.stringify(body),
  })

  const data = await response.json()
  return data.build_sets
}