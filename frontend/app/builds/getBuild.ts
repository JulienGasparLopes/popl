export const createBuild = async (pobCode: string, buildSetId: string) => {

  const body = {
    "pob_code": pobCode,
    "build_set_id": buildSetId,
  }

  await fetch('http://127.0.0.1:5000/pob/create_build', {
    method: 'POST',
    body: JSON.stringify(body),
    headers: {
      'Content-Type': 'application/json',
    }

  })
}