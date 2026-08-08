"use client";

import { useState } from "react";
import { updateUserMechanics } from "./updateUserMechanics";

const VALUES = ["primary", "secondary", "none"];

export const DefaultMechanicsColumn = ({ userId, mechanicsNames }: { userId: string; mechanicsNames: string[] }) => {
  const onUpdateMechanic = (mechanic_name: string) => {
    updateUserMechanics(userId, { [mechanic_name]: "primary" });
  };

  return (
    <div className="flex flex-col border-l">
      <div className="px-2">{userId}</div>
      {mechanicsNames.map((name) => (
        <div key={name} onClick={() => onUpdateMechanic(name)} className="p-2">
          none
        </div>
      ))}
    </div>
  );
};

export const UserMechanicsColumn = ({ userId, mechanicsMapping }: { userId: string; mechanicsMapping: object }) => {
  const onUpdateMechanic = (mechanic_name: string, newValue: string) => {
    updateUserMechanics(userId, { [mechanic_name]: newValue });
  };

  return (
    <div className="flex flex-col border-l">
      <div className="px-2">{userId}</div>
      {Object.entries(mechanicsMapping).map(([name, value]) => {
        return <MechanicCell key={name} name={name} value={value} onUpdateMechanic={onUpdateMechanic} />;
      })}
    </div>
  );
};

type onUpdateMechanicFunc = (name: string, newValue: string) => void;

const MechanicCell = ({
  name,
  value,
  onUpdateMechanic,
}: {
  name: string;
  value: string;
  onUpdateMechanic: onUpdateMechanicFunc;
}) => {
  const [currentValue, setCurrentValue] = useState(value);

  const color = currentValue === "primary" ? "bg-green-200" : currentValue === "secondary" ? "bg-orange-200" : "";

  return (
    <div
      key={name}
      onClick={() => {
        const newValue = VALUES[(VALUES.findIndex((e) => e === currentValue) + 1) % 3];
        setCurrentValue(newValue);
        onUpdateMechanic(name, newValue);
      }}
      className={`${color} px-2`}
    >
      {currentValue}
    </div>
  );
};
