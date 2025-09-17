from Utils.counters.exercise_counter import ExerciseCounter
from Utils.utils.utils import get_joint_coords, calculate_angle

class SquatCounter(ExerciseCounter):
    def __init__(self, min_angle=90):
        super().__init__("squat")
        self.min_angle = min_angle  # threshold for valid reps
        self.state = "up"           # "up" or "down"
        self.prev_angle = None
        self.last_up_angle = None
        self.deepest_angle = 0

    def update(self, landmarks):
        try:
            hip, knee, ankle = get_joint_coords(landmarks, "right_knee")
            angle = calculate_angle(hip, knee, ankle)
            anatomical_angle = 180 - angle  # 0 = standing, increases toward ~90 on squat

            # initialize prev_angle
            if self.prev_angle is None:
                self.prev_angle = anatomical_angle

            # ---------- UP -> DOWN : detect movement start ----------
            if self.state == "up":
                if anatomical_angle - self.prev_angle > 3:  # descent threshold
                    self.state = "down"
                    self.deepest_angle = anatomical_angle  # start tracking deepest point
                    self.last_up_angle = self.prev_angle

            # ---------- DOWN state ----------
            elif self.state == "down":
                # update deepest angle
                if anatomical_angle > self.deepest_angle:
                    self.deepest_angle = anatomical_angle

                # detect coming back up (return to approximately last up-angle)
                if anatomical_angle <= (self.last_up_angle + 6) and (self.prev_angle - anatomical_angle) > 3:
                    # Completed a rep
                    self.total_reps += 1

                    if self.deepest_angle >= self.min_angle:
                        self.valid_reps += 1
                        #print("valid rep — deepest angle:", self.deepest_angle)
                    else:
                        self.invalid_reps += 1
                        #print("invalid rep — deepest angle:", self.deepest_angle)

                    # reset
                    self.state = "up"
                    self.deepest_angle = 0
                    self.last_up_angle = None

            # update prev_angle
            self.prev_angle = anatomical_angle

        except Exception as e:
            # handle missing landmarks etc.
            # print("update error:", e)
            pass
