import Image from "next/image";
import { Suspense } from "react";
import { Section } from "../_components/section";
import { getWantedItems } from "./getWantedItems";

const WantedItemsPage = async () => {
  const wantedItems: { [itemName: string]: ItemWhish } = await getWantedItems();

  return (
    <Section name="Wanted Items">
      <table className="table-auto">
        <thead className="border-t">
          <tr className="border-b">
            <th scope="col" className="border-l">
              Item
            </th>
            <th scope="col" className="border-l border-r">
              Wishes
            </th>
            {/* <th scope="col" className="border-l">
              Info
            </th> */}
          </tr>
        </thead>
        <tbody>
          {Object.entries(wantedItems).map(([itemName, wishes]) => {
            return (
              <tr key={itemName} className="border-b">
                <td scope="row" className="border-l pl-4 py-2 flex w-70 justify-between items-center">
                  {itemName}
                  <Image
                    alt={itemName}
                    src={`https://www.poewiki.net/wiki/Special:${wishes["info"]["inventory_icon"]}`}
                    width={70}
                    height={70}
                  />
                </td>
                <td className="border-l border-r text-center">{wishes["total"]}</td>
                {/* <td className="border-l" data-tooltip-id={`tooltip-${itemName}`}>
                  <ItemInfoCell itemName={itemName} wishes={wishes} />
                  <div>Monsters: {JSON.stringify(wishes["info"]["drop_monsters"])}</div>
                  <div>Areas: {JSON.stringify(wishes["info"]["drop_areas"])}</div>
                  <div>Tags: {JSON.stringify(wishes["info"]["acquisition_tags"])}</div>
                </td> */}
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
