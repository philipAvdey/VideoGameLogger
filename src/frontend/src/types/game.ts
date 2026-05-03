interface Game {
  ratingId: string;
  username: string;
  title: string;
  rating: number;
  dateCompleted: string;
  releaseDate: string;
  coverArt: string
}

interface SearchResult {
  id: number;
  title: string;
  releaseDate: string;
  coverArt: string;
  ratingCount: number;
}

export type { Game, SearchResult };