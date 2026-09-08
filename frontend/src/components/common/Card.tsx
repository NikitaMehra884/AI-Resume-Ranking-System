import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ children, className = '', onClick }) => {
  return (
    <div
      onClick={onClick}
      className={`bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm ${onClick ? 'cursor-pointer hover:border-slate-700 transition' : ''} ${className}`}
    >
      {children}
    </div>
  );
};

export default Card;
