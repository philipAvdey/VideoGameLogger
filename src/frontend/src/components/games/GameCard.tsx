import React from "react";
import { Card } from "../ui/Card";
import type { Game } from "../../types/game";

interface GameCardProps {
  game: Game;
  onClick?: () => void;
}

export const GameCard: React.FC<GameCardProps> = ({ game, onClick }) => {
  const stars = "★".repeat(game.rating) + "☆".repeat(5 - game.rating);

  return (
    <Card interactive onClick={onClick}>
      <div className="flex gap-4">
        <img
          src={game.coverArt}
          alt={game.title}
          className="w-20 h-28 rounded-md object-cover"
        />
        <div className="flex-1">
          <h3 className="font-semibold text-lg mb-2">{game.title}</h3>
          <p className="text-gray-700 text-sm mb-3">
            Released: {new Date(game.releaseDate).getFullYear()}
          </p>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Rating</p>
              <p className="font-semibold text-lg">{stars}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Completed</p>
              <p className="font-semibold">
                {game.dateCompleted.split("-").slice(1).join("/")}/
                {game.dateCompleted.split("-")[0]}
              </p>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};
