import React, { useState } from "react";
import { Input } from "../ui/Input";
import { Button } from "../ui/Button";

interface SignupFormProps {
  onSubmit: (username: string, password: string) => void;
  onToggleLogin: () => void;
}

export const SignupForm: React.FC<SignupFormProps> = ({
  onSubmit,
  onToggleLogin,
}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setPasswordError("Passwords do not match");
      return;
    }

    setPasswordError("");
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

      <Input
        label="Confirm Password"
        type="password"
        placeholder="••••••••"
        value={confirmPassword}
        onChange={setConfirmPassword}
      />

      {passwordError && (
        <div className="rounded-md bg-red-100 border border-red-400 text-red-700 px-4 py-2 text-sm">
          {passwordError}
        </div>
      )}

      <Button variant="primary" type="submit" size="lg">
        Create Account
      </Button>

      <p className="text-center text-gray-600">
        Already have an account?{" "}
        <button
          type="button"
          onClick={onToggleLogin}
          className="font-semibold text-black hover:underline"
        >
          Login
        </button>
      </p>
    </form>
  );
};