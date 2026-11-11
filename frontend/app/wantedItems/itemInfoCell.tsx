"use client";

import { Tooltip } from "react-tooltip";

export const ItemInfoCell = ({ itemName, wishes }: { itemName: string; wishes: object }) => {
  return (
    <div>
      <Tooltip id={`tooltip-${itemName}`}>
        <div
          className="max-w-xl"
          dangerouslySetInnerHTML={{
            __html: `<div>Info: ${JSON.stringify(wishes["info"]["drop_text"]).replaceAll('\\"', '"')}</div>`,
          }}
        ></div>
      </Tooltip>
    </div>
  );
};
