class Gif:
    def __init__(self, frames, frame_durations):
        self.frames = frames
        self.frame_durations = frame_durations
        self.current_frame = 0
        self.ticks_since_last_frame = 0

    def update(self, dt):
        self.ticks_since_last_frame += dt
        if self.ticks_since_last_frame > self.frame_durations[self.current_frame]:
            self.ticks_since_last_frame = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame]