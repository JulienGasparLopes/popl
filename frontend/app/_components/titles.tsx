export const Title = ({ title }: { title: string }) => {
  return <h1 className="font-bold text-2xl">{title}</h1>;
};

export const SubTitle = ({ subtitle }: { subtitle: string }) => {
  return <h2 className="font-medium text-xl">{subtitle}</h2>;
};
