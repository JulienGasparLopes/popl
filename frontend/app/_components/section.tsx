import { Title } from "./titles";

export const Section = ({ name, children }: { name: string; children: React.ReactNode }) => {
  return (
    <div className="flex flex-col gap-4">
      <Title title={name} />
      <div>{children}</div>
    </div>
  );
};
