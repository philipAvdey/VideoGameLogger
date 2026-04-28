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

  const handleAuth = () => {
    onAuthenticate()
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
            {isLogin ? (
              <LoginForm
                onSubmit={handleAuth}
                onToggleSignup={() => setIsLogin(false)}
              />
            ) : (
              <SignupForm
                onSubmit={handleAuth}
                onToggleLogin={() => setIsLogin(true)}
              />
            )}
          </Card>
        </div>
      </div>
    </PageLayout>
  );
};
