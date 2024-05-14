"""Reflex custom component NavMenu."""
import reflex as rx

from reflex.components.radix.primitives.base import RadixPrimitiveComponent
from reflex.components.radix.themes.base import LiteralAccentColor
from reflex.style import Style
from reflex.utils import imports

from typing import Any, Dict, List, Literal, Optional, Union
from reflex.vars import Var

from reflex.components.component import Component, ComponentNamespace
from reflex.components.core.colors import color
from reflex.components.lucide.icon import Icon

LiteralMenuComponentDir = Literal["ltr", "rtl"]
LiteralMenuComponentOrientation = Literal["vertical", "horizontal"]
LiteralAccordionRootVariant = Literal["classic", "soft", "surface", "outline", "ghost"]

DEFAULT_ANIMATION_DURATION = 250

cubic_bezier = "cubic-bezier(0.87, 0, 0.13, 1)"

class NavMenu(rx.Component):
    """NavMenu component."""

    # The React library to wrap.
    library = "@radix-ui/react-navigation-menu@^1.1.4"


class NavMenuRoot(NavMenu):
    """navigation menu root component"""

    tag = "Root"

    alias = "RadixNavigationMenuRoot"

    # The value of the item to expand.
    value: Var[str]

    # The default value of the item to expand.
    default_value: Var[str]

    # The duration from when the mouse enters a trigger until the content opens.
    delay_duration: Var[int] = 200

    # How much time a user has to enter another trigger without incurring a delay again.
    skip_delay_duration: Var[int] = 300

    # The orientation of the menu.
    orientation: Var[LiteralMenuComponentOrientation] = "horizontal"

    # The reading direction of the menu when applicable. 
    # If omitted, inherits globally from DirectionProvider or assumes LTR (left-to-right) reading mode.
    dir: Var[LiteralMenuComponentDir]

    def get_event_triggers(self) -> Dict[str, Any]:
        """Get the events triggers signatures for the component.

        Returns:
            The signatures of the event triggers.
        """
        return {
            **super().get_event_triggers(),
            "on_value_change": lambda e0: [e0],
        }

    def add_style(self) -> Style | None:
        return {
            "display": "flex",
            "justify-content": "space-between",
            "align-items": "center",
            "flex-direction": "column",
        }



class NavMenuSub(NavMenu):
    """Signifies a submenu. Use it in place of the root part when nested to create a submenu."""

    tag = "Sub"

    alias = "RadixNavigationMenuSub"

    default_value: Var[str]

    value: Var[str]

    orientation: rx.Var[Literal["horizontal", "vertical"]] = "vertical"


class NavMenuList(NavMenu):
    """Contains the top level menu items."""
    
    tag = "List"

    alias = "RadixNavigationMenuList"

    as_child: Var[bool]

    orientation: rx.Var[Literal["horizontal", "vertical"]]

    def add_style(self):
        return {
            "position": "relative",
            "display": "flex",
            "justify-content": "center",
            "width": "100%",
            "z-index": "1",
            "background-color": "white",
            "padding": "0",
            "border-radius": "6px",
            "list-style": "none",
            "box-shadow": "0 2px 10px var(--black-a7)",
            "margin": "0",
        }

class NavMenuLink(NavMenu):
    tag = "Link"
    alias = "RadixNavigationMenuLink"
    as_child = Var[bool]
    active = Var[bool]
    onSelect : rx.EventHandler[lambda e: [e]] = None

class NavMenuItem(NavMenu):
    """A top level menu item, contains a link or trigger with content combination."""

    tag = "Item"

    alias = "RadixNavigationMenuItem"

    as_child: Var[bool]

    value: Var[str]

    _valid_children: List[str] = ["NavMenuTrigger", "NavMenuLink", "NavMenuContent", "NavMenuSub"]

    _valid_parents: List[str] = ["NavMenuRoot", "NavMenuList"]

    def add_style(self) -> Style | None:
        return None

class NavMenuTrigger(NavMenu):
    """The button that toggles the content."""

    tag = "Trigger"

    alias = "RadixNavigationMenuTrigger"

    as_child: Var[bool] = False

    def add_style(self):
        return {
            "padding": "8px 12px",
            "outline": "none",
            "user-select": "none",
            "font-weight": "500",
            "line-height": "1",
            "border-radius": "4px",
            "font-size": "15px",
            "color": "var(--violet-11)",
        }


class NavMenuContent(NavMenu):
    """Contains the content associated with each trigger."""

    tag = "Content"

    alias = "RadixNavigationMenuContent"

    as_child: Var[bool] = False

    disable_outside_pointer_events: Var[bool] = False

    on_escape_key_down: rx.EventHandler[lambda e: [e]] = None

    on_pointer_down_outside: rx.EventHandler[lambda e: [e]] = None

    on_focus_outside: rx.EventHandler[lambda e: [e]] = None

    on_interact_outside: rx.EventHandler[lambda e: [e]] = None

    force_mount: Var[bool] = None

    def add_style(self):
        return {
            "position": "relative",
            "margin-left": "10px",
        }

class NavMenuIndicator(NavMenu):
    """
    An optional indicator element that renders below the list, 
    is used to highlight the currently active trigger.
    """

    tag = "Indicator"

    alias = "RadixNavigationMenuIdicator"

    as_child: Var[bool] = False

    force_mount: Var[bool] = None

    def add_style(self):
        return {
            "display": "flex",
            "align-items": "flex-end",
            "justify-content": "center",
            "height": "10px",
            "top": "100%",
            "overflow": "hidden",
            "z-index": "1"
        }

# Viewport
class NavMenuViewport(NavMenu):
    """An optional viewport element that is used to render active content outside of the list."""

    tag = "Viewport"

    alias = "RadixNavigationMenuViewport"

    as_child: Var[bool] = False

    force_mount: Var[bool]

    def add_style(self):
        return {
            "position": "relative",
            "transform-origin": "top center",
            "width": "100%",
        }





class NavMenu(rx.Component):
    """NavMenu component."""
    root = staticmethod(NavMenuRoot.create)
    sub = staticmethod(NavMenuSub.create)
    list = staticmethod(NavMenuList.create)
    item = staticmethod(NavMenuItem.create)
    trigger = staticmethod(NavMenuTrigger.create)
    content = staticmethod(NavMenuContent.create)
    indicator = staticmethod(NavMenuIndicator.create)
    viewport = staticmethod(NavMenuViewport.create)

nav_menu = NavMenu()









    # The React component tag.

    # If the tag is the default export from the module, you must set is_default = True.
    # This is normally used when components don't have curly braces around them when importing.
    # is_default = True

    # If you are wrapping another components with the same tag as a component in your project
    # you can use aliases to differentiate between them and avoid naming conflicts.
    # alias = "OtherNavMenu"

    # The props of the React component.
    # Note: when Reflex compiles the component to Javascript,
    # `snake_case` property names are automatically formatted as `camelCase`.
    # The prop names may be defined in `camelCase` as well.
    # some_prop: rx.Var[str] = "some default value"
    # some_other_prop: rx.Var[int] = 1

    # By default Reflex will install the library you have specified in the library property.
    # However, sometimes you may need to install other libraries to use a component.
    # In this case you can use the lib_dependencies property to specify other libraries to install.
    # lib_dependencies: list[str] = []

    # Event triggers declaration if any.
    # Below is equivalent to merging `{ "on_change": lambda e: [e] }`
    # onto the default event triggers of parent/base Component.
    # The function defined for the `on_change` trigger maps event for the javascript
    # trigger to what will be passed to the backend event handler function.
    # on_change: rx.EventHandler[lambda e: [e]]

    # To add custom code to your component
    # def _get_custom_code(self) -> str:
    #     return "const customCode = 'customCode';"

