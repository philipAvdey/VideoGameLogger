import React from "react";

interface InputProps {
  placeholder?: string;
  onChange?: (value: string) => void;
  value?: string;
  type?: string;
  label?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({
  placeholder,
  onChange,
  value,
  type = "text",
  label,
  error,
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium mb-2">{label}</label>
      )}
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        className="w-full px-4 py-2 border subtle-border rounded-lg smooth-transition focus:outline-none focus:ring-2 focus:ring-black"
      />
      {error && <p className="text-red-600 text-sm mt-1">{error}</p>}
    </div>
  );
};
