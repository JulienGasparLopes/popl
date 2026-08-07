"use client";

import { useState } from "react";
import { setItemsObtained } from "./set_items_obtained";

export const RequiredItem = ({
  buildId,
  name,
  itemKey,
  itemInfo,
}: {
  buildId: string;
  name?: string;
  itemKey: string;
  itemInfo: { name: string; obtained: boolean } | null;
}) => {
  const [obtained, setObtained] = useState(itemInfo?.obtained);
  const color = obtained ? "text-green-500" : "text-red-500";
  return (
    <div className="flex gap-2">
      {name && <h3>{name}: </h3>}
      {itemInfo ? (
        <h3
          className={color}
          onClick={(event) => {
            setItemsObtained(buildId, { [itemKey]: !obtained });
            setObtained(!obtained);
          }}
        >
          {itemInfo.name}
        </h3>
      ) : (
        <h3>-</h3>
      )}
    </div>
  );
};
