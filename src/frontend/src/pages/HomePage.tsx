import React, { useState } from "react";
import { PageLayout } from "../components/layouts/PageLayout";
import { Header } from "../components/common/Header";
import { SearchBar } from "../components/search/SearchBar";
import { GameList } from "../components/games/GameList";
import { RatingModal } from "../components/games/RatingModal";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import type { Game, SearchResult } from "../types/game";

interface HomePageProps {
  onLogout: () => void;
}

export const HomePage: React.FC<HomePageProps> = ({ onLogout }) => {
  const [games, setGames] = useState<Game[]>([
    {
      id: "1",
      title: "The Legend of Zelda: Breath of the Wild",
      coverArt: "https://via.placeholder.com/150x220?text=Zelda",
      releaseDate: "2017-03-03",
      rating: 5,
      dateCompleted: "2025-12-01",
    },
    {
      id: "2",
      title: "Elden Ring",
      coverArt: "https://via.placeholder.com/150x220?text=Elden+Ring",
      releaseDate: "2022-02-25",
      rating: 4,
      dateCompleted: "2025-11-15",
    },
  ]);

  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [selectedGame, setSelectedGame] = useState<SearchResult | null>(null);
  const [editingGame, setEditingGame] = useState<Game | null>(null);

  const handleSearch = (query: string) => {
    if (query.length > 0) {
      // Mock search results - would call API in real implementation
      setSearchResults([
        {
          id: "3",
          title: `${query} - Result 1`,
          releaseDate: "2024-01-01",
          coverArt: "https://via.placeholder.com/150x220?text=Game+1",
        },
        {
          id: "4",
          title: `${query} - Result 2`,
          releaseDate: "2023-06-15",
          coverArt: "https://via.placeholder.com/150x220?text=Game+2",
        },
      ]);
    } else {
      setSearchResults([]);
    }
  };

  const handleGameSelect = (game: SearchResult) => {
    setSelectedGame(game);
    setShowRatingModal(true);
  };

  const handleRatingSubmit = (rating: number, dateCompleted: string) => {
    if (editingGame) {
      // Update existing game
      setGames(
        games.map((g) =>
          g.id === editingGame.id ? { ...g, rating, dateCompleted } : g,
        ),
      );
      setEditingGame(null);
    } else if (selectedGame) {
      // Add new game
      const newGame: Game = {
        ...selectedGame,
        rating,
        dateCompleted,
      };
      setGames([newGame, ...games]);
      setSearchResults([]);
    }
  };

  const handleEditGame = (game: Game) => {
    setEditingGame(game);
    setShowRatingModal(true);
  };

  const sortedGames = [...games].sort(
    (a, b) =>
      new Date(b.dateCompleted).getTime() - new Date(a.dateCompleted).getTime(),
  );

  return (
    <PageLayout>
      <Header onLogout={onLogout} />
      <SearchBar onSearch={handleSearch} />

      {searchResults.length > 0 && (
        <div className="mb-8 pb-8">
          <h2 className="text-2xl font-semibold mb-6">Search Results</h2>
          <div className="space-y-4">
            {searchResults.map((game) => (
              <Card
                key={game.id}
                interactive
                onClick={() => handleGameSelect(game)}
              >
                <div className="flex gap-4">
                  <img
                    src={game.coverArt}
                    alt={game.title}
                    className="w-20 h-28 object-cover rounded-md"
                  />
                  <div className="flex-1 flex justify-between items-center">
                    <div>
                      <h3 className="font-semibold text-lg mb-2 text-white">
                        {game.title}
                      </h3>
                      <p className="text-gray-400 text-sm">
                        Released: {new Date(game.releaseDate).getFullYear()}
                      </p>
                    </div>
                    <Button
                      variant="primary"
                      onClick={() => handleGameSelect(game)}
                    >
                      Add to Diary
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      <GameList games={sortedGames} onGameClick={handleEditGame} />

      <RatingModal
        isOpen={showRatingModal}
        onClose={() => {
          setShowRatingModal(false);
          setSelectedGame(null);
          setEditingGame(null);
        }}
        gameTitle={editingGame?.title || selectedGame?.title || ""}
        onSubmit={handleRatingSubmit}
        initialRating={editingGame?.rating}
        initialDate={editingGame?.dateCompleted}
      />
    </PageLayout>
  );
};
