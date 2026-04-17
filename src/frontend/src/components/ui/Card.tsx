import React from "react";

interface CardProps {
  children: React.ReactNode;
  onClick?: () => void;
  interactive?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  onClick,
  interactive = false,
}) => {
  return (
    <div
      className={`subtle-border rounded-lg p-4 smooth-transition ${
        interactive ? "hover:shadow-md cursor-pointer" : ""
      }`}
      onClick={onClick}
    >
      {children}
    </div>
  );
};
