import React from "react";
import { Card } from "../ui/Card";
import type { Game } from "../../types/game";

interface GameCardProps {
  game: Game;
  onClick?: () => void;
  onDelete?: (game: Game) => void;
}

export const GameCard: React.FC<GameCardProps> = ({
  game,
  onClick,
  onDelete,
}) => {
  const stars = "★".repeat(game.rating) + "☆".repeat(5 - game.rating);

  return (
    <Card interactive onClick={onClick}>
      <div className="flex gap-4">
        {game.coverArt ? (
          <img
            src={game.coverArt}
            alt={game.title}
            className="w-20 h-28 rounded-md object-cover"
          />
        ) : (
          <div className="w-20 h-28 rounded-md bg-gray-200 flex items-center justify-center text-xs text-gray-500">
            No Cover
          </div>
        )}

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
            <div className="text-right">
              {onDelete && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(game);
                  }}
                  className="mb-2 px-4 py-1 text-sm text-white bg-black hover:bg-gray-800 rounded transition flex items-center justify-center"
                >
                  Delete
                </button>
              )}
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
