from Utils.counters.exercise_counter import ExerciseCounter
from Utils.utils.utils import get_joint_coords, calculate_angle

class SquatCounter(ExerciseCounter):
    def __init__(self, min_angle=90):
        super().__init__("squat")
        self.min_angle = min_angle
        self.state = "up"   # up or down

    def update(self, landmarks):
        try:
            hip, knee, ankle = get_joint_coords(landmarks, "right_knee")
            angle = calculate_angle(hip, knee, ankle)
            anatomical_angle = 180 - angle  # adjust to anatomical

            if self.state == "up" and anatomical_angle <= self.min_angle:
                self.state = "down"
                self.lowest_angle = anatomical_angle

            elif self.state == "down" and anatomical_angle > self.min_angle:
                # Completed one rep
                self.total_reps += 1
                if self.lowest_angle <= self.min_angle:
                    self.valid_reps += 1
                else:
                    self.invalid_reps += 1
                self.state = "up"
                print("lowest angle:", self.lowest_angle)

        except Exception:
            pass
