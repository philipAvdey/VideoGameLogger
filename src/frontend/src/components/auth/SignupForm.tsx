import React, { useState } from "react";
import { Input } from "../ui/Input";
import { Button } from "../ui/Button";

interface SignupFormProps {
  onSubmit: (email: string, password: string, name: string) => void;
  onToggleLogin: () => void;
}

export const SignupForm: React.FC<SignupFormProps> = ({
  onSubmit,
  onToggleLogin,
}) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password === confirmPassword) {
      onSubmit(email, password, name);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Full Name"
        placeholder="John Doe"
        value={name}
        onChange={setName}
      />
      <Input
        label="Email"
        type="email"
        placeholder="you@example.com"
        value={email}
        onChange={setEmail}
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
