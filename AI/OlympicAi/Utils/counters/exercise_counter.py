from abc import ABC, abstractmethod

class ExerciseCounter(ABC):
    def __init__(self, name: str):
        self.name = name
        self.total_reps = 0
        self.valid_reps = 0
        self.invalid_reps = 0

    @abstractmethod
    def update(self, landmarks):
        """Update counter state using landmarks from the current frame"""
        pass

    def get_results(self):
        """Return summary as dict"""
        return {
            "exercise": self.name,
            "total_reps": self.total_reps,
            "valid_reps": self.valid_reps,
            "invalid_reps": self.invalid_reps,
        }


