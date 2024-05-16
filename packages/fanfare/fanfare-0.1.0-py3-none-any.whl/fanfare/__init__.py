import re

def interpolate_color(start_color, end_color, factor):
    """Calculate the color at the given 'factor' between 'start_color' and 'end_color'."""
    r = int(start_color[0] + (end_color[0] - start_color[0]) * factor)
    g = int(start_color[1] + (end_color[1] - start_color[1]) * factor)
    b = int(start_color[2] + (end_color[2] - start_color[2]) * factor)
    return r, g, b

def generate_gradient(colors, n_steps):
    """Generate a list of colors forming a gradient between the given colors over 'n_steps'."""
    gradient = []
    # Determine how many steps to place between each pair of colors
    steps_per_color = n_steps // (len(colors) - 1)
    
    for i in range(len(colors) - 1):
        start_color = colors[i]
        end_color = colors[i + 1]
        for step in range(steps_per_color):
            factor = step / steps_per_color
            gradient.append(interpolate_color(start_color, end_color, factor))
    gradient.append(colors[-1])  # Ensure the last color is included
    return gradient


# ANSI escape codes for styles
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

def hex_to_ansi(hex_color, background=False):
    # Assuming the terminal supports 24-bit color
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))  # Convert hex to RGB
    base = 48 if background else 38  # ANSI code for background (48) or foreground (38)
    return f"\033[{base};2;{rgb[0]};{rgb[1]};{rgb[2]}m"

def hex_to_rgb(hex_color):
    """Convert a HEX color to an RGB tuple."""
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def apply(text):
    # Regex patterns for different styles
    color_pattern = r"\[c (#[0-9A-Fa-f]{6})\](.*?)\[/c\]"
    bg_color_pattern = r"\[bg (#[0-9A-Fa-f]{6})\](.*?)\[/bg\]"
    bold_pattern = r"\[b\](.*?)\[/b\]"
    underline_pattern = r"\[u\](.*?)\[/u\]"
    gradient_pattern = r"\[g (#[0-9A-Fa-f]{6}(?:,#[0-9A-Fa-f]{6})+)\](.*?)\[/g\]"

    def replace_color(match):
        color_code = hex_to_ansi(match.group(1))
        return f"{color_code}{match.group(2)}{RESET}"

    def replace_bg_color(match):
        color_code = hex_to_ansi(match.group(1), background=True)
        return f"{color_code}{match.group(2)}{RESET}"

    def replace_bold(match):
        return f"{BOLD}{match.group(1)}{RESET}"

    def replace_underline(match):
        return f"{UNDERLINE}{match.group(1)}{RESET}"

    def replace_gradient(match):
        hex_colors = match.group(1).split(',')
        rgb_colors = [hex_to_rgb(hex_color) for hex_color in hex_colors]
        content = match.group(2)
        gradient = generate_gradient(rgb_colors, len(content))
        
        # Apply the gradient to each character
        colored_text = ''
        for i, char in enumerate(content):
            color_code = f"\033[38;2;{gradient[i][0]};{gradient[i][1]};{gradient[i][2]}m"
            colored_text += color_code + char
        colored_text += RESET  # Reset after the styled text
        return colored_text

    # Apply styles
    text = re.sub(color_pattern, replace_color, text)
    text = re.sub(bg_color_pattern, replace_bg_color, text)
    text = re.sub(bold_pattern, replace_bold, text)
    text = re.sub(underline_pattern, replace_underline, text)
    text = re.sub(gradient_pattern, replace_gradient, text)
    return text





import sys

class ProgressBar:
    def __init__(self, total_slots=10, total_steps=100, positive_shape='█', negative_shape='░', positive_colors=None, negative_colors=None):
        self.total_slots = total_slots
        self.total_steps = total_steps
        self.positive_shape = positive_shape
        self.negative_shape = negative_shape
        self.positive_colors = positive_colors if positive_colors else []
        self.negative_colors = negative_colors if negative_colors else []
        self.current_step = 0
        self.start_message = ''
        self.end_message = ''

    def set_progress(self, step):
        self.current_step = step
        self.draw()

    def draw(self):
        slots_filled = int((self.current_step / self.total_steps) * self.total_slots)
        slots_empty = self.total_slots - slots_filled

        # Calculate gradient colors for filled and unfilled slots if applicable
        filled_bar = self.apply_gradient(self.positive_shape, self.positive_colors, slots_filled)
        empty_bar = self.apply_gradient(self.negative_shape, self.negative_colors, slots_empty)

        # Combine parts and print progress bar
        progress_bar = f"{self.start_message} {filled_bar}{empty_bar} "
        if self.current_step >= self.total_steps:
            progress_bar += self.end_message
        sys.stdout.write(f'\r{progress_bar}')
        sys.stdout.flush()

    def apply_gradient(self, shape, colors, count):
        if not colors or len(colors) == 1:  # Solid color or default
            color = f"\033[38;2;{self.hex_to_rgb(colors[0])}m" if colors else ''
            return f"{color}{shape * count}{RESET}"
        
        gradient = self.generate_gradient(colors, count)
        return ''.join(f"\033[38;2;{color[0]};{color[1]};{color[2]}m{shape}" for color in gradient) + RESET

    def hex_to_rgb(self, hex_color):
        return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

    def generate_gradient(self, hex_colors, count):
        colors = [self.hex_to_rgb(color) for color in hex_colors]
        gradient = []
        for i in range(len(colors) - 1):
            start_color = colors[i]
            end_color = colors[i + 1]
            for j in range(count // (len(colors) - 1)):
                factor = j / (count // (len(colors) - 1))
                gradient.append(self.interpolate_color(start_color, end_color, factor))
        return gradient + [colors[-1]]

    def interpolate_color(self, start_color, end_color, factor):
        return tuple(int(start_color[i] + (end_color[i] - start_color[i]) * factor) for i in range(3))

    def set_start_message(self, message):
        self.start_message = message

    def set_end_message(self, message):
        self.end_message = message

def example_regular_console():
    print(apply("[c #FF5733]Colored text[/c] with [bg #FFFF00]background color[/bg], [b]bold[/b], and [u]underline[/u]."))
    print(apply("This is the cool value: [g #FF00CC,#0000FF]Hello, World lets make it longer and longer![/g]"))


import time
def example_progress_bar(): 
    progress_bar = ProgressBar(total_slots=40, total_steps=100, positive_colors=['$FF00CC', '#0000FF'], negative_colors=['#555555'])
    progress_bar.set_start_message('Doing cool tasks:')
    progress_bar.set_end_message(apply('[c #00FF00]COMPLETE![/c]'))
    for i in range(101):
        progress_bar.set_progress(i)
        time.sleep(0.1)  # Simulate work