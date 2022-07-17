from LooterManager import LooterManager
from MageManager import MageManager
import multiprocessing
import time
import random
from varname import nameof
import numpy as np

class QueueManager:

    INITIALIZATION = 0
    MAP_SEQUENCE_1 = 1
    MAP_SEQUENCE_2 = 2
    NEED_HS = 3
    MAP_SEQUENCE_3 = 4
    MAP_SEQUENCE_4 = 5
    MAP_SEQUENCE_5 = 6
    MAP_SEQUENCE_6 = 7
    MAP_SEQUENCE_7 = 8
    MAP_SEQUENCE_8 = 9
    MAP_SEQUENCE_9 = 10
    MAP_SEQUENCE_10 = 11
    MAP_SEQUENCE_11 = 12
    CHANGING_CHANNELS = 13
    AFTER_CC = 14
    MOVE_TO_DOOR = 15
    FROM_DOOR_TO_FM = 16
    SETUP_TO_SELL = 17
    SELL_EQUIP_ITEM = 18
    SELL_ETC_ITEM = 19
    FROM_FM_TO_DOOR = 20
    BACK_FROM_FM = 21
    REPOSITION_TOP_FIRST = 22
    REPOSITION_TOP_SECOND = 23
    REPOSITION_BOT_FIRST = 24
    REPOSITION_BOT_SECOND = 25
    NEED_DOOR = 26
    SET_CHANNELS_1 = 27
    SET_CHANNELS_2 = 28


    def __init__(self, config):
        self.config = config
        self.channels = multiprocessing.Array('i', [0, 0])
        # Initialize a constant passed between processes
        self.shared_num = multiprocessing.Value('i', self.INITIALIZATION)
        self.positioning_array = np.array([[self.REPOSITION_TOP_FIRST, self.REPOSITION_TOP_SECOND],
                                          [self.REPOSITION_BOT_FIRST, self.REPOSITION_BOT_SECOND]])
        self.positioning_dict = {'top': 0, 'bot': 1, 'first': 0, 'second': 1}
        self.q = multiprocessing.Queue()

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
        nbr_sold = 0

        while True:

            if time.time() > curr_pet_food_time + next_pet_food:
                curr_pet_food_time = time.time()
                next_pet_food = looter.feed_multiple_pets(3)

            elif time.time() > curr_mount_food_time + next_mount_food and looter.check_is_mounted():
                curr_mount_food_time = time.time()
                next_mount_food = looter.feed_mount()

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
                if looter.get_current_channel() == self.channels[0]:
                    self.q.put(self.NEED_HS)
                else:
                    self.q.put(self.MAP_SEQUENCE_3)

            elif step == self.NEED_HS:
                print('step executing: {}'.format(nameof(self.NEED_HS)))
                self.shared_num.value = self.NEED_HS
                while self.shared_num.value == self.NEED_HS:
                    pass
                self.q.put(self.MAP_SEQUENCE_3)

            elif step == self.MAP_SEQUENCE_3:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_3)))
                looter.map_sequence_3()
                self.q.put(self.MAP_SEQUENCE_4)

            elif step == self.MAP_SEQUENCE_4:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_4)))
                looter.map_sequence_4()
                self.q.put(self.MAP_SEQUENCE_5)

            elif step == self.MAP_SEQUENCE_5:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_5)))
                looter.map_sequence_5()
                self.q.put(self.MAP_SEQUENCE_6)

            elif step == self.MAP_SEQUENCE_6:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_6)))
                looter.map_sequence_6()
                self.q.put(self.MAP_SEQUENCE_7)

            elif step == self.MAP_SEQUENCE_7:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_7)))
                looter.map_sequence_7()
                self.q.put(self.MAP_SEQUENCE_8)

            elif step == self.MAP_SEQUENCE_8:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_8)))
                looter.map_sequence_8()
                self.q.put(self.MAP_SEQUENCE_9)

            elif step == self.MAP_SEQUENCE_9:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_9)))
                looter.map_sequence_9()
                self.q.put(self.MAP_SEQUENCE_10)

            elif step == self.MAP_SEQUENCE_10:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_10)))
                looter.map_sequence_10()
                self.q.put(self.MAP_SEQUENCE_11)

            elif step == self.MAP_SEQUENCE_11:
                print('step executing: {}'.format(nameof(self.MAP_SEQUENCE_11)))
                looter.map_sequence_11()
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
                self.q.put(self.BACK_FROM_FM)

            elif step == self.BACK_FROM_FM:
                print('step executing: {}'.format(nameof(self.BACK_FROM_FM)))
                self.q.put(self.NEED_HS)


            elif step == self.REPOSITION_TOP_FIRST:
                print('step executing: {}'.format(nameof(self.REPOSITION_TOP_FIRST)))
                self.shared_num.value = self.REPOSITION_TOP_FIRST
                while self.shared_num.value == self.REPOSITION_TOP_FIRST:
                    pass

            elif step == self.REPOSITION_TOP_SECOND:
                print('step executing: {}'.format(nameof(self.REPOSITION_TOP_SECOND)))
                self.shared_num.value = self.REPOSITION_TOP_SECOND
                while self.shared_num.value == self.REPOSITION_TOP_SECOND:
                    pass

            elif step == self.REPOSITION_BOT_FIRST:
                print('step executing: {}'.format(nameof(self.REPOSITION_BOT_FIRST)))
                self.shared_num.value = self.REPOSITION_BOT_FIRST
                while self.shared_num.value == self.REPOSITION_BOT_FIRST:
                    pass

            elif step == self.REPOSITION_BOT_SECOND:
                print('step executing: {}'.format(nameof(self.REPOSITION_BOT_SECOND)))
                self.shared_num.value = self.REPOSITION_BOT_SECOND
                while self.shared_num.value == self.REPOSITION_BOT_SECOND:
                    pass

            elif step == self.NEED_DOOR:
                print('step executing: {}'.format(nameof(self.NEED_DOOR)))
                self.shared_num.value = self.NEED_DOOR
                while self.shared_num.value == self.NEED_DOOR:
                    pass
                self.q.put(self.MOVE_TO_DOOR)

    def bishop(self, ign='LegalizeIt', pos='bot'):

        bs = MageManager(self.config, ign, pos)
        curr_mg_time = time.time()
        curr_inf_time = time.time()
        curr_pet_food_time = time.time()

        next_pet_food = bs.feed_pet()
        next_mg = bs.cast_mg()
        time.sleep(1.5)
        next_inf = bs.cast_infinity()

        reposition_timer = time.time()

        while True:

            if bs.reposition_needed() and time.time() - reposition_timer > 10:
                reposition_timer = time.time()
                self.q.put(self.REPOSITION_BOT_FIRST)


            if self.shared_num.value == self.SET_CHANNELS_1:
                self.channels[0] = bs.get_current_channel()
                self.shared_num.value = self.SET_CHANNELS_2

            elif self.shared_num.value == self.NEED_DOOR:
                bs.reposition()
                bs.cast_door()
                self.shared_num.value = 0
                time.sleep(0.5)

            elif self.shared_num.value == self.NEED_HS:
                bs.cast_hs()
                self.shared_num.value = 0
                time.sleep(1.5)

            elif self.shared_num.value == self.REPOSITION_BOT_FIRST:
                bs.reposition()
                self.shared_num.value = 0

            ult_cast = bs.farm()
            if ult_cast:
                # When ult is cast, we want program to sleep for 2.8 seconds. However, we can still use this time to feed pet
                now = time.time()
                while time.time() - now < 3:
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

    def mage(self, ign, position, nbr):

        mage = MageManager(self.config, ign, position)
        constant_to_use = self.positioning_array[self.positioning_dict[position], self.positioning_dict[nbr]]
        curr_mg_time = time.time()
        curr_inf_time = time.time()
        curr_pet_food_time = time.time()

        next_pet_food = mage.feed_pet()
        next_mg = mage.cast_mg()
        time.sleep(1.5)
        next_inf = mage.cast_infinity()

        reposition_timer = time.time()

        while True:

            if self.shared_num.value == self.SET_CHANNELS_2 and mage.position == 'bot' and nbr == 'second':
                self.channels[1] = mage.get_current_channel()
                self.shared_num.value = 0

            if mage.reposition_needed() and time.time() - reposition_timer > 10:
                reposition_timer = time.time()
                self.q.put(constant_to_use)

            if self.shared_num.value == constant_to_use:
                mage.reposition()
                self.shared_num.value = 0

            ult_cast = mage.farm()
            if ult_cast:
                # When ult is cast, we want program to sleep for 2.8 seconds. However, we can still use this time to feed pet
                now = time.time()
                while time.time() - now < 2.8:
                    if time.time() > curr_pet_food_time + next_pet_food:
                        curr_pet_food_time = time.time()
                        next_pet_food = mage.feed_pet()

            if time.time() > curr_mg_time + next_mg:
                curr_mg_time = time.time()
                next_mg = mage.cast_mg()
                time.sleep(1.5)
            elif time.time() > curr_inf_time + next_inf:
                curr_inf_time = time.time()
                next_inf = mage.cast_infinity()
                time.sleep(0.5)
