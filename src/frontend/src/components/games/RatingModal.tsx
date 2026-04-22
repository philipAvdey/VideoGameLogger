import React, { useState } from "react";
import { Modal } from "../ui/Modal";
import { Input } from "../ui/Input";
import { StarRating } from "../ui/StarRating";

interface RatingModalProps {
  isOpen: boolean;
  onClose: () => void;
  gameTitle: string;
  onSubmit: (rating: number, dateCompleted: string) => void;
  initialRating?: number;
  initialDate?: string;
}

export const getFormattedDate = (dateString?: string) => {
  if (dateString) return dateString.split('T')[0];
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

export const RatingModal: React.FC<RatingModalProps> = ({
  isOpen,
  onClose,
  gameTitle,
  onSubmit,
  initialRating = 0,
  initialDate,
}) => {
  const [rating, setRating] = useState(initialRating);
  const [dateCompleted, setDateCompleted] = useState(() => getFormattedDate(initialDate));

  React.useEffect(() => {
    if (isOpen) {
      setRating(initialRating);
      setDateCompleted(getFormattedDate(initialDate));
    }
  }, [isOpen, initialRating, initialDate]);

  const handleSubmit = () => {
    onSubmit(rating, dateCompleted);
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Rate "${gameTitle}"`}
      onConfirm={handleSubmit}
      confirmText="Save to Diary"
    >
      <div className="space-y-8">
        <div className="flex flex-col items-center justify-center min-h-32">
          <StarRating rating={rating} onRatingChange={setRating} />
        </div>
        <div>
          <Input
            label="Date Completed"
            type="date"
            value={dateCompleted}
            onChange={setDateCompleted}
          />
        </div>
      </div>
    </Modal>
  );
};
