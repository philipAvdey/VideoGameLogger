import React, { useState } from "react";
import { PageLayout } from "../components/layouts/PageLayout";
import { LoginForm } from "../components/auth/LoginForm";
import { SignupForm } from "../components/auth/SignupForm";
import { Card } from "../components/ui/Card";

interface AuthPageProps {
  onAuthenticate: () => void;
}

export const AuthPage: React.FC<AuthPageProps> = ({ onAuthenticate }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState("");

  const backendBaseUrl = "http://localhost:5000";

  const handleLogin = async (username: string, password: string) => {
    try {
      setError("");

      const response = await fetch(`${backendBaseUrl}/api/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Login failed");
        return;
      }

      localStorage.setItem("user_id", data.user_id);
      localStorage.setItem("username", data.username);

      onAuthenticate();
    } catch (error) {
      console.error("Login error:", error);
      setError("Could not connect to backend");
    }
  };

  const handleSignup = async (username: string, password: string) => {
    try {
      setError("");

      const response = await fetch(`${backendBaseUrl}/api/create_account`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Create account failed");
        return;
      }

      localStorage.setItem("user_id", data.user_id);
      localStorage.setItem("username", data.username);

      onAuthenticate();
    } catch (error) {
      console.error("Create account error:", error);
      setError("Could not connect to backend");
    }
  };

  return (
    <PageLayout>
      <div className="flex items-center justify-center min-h-screen">
        <div className="w-full max-w-md">
          <h1 className="text-4xl font-bold text-center mb-2">
            VideoGameLogger
          </h1>
          <p className="text-center text-gray-600 mb-8">
            Track and rate the games you love
          </p>

          <Card>
            {error && (
              <div className="mb-4 rounded-md bg-red-100 border border-red-400 text-red-700 px-4 py-2 text-sm">
                {error}
              </div>
            )}

            {isLogin ? (
              <LoginForm
                onSubmit={handleLogin}
                onToggleSignup={() => {
                  setError("");
                  setIsLogin(false);
                }}
              />
            ) : (
              <SignupForm
                onSubmit={handleSignup}
                onToggleLogin={() => {
                  setError("");
                  setIsLogin(true);
                }}
              />
            )}
          </Card>
        </div>
      </div>
    </PageLayout>
  );
};