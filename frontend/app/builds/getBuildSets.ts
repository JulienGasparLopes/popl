export const getBuildSets = async (pobCode: string) => {
  const body = {
    "pob_code": pobCode,
  };
  const response = await fetch('http://127.0.0.1:5000/pob/parse_build_sets', {
    method: 'POST',
    body: JSON.stringify(body),
    headers: {
      'Content-Type': 'application/json',
    }

  })

  const data = await response.json()
  return data.build_sets
}