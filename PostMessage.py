import win32api
import win32con
import time


def construct_lparams(repeat_count, key, wm_command, extended_key, previous_key_state=1, scan_code=None):

    assert repeat_count < 2 ** 16

    if scan_code is None:
        scan_code = win32api.MapVirtualKey(key, 0)

    if wm_command == win32con.WM_KEYDOWN:
        context_code = 0
        transition_state = 0

    elif wm_command == win32con.WM_KEYUP:
        context_code = 0
        transition_state = 1

    elif wm_command == win32con.WM_SYSKEYDOWN:
        if key == win32con.VK_MENU:
            context_code = 1
        else:
            context_code = 0
        transition_state = 0

    elif wm_command == win32con.WM_SYSKEYUP:
        if key == win32con.VK_MENU:
            context_code = 1
        else:
            context_code = 0
        transition_state = 1

    else:
        pass

    return int(format(transition_state, '01b') + format(previous_key_state, '01b') + format(context_code, '01b') + format(0, '04b') + \
           format(extended_key, '01b') + format(scan_code, '08b') + format(repeat_count, '016b'), base=2)


def pyPostMessage(action, key_config, hwnd, repeat_count=1, previous_key_state=1, scan_code=None, duration=None):
    # actions are pre-determined
    # key_config is simply the appropriate key retrieved from configs

    key, extended_param = key_config

    if action == 'press':
        lparam_keydown = construct_lparams(
            repeat_count=repeat_count, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0, scan_code=scan_code)
        lparam_keyup = construct_lparams(
            repeat_count=repeat_count, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param, previous_key_state=previous_key_state, scan_code=scan_code)

        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        time.sleep(0.05)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    elif action == 'mousemove':
        pass

    elif action == 'hold':
        lparam_keydown_init = construct_lparams(
            repeat_count=repeat_count, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0, scan_code=scan_code)
        lparam_keydown = construct_lparams(
            repeat_count=repeat_count, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=1, scan_code=scan_code)
        lparam_keyup = construct_lparams(
            repeat_count=repeat_count, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param, previous_key_state=previous_key_state, scan_code=scan_code)

        now = time.time()
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, lparam_keydown_init)
        while time.time() - now < duration:
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
            time.sleep(0.05)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    elif action == 'write':

        lparam_char = construct_lparams(repeat_count=repeat_count, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        win32api.PostMessage(hwnd, win32con.WM_CHAR, key, lparam_char)

    elif action == 'click':
        pass

    else:
        pass

    time.sleep(0.05)