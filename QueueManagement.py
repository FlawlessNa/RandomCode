from LooterManager import LooterManager
from MageManager import MageManager
import multiprocessing
import time
import random
from varname import nameof
import cv2
from ImageDetection import find_image

class QueueManager:

    INITIALIZATION = 0
    MAP_SEQUENCE_1 = 1
    MAP_SEQUENCE_2 = 2
    MAP_SEQUENCE_3 = 3
    MAP_SEQUENCE_4 = 4
    CHANGING_CHANNELS = 5
    AFTER_CC = 6
    MOVE_TO_DOOR = 7
    FROM_DOOR_TO_FM = 8
    SETUP_TO_SELL = 9
    SELL_EQUIP_ITEM = 10
    SELL_ETC_ITEM = 11
    FROM_FM_TO_DOOR = 12
    REPOSITION_FIRST = 13
    REPOSITION_SECOND = 14
    NEED_DOOR = 15
    SET_CHANNELS_1 = 16
    SET_CHANNELS_2 = 17
    MOVE_FOR_ANTIBOT_BS = 18
    MOVE_FOR_ANTIBOT_BOT_MAGE = 19


    def __init__(self, config):
        self.config = config
        self.channels = multiprocessing.Array('i', [0, 0])
        # Initialize a constant passed between processes
        self.shared_num = multiprocessing.Value('i', self.INITIALIZATION)
        self.q = multiprocessing.Queue()

    def update_value(self):
        pass

    def looter(self, ign='Guarding'):

        looter = LooterManager(self.config, ign)
        looter.ensure_mount_is_used()
        time.sleep(1.75)
        looter.toggle_mount()
        time.sleep(1.75)
        looter.use_stance()
        time.sleep(1.75)
        looter.toggle_mount()
        time.sleep(1.75)
        curr_pet_food_time = time.time()
        curr_mount_food_time = time.time()
        next_pet_food = looter.feed_multiple_pets(3)
        self.q.put(self.INITIALIZATION)

        next_mount_food = looter.feed_mount()
        time.sleep(2)  # leaves time for all others to set up properly
        step = 0
        prev_step = 0
        nbr_sold = 0

        while True:

            if time.time() > curr_pet_food_time + next_pet_food:
                curr_pet_food_time = time.time()
                next_pet_food = looter.feed_multiple_pets(3)

            elif time.time() > curr_mount_food_time + next_mount_food and looter.check_is_mounted():
                curr_mount_food_time = time.time()
                next_mount_food = looter.feed_mount()

            if step not in [self.REPOSITION_FIRST, self.REPOSITION_SECOND, self.NEED_DOOR]:
                prev_step = step

            step = self.q.get()

            if step == self.INITIALIZATION:
                print('step executing: {}'.format(nameof(self.INITIALIZATION)))
                self.shared_num.value = self.SET_CHANNELS_1
                while self.shared_num.value == self.SET_CHANNELS_1:
                    pass

                while self.shared_num.value == self.SET_CHANNELS_2:
                    pass

                print('channel list completed: {}'.format(self.channels[:]))
                self.q.put(self.MAP_SEQUENCE_1)

            elif step == self.MAP_SEQUENCE_1:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_1)))
                looter.map_sequence_1()
                self.q.put(self.MAP_SEQUENCE_2)

            elif step == self.MAP_SEQUENCE_2:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_2)))
                looter.map_sequence_2()
                self.q.put(self.MAP_SEQUENCE_3)

            elif step == self.MAP_SEQUENCE_3:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_3)))
                looter.map_sequence_3()
                self.q.put(self.MAP_SEQUENCE_4)

            elif step == self.MAP_SEQUENCE_4:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_4)))
                looter.map_sequence_4()
                self.q.put(self.CHANGING_CHANNELS)

            elif step == self.CHANGING_CHANNELS:
                print('step executing: {}'.format(nameof(self.CHANGING_CHANNELS)))
                channels = list(self.channels)
                looter.change_channel(channels[~channels.index(looter.get_current_channel())])
                self.q.put(self.AFTER_CC)

            elif step == self.AFTER_CC:
                print('step executing: {}'.format(nameof(self.AFTER_CC)))
                if looter.after_channel_change():
                    if looter.get_current_channel() == self.channels[0]:
                        self.q.put(self.NEED_DOOR)
                    else:
                        self.q.put(self.MAP_SEQUENCE_1)
                else:
                    self.q.put(self.MAP_SEQUENCE_1)

            elif step == self.MOVE_TO_DOOR:
                print('step executing: {}'.format(nameof(self.MOVE_TO_DOOR)))
                looter.move_to_and_enter_door()
                self.q.put(self.FROM_DOOR_TO_FM)

            elif step == self.FROM_DOOR_TO_FM:
                print('step executing: {}'.format(nameof(self.FROM_DOOR_TO_FM)))
                looter.move_from_door_to_fm()
                self.q.put(self.SETUP_TO_SELL)

            elif step == self.SETUP_TO_SELL:
                print('step executing: {}'.format(nameof(self.SETUP_TO_SELL)))
                looter.setup_for_sell_equip_items()
                self.q.put(self.SELL_EQUIP_ITEM)

            elif step == self.SELL_EQUIP_ITEM:
                nbr_sold = looter.sell_equip_items(nbr_sold)
                print('step executing: {} -- number of items sold: {}'.format(nameof(self.SELL_EQUIP_ITEM), nbr_sold))
                if nbr_sold < 90:
                    self.q.put(self.SELL_EQUIP_ITEM)
                else:
                    nbr_sold = 0
                    self.q.put(self.SELL_ETC_ITEM)

            elif step == self.SELL_ETC_ITEM:
                print('step executing: {}'.format(nameof(self.SELL_ETC_ITEM)))
                looter.sell_etc_items()
                self.q.put(self.FROM_FM_TO_DOOR)

            elif step == self.FROM_FM_TO_DOOR:
                print('step executing: {}'.format(nameof(self.FROM_FM_TO_DOOR)))
                looter.move_from_fm_to_door()
                self.q.put(self.AFTER_CC)

            elif step == self.REPOSITION_FIRST:
                print('step executing: {}'.format(nameof(self.REPOSITION_FIRST)))
                self.shared_num.value = self.REPOSITION_FIRST
                while self.shared_num.value == self.REPOSITION_FIRST:
                    pass

            elif step == self.REPOSITION_SECOND:
                print('step executing: {}'.format(nameof(self.REPOSITION_SECOND)))
                self.shared_num.value = self.REPOSITION_SECOND
                while self.shared_num.value == self.REPOSITION_SECOND:
                    pass

            elif step == self.NEED_DOOR:
                print('step executing: {}'.format(nameof(self.NEED_DOOR)))
                self.shared_num.value = self.NEED_DOOR
                while self.shared_num.value == self.NEED_DOOR:
                    pass
                self.q.put(self.MOVE_TO_DOOR)

            elif step == self.MOVE_FOR_ANTIBOT_BS:
                print('step executing: {}'.format(nameof(self.MOVE_FOR_ANTIBOT_BS)))
                self.shared_num.value = self.MOVE_FOR_ANTIBOT_BS
                while self.shared_num.value == self.MOVE_FOR_ANTIBOT_BS:
                    pass

            elif step == self.MOVE_FOR_ANTIBOT_BOT_MAGE:
                print('step executing: {}'.format(nameof(self.MOVE_FOR_ANTIBOT_BOT_MAGE)))
                self.shared_num.value = self.MOVE_FOR_ANTIBOT_BOT_MAGE
                while self.shared_num.value == self.MOVE_FOR_ANTIBOT_BOT_MAGE:
                    pass


    def bishop(self, ign='LegalizeIt'):

        bs = MageManager(self.config, ign)
        curr_mg_time = time.time()
        curr_inf_time = time.time()
        curr_pet_food_time = time.time()
        antibot_timer = time.time()

        next_pet_food = bs.feed_pet()
        next_mg = bs.cast_mg()
        time.sleep(1.5)
        next_inf = bs.cast_infinity()

        next_move = random.randint(450, 550)
        last_added_to_queue = time.time()

        while True:

            if self.shared_num.value == self.SET_CHANNELS_1:
                self.channels[0] = bs.get_current_channel()
                self.shared_num.value = self.SET_CHANNELS_2

            if self.shared_num.value == self.NEED_DOOR:
                bs.cast_door()
                time.sleep(0.5)
                self.shared_num.value = 0

            if self.shared_num.value == self.MOVE_FOR_ANTIBOT_BS:
                bs.move_right_for(0.1)
                bs.move_left_for(0.1)
                antibot_timer = time.time()
                self.shared_num.value = 0

            ult_cast = bs.farm()
            if ult_cast:
                # When ult is cast, we want program to sleep for 2.8 seconds. However, we can still use this time to feed pet
                now = time.time()
                while time.time() - now < 2.8:
                    if time.time() > curr_pet_food_time + next_pet_food:
                        curr_pet_food_time = time.time()
                        next_pet_food = bs.feed_pet()

            if time.time() > curr_mg_time + next_mg:
                curr_mg_time = time.time()
                next_mg = bs.cast_mg()
                time.sleep(1.5)
            elif time.time() > curr_inf_time + next_inf:
                curr_inf_time = time.time()
                next_inf = bs.cast_infinity()
                time.sleep(0.5)
            elif time.time() > antibot_timer + next_move and time.time() - last_added_to_queue > 60:
                self.q.put(self.MOVE_FOR_ANTIBOT_BS)
                last_added_to_queue = time.time()

    def bot_mage(self, ign):

        bot_mage = MageManager(self.config, ign)
        curr_mg_time = time.time()
        curr_inf_time = time.time()
        curr_pet_food_time = time.time()

        next_pet_food = bot_mage.feed_pet()
        next_mg = bot_mage.cast_mg()
        time.sleep(1.5)
        next_inf = bot_mage.cast_infinity()

        antibot_timer = time.time()
        next_move = random.randint(450, 550)
        last_added_to_queue = time.time()

        while True:

            if self.shared_num.value == self.SET_CHANNELS_2:
                self.channels[1] = bot_mage.get_current_channel()
                self.shared_num.value = 0

            if self.shared_num.value == self.MOVE_FOR_ANTIBOT_BOT_MAGE:
                bot_mage.move_right_for(0.1)
                bot_mage.move_left_for(0.1)
                antibot_timer = time.time()
                self.shared_num.value = 0

            ult_cast = bot_mage.farm()
            if ult_cast:
                # When ult is cast, we want program to sleep for 2.8 seconds. However, we can still use this time to feed pet
                now = time.time()
                while time.time() - now < 2.8:
                    if time.time() > curr_pet_food_time + next_pet_food:
                        curr_pet_food_time = time.time()
                        next_pet_food = bot_mage.feed_pet()

            if time.time() > curr_mg_time + next_mg:
                curr_mg_time = time.time()
                next_mg = bot_mage.cast_mg()
                time.sleep(1.5)
            elif time.time() > curr_inf_time + next_inf:
                curr_inf_time = time.time()
                next_inf = bot_mage.cast_infinity()
                time.sleep(0.5)

            elif time.time() > antibot_timer + next_move and time.time() - last_added_to_queue > 60:
                self.q.put(self.MOVE_FOR_ANTIBOT_BOT_MAGE)
                last_added_to_queue = time.time()

    def top_mage(self, ign, nbr):

        top_mage = MageManager(self.config, ign)
        curr_mg_time = time.time()
        curr_inf_time = time.time()
        curr_pet_food_time = time.time()

        next_pet_food = top_mage.feed_pet()
        next_mg = top_mage.cast_mg()
        time.sleep(1.5)
        next_inf = top_mage.cast_infinity()

        reposition_timer = time.time()

        while True:

            if nbr == 1:

                if top_mage.reposition_needed() and time.time() - reposition_timer > 10:
                    reposition_timer = time.time()
                    self.q.put(self.REPOSITION_FIRST)

                if self.shared_num.value == self.REPOSITION_FIRST:
                    top_mage.reposition()
                    self.shared_num.value = 0

            elif nbr == 2:
                if top_mage.reposition_needed() and time.time() - reposition_timer > 10:
                    reposition_timer = time.time()
                    self.q.put(self.REPOSITION_SECOND)

                if self.shared_num.value == self.REPOSITION_SECOND:
                    top_mage.reposition()
                    self.shared_num.value = 0

            ult_cast = top_mage.farm()
            if ult_cast:
                # When ult is cast, we want program to sleep for 2.8 seconds. However, we can still use this time to feed pet
                now = time.time()
                while time.time() - now < 2.8:
                    if time.time() > curr_pet_food_time + next_pet_food:
                        curr_pet_food_time = time.time()
                        next_pet_food = top_mage.feed_pet()

            if time.time() > curr_mg_time + next_mg:
                curr_mg_time = time.time()
                next_mg = top_mage.cast_mg()
                time.sleep(1.5)
            elif time.time() > curr_inf_time + next_inf:
                curr_inf_time = time.time()
                next_inf = top_mage.cast_infinity()
                time.sleep(0.5)

