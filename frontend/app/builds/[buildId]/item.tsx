"use client";

import { useState } from "react";
import { setItemsObtained } from "./setItemsObtained";

export const RequiredItem = ({
  buildId,
  name,
  itemKey,
  itemInfo,
  updatable = false,
}: {
  buildId: string;
  name?: string;
  itemKey: string;
  itemInfo: ItemInfo | null;
  updatable?: boolean;
}) => {
  const [obtained, setObtained] = useState(itemInfo?.obtained);
  const color = obtained ? "text-green-500" : "text-red-500";
  const pointer = updatable ? "cursor-pointer" : "";

  return (
    <div className="flex gap-2">
      {name && <h3>{name}: </h3>}
      {itemInfo ? (
        <h3
          className={`${color} ${pointer}`}
          onClick={(event) => {
            if (!updatable) return;

            const key = itemKey.includes("jewels") ? "jewels" : itemKey;
            const data = itemKey.includes("jewels") ? { [itemKey.replace("jewels", "")]: !obtained } : !obtained;
            setItemsObtained(buildId, { [key]: data });
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
