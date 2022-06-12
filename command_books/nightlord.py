"""A collection of all commands that Night lord can use to interact with the game. 	"""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command
from src.common.vkeys import press, key_down, key_up
from random import random


# List of key mappings
class Key:
    # Movement
    JUMP = 'space'
    FLASH_JUMP = 'space'
    SHADOW_LEAP = 'd'
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
    EXPLOSIVE_SHURIKEN = 'h'

    # Buffs Toggle
    MARK_OF_ASSASIN = 'f9'

    # Skills
    SHOWDOWN_CHALLENGE = 'c'
    DARK_FLARE = '5'
    FRAILTY_CURSE = '6'
    SECRET_SCROLL = '7'
    FUMA_SHURIKEN = 'b'
    SUDDEN_RAID = 'g'


#########################
#       Commands        #
#########################
def step(direction, target):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    """

    num_presses = 2
    if direction == 'up' or direction == 'down':
        num_presses = 1
    if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))
    d_y = target[1] - config.player_pos[1]
    if abs(d_y) > settings.move_tolerance * 1.5:
        if direction == 'down':
            press(Key.JUMP, 3)
        elif direction == 'up':
            press(Key.JUMP, 1)
    press(Key.FLASH_JUMP, num_presses)


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
                        NightLordShadowLeap().main()
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
        self.cd120_buff_time = 0
        self.cd180_buff_time = 0
        self.cd200_buff_time = 0
        self.cd240_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0

    def main(self):
        buffs = [Key.HOLY_SYMBOL]
        now = time.time()

        # if self.cd120_buff_time == 0 or now - self.cd120_buff_time > 120:
        #     press(Key.DIVINE_WRATH, 2)
        #     self.cd120_buff_time = now
        if self.cd180_buff_time == 0 or now - self.cd180_buff_time > 180:
            press(Key.EXPLOSIVE_SHURIKEN, 2)
            self.cd180_buff_time = now
        # if self.cd200_buff_time == 0 or now - self.cd200_buff_time > 200:
        #     press(Key.WEAVE_INFUSION, 2)
        #     press(Key.CONVERSION_OVERDRIVE, 2)
        #     self.cd200_buff_time = now
        # if self.cd240_buff_time == 0 or now - self.cd240_buff_time > 240:
        #     press(Key.GRANDIS_GODDESS, 2)
        #     self.cd240_buff_time = now
        # if self.cd900_buff_time == 0 or now - self.cd900_buff_time > 900:
        #     press(Key.HERO_OF_THE_FLORA, 2)
        #     self.cd900_buff_time = now
        if self.decent_buff_time == 0 or now - self.decent_buff_time > settings.buff_cooldown:
            for key in buffs:
                press(key, 3, up_time=0.3)
            self.decent_buff_time = now


class NightLordFlashJump(Command):
    """Performs a flash jump in the given direction."""

    def __init__(self, direction):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)

    def main(self):
        key_down(self.direction)
        time.sleep(0.1)
        press(Key.FLASH_JUMP, 1 if random() < 0.5 else 2)
        key_up(self.direction)
        time.sleep(0.5)


class NightLordShadowLeap(Command):
    """Performs a shadow leap upwards."""

    def main(self):
        press(Key.JUMP, 1)
        press(Key.SHADOW_LEAP, 1)

# Attacks


class NightLordShowdownChallenge(Command):
    """Attacks using 'ShowdownChallenge' in a given direction."""

    def __init__(self, direction, attacks=2, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.attacks = int(attacks)
        self.repetitions = int(repetitions)

    def main(self):
        time.sleep(0.05)
        key_down(self.direction)
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.SHOWDOWN_CHALLENGE, self.attacks, up_time=0.05)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)


class NightLordDarkFlare(Command):
    """Places 'DarkFlare' once."""

    def main(self):
        press(Key.DARK_FLARE, 2)


class NightLordFrailtyCurse(Command):
    """Places 'Frailty Curse' once."""

    def main(self):
        press(Key.FRAILTY_CURSE, 2)


class NightLordSecretScroll(Command):
    """Places 'Secret Scroll' once."""

    def main(self):
        press(Key.SECRET_SCROLL, 2)


class NightLordFumaShuriken(Command):
    """Uses 'Fuma Shuriken' once."""

    def main(self):
        press(Key.FUMA_SHURIKEN, 2, down_time=0.1)


class NightLordSuddenRaid(Command):
    """Uses 'Sudden raid' once"""

    def main(self):
        press(Key.SUDDEN_RAID, 2)
