import React, { useState } from 'react';
import { AuthPage } from './pages/AuthPage';
import { HomePage } from './pages/HomePage';
import './styles/globals.css';

export const App: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <>
      {isAuthenticated ? (
        <HomePage onLogout={() => setIsAuthenticated(false)} />
      ) : (
        <AuthPage onAuthenticate={() => setIsAuthenticated(true)} />
      )}
    </>
  );
};

export default App;
