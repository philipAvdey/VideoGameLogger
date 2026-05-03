import React from "react";
import { GameCard } from "./GameCard";
import type { Game } from "../../types/game";

interface GameListProps {
  games: Game[];
  onGameClick?: (game: Game) => void;
  onGameDelete?: (game: Game) => void;
}

export const GameList: React.FC<GameListProps> = ({ games, onGameClick, onGameDelete }) => {
  if (games.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 text-lg">
          No games yet. Search and add one to get started!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold mb-6">Your Game Diary</h2>
      {games.map((game) => (
        <GameCard
          key={game.ratingId}
          game={game}
          onClick={() => onGameClick?.(game)}
          onDelete={onGameDelete}
        />
      ))}
    </div>
  );
};
