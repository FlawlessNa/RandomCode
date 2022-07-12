import win32api
import win32con
import time

# http://www.kbdedit.com/manual/low_level_vk_list.html
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes

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

    return repeat_count + (scan_code << 16) + (extended_key << 24) + (context_code << 29) + (previous_key_state << 30) + (transition_state << 31)
    # return int(format(transition_state, '01b') + format(previous_key_state, '01b') + format(context_code, '01b') + format(0, '04b') + \
    #        format(extended_key, '01b') + format(scan_code, '08b') + format(repeat_count, '016b'), base=2)


def pyPostMessage(action, key_config=None, hwnd=None, repeat_count=1, previous_key_state=1, scan_code=None, duration=None, coordinates=None):
    # actions are pre-determined
    # key_config is simply the appropriate key retrieved from configs

    if action == 'press':
        key, extended_param = key_config
        lparam_keydown = construct_lparams(
            repeat_count=repeat_count, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0, scan_code=scan_code)
        lparam_keyup = construct_lparams(
            repeat_count=repeat_count, key=key, wm_command=win32con.WM_KEYUP, extended_key=extended_param, previous_key_state=previous_key_state, scan_code=scan_code)

        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, lparam_keydown)
        time.sleep(0.05)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, lparam_keyup)

    elif action == 'mousemove':  # TODO: figure out the problem here
        x, y = coordinates
        lparam = (x << 16) + y  # shifts the x-coordinate by 16 bytes
        win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, lparam)

    elif action == 'hold':
        key, extended_param = key_config
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
        key, extended_param = key_config
        lparam_char = construct_lparams(repeat_count=repeat_count, key=key, wm_command=win32con.WM_KEYDOWN, extended_key=extended_param, previous_key_state=0)
        win32api.PostMessage(hwnd, win32con.WM_CHAR, key, lparam_char)

    elif action == 'click':  # TODO: figure out the problem here
        x, y = coordinates
        lparam = int((y << 16) + x, base=2)  # shifts the y-coordinate by 16 bytes
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, lparam)

    else:
        pass

    time.sleep(0.05)