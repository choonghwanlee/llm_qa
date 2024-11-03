// components/ProgressBar.tsx

import React, { useEffect, useState } from "react";

interface ProgressBarProps {
  completed: number;
  total: number;
  isOpen: boolean;
  onClose: () => void; // Function to close the progress bar
}

const ProgressBar: React.FC<ProgressBarProps> = ({
  completed,
  total,
  isOpen,
  onClose,
}) => {
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    // Check if progress is complete and show the success message
    if (completed === total && total > 0) {
      setShowSuccess(true);
      // Hide progress bar after 2 seconds
      const timer = setTimeout(() => {
        setShowSuccess(false);
        onClose(); // Close the progress bar
      }, 2000);
      return () => clearTimeout(timer); // Clean up the timer
    }
  }, [completed, total, onClose]);

  if (!isOpen) return null; // Don't render if not open

  const progressPercentage = (completed / total) * 100;

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      <div className="bg-black p-4 rounded shadow-lg">
        {showSuccess ? (
          <h2 className="text-lg font-semibold text-white">
            Success! Please refresh the page
          </h2>
        ) : (
          <>
            <h2 className="text-lg font-semibold text-white">
              Running Tests...
            </h2>
            <div className="w-full bg-gray-800 rounded h-4 mt-2">
              <div
                className="bg-blue-600 h-full rounded"
                style={{ width: `${progressPercentage}%` }}
              />
            </div>
            <p className="mt-2 text-center text-white">
              {completed} / {total}
            </p>
          </>
        )}
      </div>
    </div>
  );
};

export default ProgressBar;
