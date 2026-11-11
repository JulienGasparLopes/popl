"use client";

import Image from "next/image";
import { useState } from "react";
import { setItemsObtained } from "./setItemsObtained";

export const RequiredItem = ({
  buildId,
  name,
  itemKey,
  itemInfo,
  itemNameToInventoryIcon,
  updatable = false,
}: {
  buildId: string;
  name?: string;
  itemKey: string;
  itemInfo: ItemInfo | null;
  itemNameToInventoryIcon: { [id: string]: string };
  updatable?: boolean;
}) => {
  const [obtained, setObtained] = useState(itemInfo?.obtained);
  const color = obtained ? "text-green-500" : "text-red-500";
  const pointer = updatable ? "cursor-pointer" : "";

  return (
    <div className="flex gap-2 items-center">
      {name && <h3>{name}: </h3>}
      {itemInfo ? (
        <div
          className={`flex items-center gap-2 ${pointer}`}
          onClick={(event) => {
            if (!updatable) return;

            const key = itemKey.includes("jewels") ? "jewels" : itemKey;
            const data = itemKey.includes("jewels") ? { [itemKey.replace("jewels", "")]: !obtained } : !obtained;
            setItemsObtained(buildId, { [key]: data });
            setObtained(!obtained);
          }}
        >
          <Image
            alt={itemInfo.name}
            src={`https://www.poewiki.net/wiki/Special:${itemNameToInventoryIcon[itemInfo.name]}`}
            width={50}
            height={50}
          />
          <h3 className={`${color}`}>{itemInfo.name}</h3>
        </div>
      ) : (
        <h3>-</h3>
      )}
    </div>
  );
};
