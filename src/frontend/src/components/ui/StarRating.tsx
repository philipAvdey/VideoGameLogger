import React, { useState } from "react";

interface StarRatingProps {
  rating: number;
  onRatingChange: (rating: number) => void;
}

export const StarRating: React.FC<StarRatingProps> = ({
  rating,
  onRatingChange,
}) => {
  const [hoverRating, setHoverRating] = useState(0);

  return (
    <div className="flex gap-3 justify-center">
      {[1, 2, 3, 4, 5].map((star) => {
        const isSelected = star <= (hoverRating || rating);
        return (
          <button
            key={star}
            type="button"
            onClick={() => onRatingChange(star)}
            onMouseEnter={() => setHoverRating(star)}
            onMouseLeave={() => setHoverRating(0)}
            style={{
              appearance: "none",
              WebkitAppearance: "none",
              backgroundColor: "transparent",
              border: "none",
              padding: 0,
              margin: 0,
              cursor: "pointer",
            }}
          >
            <span className="text-4xl smooth-transition text-black">
              {isSelected ? "★" : "☆"}
            </span>
          </button>
        );
      })}
    </div>
  );
};
