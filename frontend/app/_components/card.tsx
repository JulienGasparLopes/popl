import { SubTitle } from "./titles";

export const Card = ({ title, children }: { title: string; children: React.ReactNode }) => {
  return (
    <div className="border border-gray-400 rounded-md p-4 flex flex-col gap-4">
      <SubTitle subtitle={title} />
      <div>{children}</div>
    </div>
  );
};
