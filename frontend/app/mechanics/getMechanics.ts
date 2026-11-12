export const getMechanics = async () => {
  const response = await fetch('http://backend:5000/mechanics', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  })

  if (!response.ok)
    return null;

  return (await response.json())
}