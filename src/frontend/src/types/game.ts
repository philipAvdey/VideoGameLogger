interface Game {
  id: string;
  title: string;
  coverArt: string;
  releaseDate: string;
  rating: number; // 1-10
  dateCompleted: string;
  notes?: string;
}

interface SearchResult {
  id: string;
  title: string;
  releaseDate: string;
  coverArt: string;
  ratingCount: number;
}

export type { Game, SearchResult }
