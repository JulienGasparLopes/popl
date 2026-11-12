export const getBuildSets = async (pobCode: string) => {
  const body = {
    "pob_code": pobCode,
  };
  const response = await fetch('http://backend:5000/pob/parse_build_sets', {
    method: 'POST',
    credentials: "include",
    body: JSON.stringify(body),
    headers: {
      'Content-Type': 'application/json',
    }

  })

  const data = await response.json()
  return data.build_sets
}