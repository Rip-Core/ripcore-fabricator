from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.game_state_util import GameState, CarState, Rotator, Physics, Vector3

from Snapshot.snap import Recorder
from play_moment.moment import Moment
import keyboard
import time


class MyBot(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.recorder = None
        self.moment = None
        self.stop_time = 30
        self.start_record = False
        self.buffer = []
        self.replay_start = False
        self.show_text = False
        self.snap_save = False
        self.replay_check = False
        self.is_ready_to_load = False
        self.isbotout = False

    def initialize_agent(self):
        self.recorder = Recorder()
        self.moment = Moment()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """
        if keyboard.is_pressed("/"):
            self.stop_time = 30
            self.start_record = True
            self.show_text = True

        if self.start_record:
            if self.stop_time == 0:
                self.start_record = False
                self.recorder.save()
                self.show_text = False
            else:
                print(self.stop_time)
                self.recorder.store(packet)
                self.stop_time -= 1
                time.sleep(1)

        if keyboard.is_pressed("*"):
            self.replay_start = True
            self.moment.init_count()
        if self.replay_start:
            self.is_ready_to_load = self.moment.load_packet()
            if self.is_ready_to_load:
                self.moment.get_state()
                self.set_game_state(self.moment.load_state())
            self.replay_start = False

        recording = "Recording: {}".format(self.stop_time)
        if self.show_text:
            self.debug(self.renderer, recording)

        controls = SimpleControllerState()
        controls.throttle = 1

        return controls

    def debug(self, renderer, text):
        renderer.begin_rendering()
        renderer.draw_string_2d(20, 500, 2, 2, text, renderer.white())
        renderer.end_rendering()
