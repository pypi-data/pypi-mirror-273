from types import NoneType
from typing import Union

from IPython.display import display
from IPython.display import HTML


def displayit(value: str):
    """
    Displays the given HTML value using IPython's display function.

    Parameters:
        value (str): The HTML value to be displayed.

    Returns:
        None
    """
    display(HTML(value))


def displayitwell(value: str, color: str = 'black',
                  font_style: str = 'normal', font_weight: str = 'normal', text_decoration: Union[str, NoneType] = None,
                  font_size: str = '1em', font_family='default', inline: bool = True):
    """
    A function that displays the 'value' with specified styling options.

    Parameters:
        value (str): The content to be displayed.
        color (str): The color of the text (default is 'black').
        font_style (str): The style of the font (default is 'normal').
        font_weight (str): The weight of the font (default is 'normal').
        text_decoration (Union[str, NoneType]): The text decoration style (default is None).
        font_size (str): The size of the font (default is '1em').
        font_family (str): The font family (default is 'default').
        inline (bool): Whether to display the content inline or in a block (default is True).
    """
    tag = 'span' if inline else 'div'
    text_decoration_value = f" text-decoration: {text_decoration};" if text_decoration is not None else ''
    displayit(f"<{tag} style='color: {color}; font-style: {font_style}; font-weight: {font_weight};{text_decoration_value} font-size: {font_size}; font-family: {font_family if font_family != 'default' else ''}'>{value}</{tag}>")


def dict_to_html(dictionary):
    """
    Converts a dictionary into an HTML-formatted string.

    Parameters:
        dictionary (dict): The dictionary to be converted to HTML.

    Returns:
        str: The HTML-formatted string representing the dictionary.
    """
    html_output = '<div>{<br>\n'
    for key, value in dictionary.items():
        html_output += f"&nbsp;&nbsp;{key}: {value}<br>\n"
    html_output += '}</div>'
    return html_output