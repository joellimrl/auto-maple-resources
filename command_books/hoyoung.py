"""A collection of all commands that Ho young can use to interact with the game. 	"""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command, Fall
from src.common.vkeys import press, key_down, key_up


# List of key mappings
class Key:
    # Movement
    JUMP = 'space'
    FLASH_JUMP = 'space'
    NIMBUS = 'f2'
    # IMPALE = '1'
    # RESONANCE = '2'
    # PLUMMET = 'r'
    # FEATHER_FLOAT = 'f'
    # HIGH_RISE = 'ctrl'

    # Buffs
    # WEAVE_INFUSION = 'f1'
    # HERO_OF_THE_FLORA = 'f2'
    # SPEED_INFUSION = 'f3'
    HOLY_SYMBOL = 'f5'
    # SHARP_EYE = 'f5'
    # COMBAT_ORDERS = 'f6'
    # ADVANCED_BLESSING = 'f7'
    GRANDIS_GODDESS = 'l'
    EXTREME_IMMOLATION = 'j'
    ILLUSION_OF_HEH = 'h'
    TAEUL_DIVINE_MEDICINE = '7'
    CLONE_TALISMAN = 'r'  # Talisman magic
    GHOST_TALISMAN = 't'  # Talisman magic
    FIST_BUTTERFLIES = 'y'  # Scroll magic
    REBELLIOUS_POWER = 'page down'  # Map wipe

    # Buffs Toggle
    # MARK_OF_ASSASIN = 'f9'

    # Skills
    FAN_HUMAN = 'c'
    CHAIN_EARTH = 'x'
    CONFLAG_HEAVEN = 'v'
    CUDGEL_HUMAN = 'd'
    FACE_ROCK = 'f'
    BUCHAE_HEAVEN = 'g'
    ROCK_EARTH = 'f3'
    FIST_VORTEX = 'u'  # Scroll magic, Small summon
    MOUNTAIN_SPIRIT = 'page up'  # Scroll magic, Big summon


#########################
#       Commands        #
#########################
def step(direction, target):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    """

    # num_presses = 2
    # if direction == 'up' or direction == 'down':
    #     num_presses = 1
    # if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
    #     time.sleep(utils.rand_float(0.1, 0.3))
    # d_y = target[1] - config.player_pos[1]
    # if abs(d_y) > settings.move_tolerance * 1.5:
    #     if direction == 'down':
    #         press(Key.JUMP, 3)
    #     elif direction == 'up':
    #         HoYoungNimbus('up').main()
    # press(Key.FLASH_JUMP, num_presses)

    if direction == 'up':
        d_y = target[1] - config.player_pos[1]
        HoYoungNimbus(direction, abs(d_y) * 5).main()
    elif direction == 'down':
        Fall().main()
    else:
        # d_x = target[0] - config.player_pos[0]
        # HoYoungNimbus(direction, abs(d_x) * 5).main()
        HoYoungFlashJump(direction).main()


class Adjust(Command):
    """Fine-tunes player position using small movements."""

    def __init__(self, x, y, max_steps=5):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)

    def main(self):
        counter = self.max_steps
        toggle = True
        error = utils.distance(config.player_pos, self.target)
        while config.enabled and counter > 0 and error > settings.adjust_tolerance:
            if toggle:
                d_x = self.target[0] - config.player_pos[0]
                threshold = settings.adjust_tolerance / math.sqrt(2)
                if abs(d_x) > threshold:
                    walk_counter = 0
                    if d_x < 0:
                        key_down('left')
                        while config.enabled and d_x < -1 * threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('left')
                    else:
                        key_down('right')
                        while config.enabled and d_x > threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('right')
                    counter -= 1
            else:
                d_y = self.target[1] - config.player_pos[1]
                if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
                    if d_y < 0:
                        HoYoungNimbus('up').main()
                    else:
                        key_down('down')
                        time.sleep(0.05)
                        press(Key.JUMP, 3, down_time=0.1)
                        key_up('down')
                        time.sleep(0.05)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle


class Buff(Command):
    """Uses each of Night lord's buffs once."""

    def __init__(self):
        super().__init__(locals())
        self.cd25_buff_time = 0
        self.cd100_buff_time = 0
        self.cd180_buff_time = 0
        self.cd200_buff_time = 0
        self.cd240_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0
        self.rebellious_toggle = False

    def main(self):
        buffs = [Key.HOLY_SYMBOL]
        now = time.time()

        if self.cd25_buff_time == 0 or now - self.cd25_buff_time > 25:
            if (self.rebellious_toggle):
                press(Key.REBELLIOUS_POWER, 1)
                self.rebellious_toggle = False
        if self.cd100_buff_time == 0 or now - self.cd100_buff_time > 100:
            press(Key.ILLUSION_OF_HEH, 2)
            press(Key.TAEUL_DIVINE_MEDICINE, 2)
            time.sleep(1)
            press(Key.GHOST_TALISMAN, 2)
            press(Key.FIST_BUTTERFLIES, 2)
            self.cd100_buff_time = now
        # if self.cd180_buff_time == 0 or now - self.cd180_buff_time > 180:
        #     press(Key.EXPLOSIVE_SHURIKEN, 2)
        #     self.cd180_buff_time = now
        if self.cd200_buff_time == 0 or now - self.cd200_buff_time > 200:
            press(Key.EXTREME_IMMOLATION, 2)
            self.cd200_buff_time = now
        if self.cd240_buff_time == 0 or now - self.cd240_buff_time > 240:
            press(Key.GRANDIS_GODDESS, 2)
            press(Key.CLONE_TALISMAN, 2)
            if (not self.rebellious_toggle):
                press(Key.REBELLIOUS_POWER, 1)
                self.rebellious_toggle = True
            self.cd240_buff_time = now
        # if self.cd900_buff_time == 0 or now - self.cd900_buff_time > 900:
        #     press(Key.HERO_OF_THE_FLORA, 2)
        #     self.cd900_buff_time = now
        if self.decent_buff_time == 0 or now - self.decent_buff_time > settings.buff_cooldown:
            for key in buffs:
                press(key, 3, up_time=0.3)
            self.decent_buff_time = now


class HoYoungFlashJump(Command):
    """Performs a flash jump in the given direction."""

    def __init__(self, direction):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)

    def main(self):
        key_down(self.direction)
        time.sleep(0.1)
        press(Key.FLASH_JUMP, 2)
        key_up(self.direction)
        time.sleep(0.5)


class HoYoungNimbus(Command):
    """Holds nimbus to fly around"""

    def __init__(self, direction, duration=1.5):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)
        self.duration = float(duration)

    def main(self):
        press(Key.JUMP, 1)
        key_down(Key.NIMBUS)
        time.sleep(0.1)
        key_down(self.direction)
        time.sleep(self.duration)
        key_up(self.direction)
        time.sleep(0.1)
        key_up(Key.NIMBUS)
        time.sleep(0.5)

# Attacks


class HoYoungFanHuman(Command):
    """Attacks using 'Flying Fan:Human' in a given direction."""

    def __init__(self, direction, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.repetitions = int(repetitions)

    def main(self):
        time.sleep(0.05)
        key_down(self.direction)
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.FAN_HUMAN, 1, up_time=0.05)
        key_up(self.direction)
        time.sleep(0.2)


class HoYoungEarthChain(Command):
    """Attacks using 'Earth Chain:Earth' left or right."""

    def __init__(self, direction, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.repetitions = int(repetitions)

    def main(self):
        time.sleep(0.05)
        key_down(self.direction)
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.CHAIN_EARTH, 2, up_time=0.05)
        key_up(self.direction)
        time.sleep(0.2)


class HoYoungConflagHeaven(Command):
    """Attacks using 'Conflagration Chain:Heaven' upwards."""

    def __init__(self, followWithFaceRock=False, repetitions=1):
        super().__init__(locals())
        self.followUp = followWithFaceRock
        self.repetitions = int(repetitions)

    def main(self):
        time.sleep(0.05)
        press(Key.JUMP, 1)
        key_down('up')
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.CONFLAG_HEAVEN, 2, up_time=0.05)
        key_up('up')
        time.sleep(0.2)
        if (self.followUp):
            HoYoungFaceRock().main()


class HoYoungFaceRock(Command):
    """Attacks using 'Transform:Face Rock' downwards."""

    def main(self):
        press(Key.FACE_ROCK, 1, up_time=0.05)
        time.sleep(0.2)


class HoYoungCudgelHuman(Command):
    """Attacks using 'Gold Cudgel:Human' in a given direction."""

    def __init__(self, direction, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.repetitions = int(repetitions)

    def main(self):
        time.sleep(0.05)
        key_down(self.direction)
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.CUDGEL_HUMAN, 1, up_time=0.05)
        key_up(self.direction)
        time.sleep(0.2)


class HoYoungBuchaeHeaven(Command):
    """Attacks using 'Buchae Chain:Heaven' in a given direction."""

    def __init__(self, direction, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.repetitions = int(repetitions)

    def main(self):
        time.sleep(0.05)
        key_down(self.direction)
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.BUCHAE_HEAVEN, 2, up_time=0.05)
        key_up(self.direction)
        time.sleep(0.2)


class HoYoungRockEarth(Command):
    """Attacks using 'Rock Chain:Earth' in a given direction."""

    def __init__(self, direction, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.repetitions = int(repetitions)

    def main(self):
        time.sleep(0.05)
        key_down(self.direction)
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.ROCK_EARTH, 2, up_time=0.05)
        key_up(self.direction)
        time.sleep(0.2)


class HoYoungFistVortex(Command):
    """Places 'Fist: Inhaling Vortex' once."""

    def main(self):
        press(Key.FIST_VORTEX, 1)


class HoYoungMountainSpirit(Command):
    """Places 'Mountain Spirit Summoning' once."""

    def main(self):
        press(Key.MOUNTAIN_SPIRIT, 1)
