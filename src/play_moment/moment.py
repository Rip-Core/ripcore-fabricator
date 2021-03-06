from rlbot.utils.game_state_util import GameState, BallState, CarState, GameInfoState
import pickle
import configparser


class Moment:
    def __init__(self):
        self.packet = []
        self.num_cars = None
        self.starting_time = None
        self.starting_state = None
        self.game_state = None
        self.car_state = None
        self.ball_state = None
        self.game_info_state = None
        self.snap_count = 4
        self.car_index = None
        self.set_playback_time = 10
        self.snap_end_time = None

    def init_count(self):
        try:
            config = configparser.ConfigParser()
            config.read("src/config.ini")
            self.snap_count = int(config['SETTINGS']['set_custom_snap'])
            self.set_playback_time = int(config['SETTINGS']['playback_time'])
        except Exception as e:
            print(e)

    def load_packet(self) -> bool:
        try:
            with open("src/Snapshot/dumper/snapshot#{}.pickle".format(self.snap_count), "rb") as fp:
                self.packet = pickle.load(fp)
            self.num_cars = self.packet[len(self.packet) - 1].num_cars
            self.snap_end_time = self.packet[0].game_info.seconds_elapsed
            self.starting_time = self.snap_end_time + self.set_playback_time
            if self.snap_end_time:
                for key, buffer in enumerate(self.packet):
                    if round(buffer.game_info.seconds_elapsed) == round(self.starting_time):
                        self.starting_state = buffer
                return True
            return False
        except Exception as e:
            print(e)

    def get_state(self):
        try:
            self.game_state = GameState.create_from_gametickpacket(
                self.starting_state)
            self.car_state = self.game_state.cars[0].__dict__
            self.ball_state = self.game_state.ball.__dict__
            self.game_info_state = self.game_state.game_info
        except Exception as e:
            print(e)

    def load_state(self) -> GameState:
        try:
            car_state = CarState(
                physics=self.car_state["physics"], boost_amount=self.car_state["boost_amount"])
            ball_state = BallState(physics=self.ball_state["physics"])
            game_info_state = GameInfoState(self.game_info_state)

            game_state = GameState(ball=ball_state, cars={
                0: car_state}, game_info=game_info_state)

            with open(f"src/Snapshot/training_pack/test#{self.snap_count}.pack", "wb") as gs:
                pickle.dump(game_state, gs)
            return game_state
        except Exception as e:
            print(e)
