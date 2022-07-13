import win32gui
from configparser import ConfigParser
from LooterManager import LooterManager
from ImageDetection import find_image
from MultiClients import MultiClients
from MageManager import MageManager
import multiprocessing
import psutil
import time
import cv2
import random
from PostMessage import pyPostMessage

user = 'Nass'
config = ConfigParser()
config.read('common_config.ini')

if user == 'Nass':
    config.read('config_nass.ini')
else:
    config.read('config_lec.ini')  # TODO
config.read(config.get(section='Login Credentials', option='path'))


def bot_farmer(ign, q):

    bot_mage_client = MageManager(config, ign)

    bot_mage_client.cast_mg()
    mg_time = time.time()
    next_mg = random.randint(450, 550)
    time.sleep(1.5)

    bot_mage_client.cast_infinity()
    inf_time = time.time()
    next_inf = random.randint(605, 650)
    time.sleep(0.5)

    while True:
        val = bot_mage_client.farm()
        if val:
            time.sleep(2.8)
            if time.time() > mg_time + next_mg:
                bot_mage_client.cast_mg()
                mg_time = time.time()
                time.sleep(1.5)

            elif time.time() > inf_time + next_inf:
                bot_mage_client.cast_infinity()
                inf_time = time.time()
                time.sleep(0.5)


def top_farmer(ign, q):

    top_mage_client = MageManager(config, ign=ign)

    top_mage_client.cast_mg()
    mg_time = time.time()
    next_mg = random.randint(450, 550)
    time.sleep(1.5)

    top_mage_client.cast_infinity()
    inf_time = time.time()
    next_inf = random.randint(605, 650)
    time.sleep(0.5)

    while True:
        if top_mage_client.reposition_needed():
            if 'ign' == 'Goldmine2':
                q.put(6)
            elif 'ign' == 'Goldmine3':
                q.put(7)
        val = top_mage_client.farm()
        if val:
            time.sleep(2.8)
            if time.time() > mg_time + next_mg:
                top_mage_client.cast_mg()
                mg_time = time.time()
                time.sleep(1.5)

            elif time.time() > inf_time + next_inf:
                top_mage_client.cast_infinity()
                inf_time = time.time()
                time.sleep(0.5)


def queue_reader(looter, top1, top2, bot1, bot2, q):

    looter_client = LooterManager(config, looter)
    looter_client.set_current_channel(11)

    top_mage_client1 = MageManager(config, top1)
    top_mage_client2 = MageManager(config, top2)

    bot_mage_client1 = MageManager(config, bot1)
    bot_mage_client1.set_current_channel(10)

    bot_mage_client2 = MageManager(config, bot2)
    channel_list = [10, 11]

    q.put(1)
    while True:
        i = q.get()
        if i == 1:
            looter_client.map_sequence_1()
            q.put(2)
        elif i == 2:
            looter_client.map_sequence_2()
            q.put(3)
        elif i == 3:
            looter_client.map_sequence_3()
            q.put(4)
        elif i == 4:
            looter_client.map_sequence_4()
            q.put(5)
        elif i == 5:
            looter_client.change_channel(channel_list[~channel_list.index(looter_client.get_current_channel())])
            if looter_client.get_current_channel() == bot_mage_client1.get_current_channel():
                q.put(8)
            q.put(1)
        elif i == 6:
            top_mage_client1.reposition()
        elif i == 7:
            top_mage_client2.reposition()
        elif i == 8:
            bot_mage_client1.cast_hs()
        if i == 'DONE':
            break


if __name__ == '__main__':
    test = LooterManager(config, 'Guarding')
    test.move_to_and_enter_door()
    test.move_from_door_to_fm()
    test.move_from_fm_to_door()
    # while True:
    #
    #     haystack = test.take_screenshot()
    #     char = test.find_self()
    #     portal = find_image(haystack, cv2.imread(test.config.get(section='Map Images', option='CBD_portal2'), cv2.IMREAD_COLOR), threshold=0.9)
    #     x1, y1, w1, h1 = list(*char)
    #     x2, y2, w2, h2 = list(*portal)
    #
    #     cv2.rectangle(haystack, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0))
    #     cv2.rectangle(haystack, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0))
    #     cv2.imshow('test', haystack)
    #     cv2.waitKey(1)
    #     print('Guarding mid-x point is at {}'.format(x1 + w1/2))
    #     print('Target mid-x point is at {}'.format(x2 + w2/2))


    # queue = multiprocessing.Queue()
    # proc1 = multiprocessing.Process(target=queue_reader, args=('Guarding', 'Goldmine2', 'Goldmine3', 'LegalizeIt', 'Goldmine1', queue,))
    # proc2 = multiprocessing.Process(target=bot_farmer, args=('Goldmine1', queue, ))
    # proc3 = multiprocessing.Process(target=top_farmer, args=('Goldmine2', queue, ))
    # proc4 = multiprocessing.Process(target=bot_farmer, args=('LegalizeIt', queue, ))
    # proc5 = multiprocessing.Process(target=top_farmer, args=('Goldmine3', queue, ))
    #
    # proc1.start()
    # proc2.start()
    # proc3.start()
    # proc4.start()
    # proc5.start()
    #
    # proc1.join()
    # proc2.join()
    # proc3.join()
    # proc4.join()
    # proc5.join()

    #
    # loop_time = time.time()
    # proc1 = multiprocessing.Process(target=top_farmer, args=(queue, ))
    # proc2 = multiprocessing.Process(target=bot_farmer, args=(queue, ))
    # proc3 = multiprocessing.Process(target=looter, args=(queue, ))
    # proc1.start()
    # proc2.start()
    # proc3.start()
    #
    # proc1.join()
    # proc2.join()
    # proc3.join()

    # Guarding.move_right_and_up_by(200)
    # Guarding.setup_hp_threshold()
    # Guarding.setup_mp_threshold()
    # Guarding.ensure_mount_is_used()
    # Guarding.map_sequence_1()
    # Guarding.map_sequence_2()
    # Guarding.map_sequence_3()
    # Guarding.map_sequence_4()
    # proc1 = multiprocessing.Process(target=loot)
    # proc2 = multiprocessing.Process(target=farm1)
    # proc3 = multiprocessing.Process(target=farm2)
    # proc1.start()
    # proc2.start()
    # proc3.start()