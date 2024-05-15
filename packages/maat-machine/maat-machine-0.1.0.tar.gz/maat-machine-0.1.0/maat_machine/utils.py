import sys

from tensorflow import config as tf_config

import maat_machine.pprint as mpprn

def print_system_info():
    print(f"Python version: {sys.version}")
    print(f"Version info: {sys.version_info}")
    print(f"Platform: {sys.platform}")


def display_system_info():
    mpprn.displayitwell(f"<hr>🐍 Python version:<br>&emsp;&emsp;&emsp;&emsp;{sys.version}", color='darkorange', font_weight='bold', inline=False)
    mpprn.displayitwell(f"🍃 Version info:<br>&emsp;&emsp;&emsp;&emsp;{sys.version_info}", color='darkblue', font_weight='bold', inline=False)
    mpprn.displayitwell(f"💻 Platform:<br>&emsp;&emsp;&emsp;&emsp;{sys.platform}<hr>", color='darkred', font_weight='bold', inline=False)


def print_gpu_info():
    print("⚙️ GPU Information:")
    devices = tf_config.list_physical_devices('GPU')
    if devices:
        print('\n'.join([f"\t✅ {tf_config.experimental.get_device_details(device).get('device_name', 'Unknown GPU')}" for device in devices]))
    else:
        print("\t🛑 No GPUs found.")


def display_gpu_info():
    mpprn.displayitwell("<hr>⚙️&nbsp;GPU Information:", color='darkgreen', font_weight='bold', inline=False)
    devices = tf_config.list_physical_devices('GPU')
    if devices:
        mpprn.displayitwell(
            '<ul style="margin-top: -0.8em">' \
            + '</li>'.join([f"<li style=\"list-style: none; padding-left: 1em;\">✅&nbsp;{tf_config.experimental.get_device_details(device).get('device_name', 'Unknown GPU')}" for device in devices]) \
            + '</ul><hr>'
        )
    else:
        mpprn.displayitwell("&emsp;&emsp;&emsp;&emsp;🛑&nbsp;No GPUs found.<hr>")


def print_environment_info():
    print_system_info()
    print_gpu_info()


def display_environment_info():
    display_system_info()
    display_gpu_info()