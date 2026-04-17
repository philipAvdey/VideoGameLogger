import React, { useState } from 'react';
import { Input } from '../ui/Input';

interface SearchBarProps {
  onSearch?: (query: string) => void;
  placeholder?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  placeholder = 'Search games...',
}) => {
  const [query, setQuery] = useState('');

  const handleChange = (value: string) => {
    setQuery(value);
    onSearch?.(value);
  };

  return (
    <div className="w-full mb-8">
      <Input
        placeholder={placeholder}
        value={query}
        onChange={handleChange}
      />
    </div>
  );
};
