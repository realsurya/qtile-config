#---------------------------------------#
#           ___           ___           #
#          /\__\         /\  \          #
#         /:/ _/_       |::\  \         #
#        /:/ /\  \      |:|:\  \        #
#       /:/ /::\  \   __|:|\:\  \       #
#      /:/_/:/\:\__\ /::::|_\:\__\      #
#      \:\/:/ /:/  / \:\~~\  \/__/      #
#       \::/ /:/  /   \:\  \            #
#        \/_/:/  /     \:\  \           #
#          /:/  /       \:\__\          #
#          \/__/         \/__/          #
#                                       #
#           ~My Qtile Config~           #
#             Feb. 04, 2022             #
#                                       #
#           Surya Manikhandan           #
#    Aerospace Eng. Student @ Purdue    #
#                                       #
#        [E]:smanikha@purdue.edu        #
#  [In]:linkedin.com/in/aerospacesurya  #
#      [Git]: github.com/realsurya      #
#---------------------------------------#

from typing import List

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

#---------------------------------------#
#             COLOR SCHEHE              #
#---------------------------------------#
black = '#000000'
transparent = '#00000000'
active = '#e74c3c'
inactive= '#34495e'

#---------------------------------------#
#            BASE KEYBINDS              #
#---------------------------------------#

mod = "mod4"
terminal = guess_terminal()

keys = [
    # My Ref: https://docs.qtile.orgm/en/latest/manual/config/lazy.html

    # Toggle focus between windows.
    Key([mod], "Left", lazy.layout.left(), desc="Switch focus left"),
    Key([mod], "Right", lazy.layout.right(), desc="Switch focus right"),
    Key([mod], "Down", lazy.layout.down(), desc="Switch focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Switch focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Switch window focus to other window"),

    # Move windows within columns or shuffle in current stack.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Manipulate window sizes.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Extend stack to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Extend stack to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Extend window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Extend window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # toggle priority of sleected window in stack.
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "d", lazy.spawn('rofi -theme gruvbox-dark-hard -font "hack 24" -show run -icon-theme "Papirus" -show-icons'), desc="Spawn rofi"),
]

#---------------------------------------#
#              WORKSPACES               #
#---------------------------------------#
groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            # Pure workspace shifting
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # Move windows between workspaces
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )


#---------------------------------------#
#             TILE LAYOUTS              #
#---------------------------------------#
layouts = [
    layout.Columns(border_focus=active,border_normal=inactive,border_on_single=True ,border_width=4,margin=15),
    layout.Max(),
    # layout.Stack(numm_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]


#---------------------------------------#
#                 BAR                   #
#---------------------------------------#
widget_defaults = dict(
    font="sans",
    fontsize=28,
    padding=20,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(background=black),
                widget.GroupBox(highlight_method='line', background=black, highlight_color=active),
                widget.Spacer(length=bar.STRETCH, bagkground=black),
                widget.Clock(format=" ~   %a %m/%d  %I:%M %p   ~ ", background=black),
                widget.Spacer(length=bar.STRETCH, bagkground=black),
                widget.Battery(format=' Bat1: {percent:2.0%}', update_interval=5, battery=1, background=black),
                widget.Battery(format='Bat2: {percent:2.0%} ', update_interval=5, battery=2, background=black),
            ],
            45,
            background=black,
            margin=[5,5,5,5]
        ),
    ),
]


#---------------------------------------#
#           FLOATING LAYOUTS            #
#---------------------------------------#
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
] # Drag floating layouts.

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(border_focus=active,border_normal=inactive,border_width=4,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)


#---------------------------------------#
#                QUIRKS                 #
#---------------------------------------#
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wmname = "Qtile"
