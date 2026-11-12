export const updateUserMechanics = async (userId: string, mechanicsMapping: object) => {

    const body = mechanicsMapping;
    await fetch(`http://backend:5000/mechanics/${userId}`, {
        method: 'POST',
        credentials: "include",
        body: JSON.stringify(body),
        headers: {
            'Content-Type': 'application/json',
        }
    })
}