import { Suspense } from "react";
import { Section } from "../_components/section";
import { getWantedItems } from "./getWantedItems";
import { ItemInfoCell } from "./itemInfoCell";

const WantedItemsPage = async () => {
  const wantedItems = await getWantedItems();

  return (
    <Section name="Wanted Items">
      <table className="table-auto">
        <thead>
          <tr className="border-b">
            <th scope="col">Item</th>
            <th scope="col" className="border-l">
              Wishes
            </th>
            <th scope="col" className="border-l">
              Info
            </th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(wantedItems).map(([itemName, wishes]) => {
            return (
              <tr key={itemName} className="border-b">
                <td scope="row">{itemName}</td>
                <td className="border-l">{wishes["total"]}</td>
                <td className="border-l" data-tooltip-id={`tooltip-${itemName}`}>
                  <ItemInfoCell itemName={itemName} wishes={wishes} />
                  <div>Monsters: {JSON.stringify(wishes["info"]["drop_monsters"])}</div>
                  <div>Areas: {JSON.stringify(wishes["info"]["drop_areas"])}</div>
                  <div>Tags: {JSON.stringify(wishes["info"]["acquisition_tags"])}</div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </Section>
  );
};

const WantedItemsPageSuspense = async () => {
  return (
    <Suspense fallback="Loading ...">
      <WantedItemsPage />
    </Suspense>
  );
};

export default WantedItemsPageSuspense;
