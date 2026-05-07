import React, { useState } from "react";
import { Input } from "../ui/Input";
import { Button } from "../ui/Button";

interface LoginFormProps {
  onSubmit: (username: string, password: string) => void;
  onToggleSignup: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({
  onSubmit,
  onToggleSignup,
}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(username, password);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Username"
        type="text"
        placeholder="Enter username"
        value={username}
        onChange={setUsername}
      />
      <Input
        label="Password"
        type="password"
        placeholder="••••••••"
        value={password}
        onChange={setPassword}
      />
      <Button variant="primary" type="submit" size="lg">
        Login
      </Button>
      <p className="text-center text-gray-600">
        Don't have an account?{" "}
        <button
          type="button"
          onClick={onToggleSignup}
          className="font-semibold text-black hover:underline"
        >
          Sign up
        </button>
      </p>
    </form>
  );
};