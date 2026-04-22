import React, { useState } from "react";
import { Input } from "../ui/Input";
import { Button } from "../ui/Button";

interface SearchBarProps {
  onSearch?: (query: string) => void;
  placeholder?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  placeholder = "Search games...",
}) => {
  const [query, setQuery] = useState("");

  const handleChange = (value: string) => {
    setQuery(value);
  };

  const handleSearch = () => {
    if (query.trim()) {
      onSearch?.(query.trim());
    }
  };

  return (
    <div className="w-full mb-8">
      <div className="flex gap-2">
        <div className="flex-1">
          <Input
            placeholder={placeholder}
            value={query}
            onChange={handleChange}
          />
        </div>
        <Button onClick={handleSearch} size="md">
          Search
        </Button>
      </div>
    </div>
  );
};
