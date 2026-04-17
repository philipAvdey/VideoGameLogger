import React from "react";
import { Button } from "../ui/Button";

interface HeaderProps {
  onLogout?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onLogout }) => {
  return (
    <header className="mb-8 pb-4 flex justify-between items-center">
      <h1 className="text-3xl font-bold">VideoGameLogger</h1>
      {onLogout && (
        <Button variant="ghost" onClick={onLogout}>
          Logout
        </Button>
      )}
    </header>
  );
};
