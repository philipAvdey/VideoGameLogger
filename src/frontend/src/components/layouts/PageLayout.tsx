import React from 'react';

interface PageLayoutProps {
  children: React.ReactNode;
}

export const PageLayout: React.FC<PageLayoutProps> = ({ children }) => {
  return <div className="max-w-4xl mx-auto px-6 py-8">{children}</div>;
};
