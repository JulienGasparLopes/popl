"use client";

import { useState } from "react";
import { updateUserMechanics } from "./updateUserMechanics";

const VALUES = ["primary", "secondary", "none"];

export const DefaultMechanicsColumn = ({
  ownerId,
  ownerPseudo,
  mechanicsNames,
}: {
  ownerId: string;
  ownerPseudo: string;
  mechanicsNames: string[];
}) => {
  const onUpdateMechanic = (mechanic_name: string) => {
    updateUserMechanics(ownerId, { [mechanic_name]: "primary" });
  };

  return (
    <div className="flex flex-col border-l">
      <div className="px-2 border-b">{ownerPseudo}</div>
      {mechanicsNames.map((name) => (
        <MechanicCell key={name} name={name} value={"none"} onUpdateMechanic={onUpdateMechanic} updatable={true} />
      ))}
    </div>
  );
};

export const UserMechanicsColumn = ({
  ownerId,
  ownerPseudo,
  mechanicsMapping,
  updatable,
}: {
  ownerId: string;
  ownerPseudo: string;
  mechanicsMapping: object;
  updatable: boolean;
}) => {
  const onUpdateMechanic = (mechanic_name: string, newValue: string) => {
    updateUserMechanics(ownerId, { [mechanic_name]: newValue });
  };

  return (
    <div className="flex flex-col border-l">
      <div className="px-2 border-b">{ownerPseudo}</div>
      {Object.entries(mechanicsMapping).map(([name, value]) => {
        return (
          <MechanicCell
            key={name}
            name={name}
            value={value}
            onUpdateMechanic={onUpdateMechanic}
            updatable={updatable}
          />
        );
      })}
    </div>
  );
};

type onUpdateMechanicFunc = (name: string, newValue: string) => void;

const MechanicCell = ({
  name,
  value,
  onUpdateMechanic,
  updatable,
}: {
  name: string;
  value: string;
  onUpdateMechanic: onUpdateMechanicFunc;
  updatable: boolean;
}) => {
  const [currentValue, setCurrentValue] = useState(value);

  const color = currentValue === "primary" ? "bg-green-200" : currentValue === "secondary" ? "bg-orange-200" : "";
  const pointer = updatable ? "cursor-pointer" : "";

  return (
    <div
      key={name}
      onClick={() => {
        if (!updatable) return;

        const newValue = VALUES[(VALUES.findIndex((e) => e === currentValue) + 1) % 3];
        setCurrentValue(newValue);
        onUpdateMechanic(name, newValue);
      }}
      className={`${color} ${pointer} px-2`}
    >
      {currentValue}
    </div>
  );
};
