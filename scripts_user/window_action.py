

def put_in_center(window_name, window_width=440, window_height=480) -> None:
    """
    Putting created window in the center of screen
    :param window_name: the name of a new window
    :param window_width: the width of a new window
    :param window_height: the height of a new window
    :return: None
    """
    window_name.resizable(False, False)
    screen_width = window_name.winfo_screenwidth()
    screen_height = window_name.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    window_name.geometry(f'{window_width}x{window_height}+{x_cordinate}+{y_cordinate}')