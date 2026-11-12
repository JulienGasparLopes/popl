
export const getWantedItems = async () => {
  const response = await fetch('http://backend:5000/wanted_items', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  })

  return (await response.json())
}