export default async function Home() {
  const itemsResponse = await fetch("http://127.0.0.1:5000/items");
  const items: object[] = (await itemsResponse.json()).items;

  const itemsByClass = items.reduce((acc, item) => {
    const values = acc?.[item.item_class] || [];
    values.push(item);
    acc[item.item_class] = values;
    return acc;
  }, {});

  return (
    <main>
      Coucou
      {Object.entries(itemsByClass).map(([key, values]) => {
        return (
          <div key={key}>
            <h1>{key}</h1>
            <select>
              <option value="None">None</option>
              {values.map((value) => (
                <option key={value.name} value={value.name}>
                  {value.name}
                </option>
              ))}
            </select>
          </div>
        );
      })}
    </main>
  );
}
