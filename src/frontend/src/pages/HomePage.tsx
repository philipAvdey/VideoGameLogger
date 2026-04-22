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
  // TODO: will probably need to fetch from user's existing data or something?
  const [games, setGames] = useState<Game[]>([]);

  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [selectedGame, setSelectedGame] = useState<SearchResult | null>(null);
  const [editingGame, setEditingGame] = useState<Game | null>(null);

  // TODO: fix
  const backendBaseUrl = "http://localhost:5000";

  const handleSearch = async (query: string) => {
    if (query.length > 0) {
      try {
        const response = await fetch(
          `${backendBaseUrl}/api/igdb/search?query=${encodeURIComponent(query)}`,
        );
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || "Failed to search games");
        }
        const games = data.games as SearchResult[];
        games.map((g) => g.coverArt);
        setSearchResults(
          (games || []).sort(
            (a, b) => (b.ratingCount || 0) - (a.ratingCount || 0),
          ),
        );
      } catch (error) {
        console.error("Search error:", error);
        setSearchResults([]);
      }
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

  const sortedGames = [...games].sort((a, b) =>
    b.dateCompleted.localeCompare(a.dateCompleted),
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
                    className="w-20 h-28 rounded-md object-cover"
                  />
                  <div className="flex-1 flex justify-between items-center">
                    <div>
                      <h3 className="font-semibold text-lg mb-2 text-black">
                        {game.title}
                      </h3>
                      <p className="text-gray-400 text-sm">
                        Released:{" "}
                        {game.releaseDate
                          ? game.releaseDate.split("-")[0]
                          : "N/A"}
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
