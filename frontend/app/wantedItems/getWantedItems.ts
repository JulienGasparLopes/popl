
export const getWantedItems = async () => {
  const response = await fetch('http://127.0.0.1:5000/wanted_items', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  })

  return (await response.json())
}