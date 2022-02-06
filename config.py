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
#            BASE KEYBINDS              #
#---------------------------------------#

mod = "mod4"
terminal = guess_terminal()

keys = [
    # Ref: https://docs.qtile.orgm/en/latest/manual/config/lazy.html
    # Toggle focus between windows.  
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows within columns or shuffle in current stack.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Manipulate window sizes.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # toggle priority of seected window in stack.
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
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]


#---------------------------------------#
#              WORKSPACES               #
#---------------------------------------#
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


#---------------------------------------#
#             TILE LAYOUTS              #
#---------------------------------------#
layouts = [
    layout.Columns(border_focus_stack=["#00E48B", "#000000"], border_width=4),
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
    fontsize=26,
    padding=20,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ffffff", "#ff0000"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox("| Surya M |", name="default"),     
                widget.Systray(),
                widget.Clock(format="| %I:%M %p - %a %m/%d |"),
                widget.Battery(format='| Bat: {percent:2.0%} ({hour:d}:{min:02d} {char}) |', charge_char="▲", discharge_char="▼", update_interval=3),
                widget.QuickExit(default_text="| Shutdown |", countdown_format ='| {} Seconds |')
            ],
            45,
            background='#000000',
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
floating_layout = layout.Floating(
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
wmname = "LG3D"
