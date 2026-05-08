import React, { useEffect, useState } from "react";
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
  const [games, setGames] = useState<Game[]>([]);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [selectedGame, setSelectedGame] = useState<SearchResult | null>(null);
  const [editingGame, setEditingGame] = useState<Game | null>(null);

  const user_id = localStorage.getItem("user_id");
  // const username = localStorage.getItem("username");

  const loadRatedGames = async () => {
    try {
      const response = await fetch(
        `/api/ratings?user_id=${user_id}`,
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to load ratings");
      }

      setGames(data.userRatings || []);
    } catch (error) {
      console.error("Load ratings error:", error);
    }
  };

  useEffect(() => {
    loadRatedGames();
  }, []);

  const handleSearch = async (query: string) => {
    if (query.length > 0) {
      try {
        const response = await fetch(
          `/api/igdb/search?query=${encodeURIComponent(query)}`,
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to search games");
        }
        const games = Array.isArray(data.games) ? data.games : [];
        setSearchResults(
          games.sort(
            (a: SearchResult, b: SearchResult) =>
              (b.ratingCount || 0) - (a.ratingCount || 0),
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

  const handleRatingSubmit = async (rating: number, dateCompleted: string) => {
    try {
      if (editingGame) {
        const response = await fetch(
          `/api/ratings/${editingGame.ratingId}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              user_id: user_id,
              rating: rating,
              dateCompleted: dateCompleted,
            }),
          },
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to update rating");
        }

        setEditingGame(null);
      } else if (selectedGame) {
        const response = await fetch(`/api/ratings`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: user_id,
            title: selectedGame.title,
            rating: rating,
            releaseDate: selectedGame.releaseDate,
            coverArt: selectedGame.coverArt,
            dateCompleted: dateCompleted,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to add rating");
        }

        setSelectedGame(null);
        setSearchResults([]);
      }

      await loadRatedGames();
      setShowRatingModal(false);
    } catch (error) {
      console.error("Rating submit error:", error);
    }
  };

  const handleEditGame = (game: Game) => {
    setEditingGame(game);
    setShowRatingModal(true);
  };

  const handleDeleteGame = async (game: Game) => {
    if (!window.confirm(`Delete "${game.title}" from your diary?`)) {
      return;
    }

    try {
      const response = await fetch(
        `/api/ratings/${game.ratingId}?user_id=${user_id}`,
        {
          method: "DELETE",
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to delete rating");
      }

      await loadRatedGames();
    } catch (error) {
      console.error("Delete error:", error);
    }
  };

  const sortedGames = [...games].sort((a, b) => {
    // Sort by dateCompleted in descending order (most recent first)
    return b.dateCompleted.localeCompare(a.dateCompleted);
  });

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

      <GameList
        games={sortedGames}
        onGameClick={handleEditGame}
        onGameDelete={handleDeleteGame}
      />

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
