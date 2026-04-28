interface Game {
  ratingId: string;
  username: string;
  title: string;
  rating: number;
}

interface SearchResult {
  id: string;
  title: string;
  releaseDate: string;
  coverArt: string;
  ratingCount: number;
}

export type { Game, SearchResult };