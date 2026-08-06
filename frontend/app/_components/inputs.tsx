export const Button = ({ title }: { title: string }) => {
  return (
    <button type="submit" className="outline-1 -outline-offset-1 outline-gray-600 border rounded-sm px-2 mt-4">
      {title}
    </button>
  );
};
