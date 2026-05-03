// BOOK DATA

export interface SimilarBook {
  slug: string;
  reason: string;
}

export interface PurchaseOption {
  format: string; // e.g., "eBook", "Paperback", "Hardcover", "Audio"
  price: string;
  url: string;
}

export interface Book {
  id: string;
  title: string;
  series: string;
  positionInSeries: number;
  releaseDate: string;
  coverImage: string;
  altText: string;
  miniBlurb: string;
  tagLine: string;
  blurb: string;
  isRecent: boolean;
  isFeatured: boolean;
  genre: string;
  subGenre: string[];
  tropes: string[];
  dynamics: string[];
  readerNotes: string[];
  isKU: boolean; 
  similarBooks: SimilarBook[];
  purchaseOptions: PurchaseOption[];
}

// READER MAGNET DATA

export interface Extra {
  parentBookId: string;
  type: string; 
  chronology: number;
  timelineContext: string;
  requirement: string;
  bookfunnelLink: string;
}

// TROPE DATA

export interface Trope {
  slug: string;
  name: string;
  description: string;
  featured: boolean;
  canonical: boolean;
}