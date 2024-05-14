from trame_client.widgets.core import AbstractElement, Template  # noqa
from ..module import quasar

class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(quasar)


class QAjaxBar(HtmlElement):
    """
    Properties

    :param position: Position within window of where QAjaxBar should be displayed
    :param size: Size in CSS units, including unit name
    :param color: Color name for component from the Quasar Color Palette
    :param reverse: Reverse direction of progress
    :param skip_hijack: Skip Ajax hijacking (not a reactive prop)
    :param hijack_filter: Filter which URL should trigger start() + stop()

    Events

    :param position: Position within window of where QAjaxBar should be displayed
    :param size: Size in CSS units, including unit name
    :param color: Color name for component from the Quasar Color Palette
    :param reverse: Reverse direction of progress
    :param skip_hijack: Skip Ajax hijacking (not a reactive prop)
    :param hijack_filter: Filter which URL should trigger start() + stop()
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-ajax-bar", children, **kwargs)
        self._attr_names += [
            "position",
            "size",
            "color",
            "reverse",
            "skip_hijack",
            "hijack_filter",
        ]
        self._event_names += [
            "start",
            "stop",
        ]


class QAvatar(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param font_size: The size in CSS units, including unit name, of the content (icon, text)
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param square: Removes border-radius so borders are squared
    :param rounded: Applies a small standard border-radius for a squared shape of the component

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param font_size: The size in CSS units, including unit name, of the content (icon, text)
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param square: Removes border-radius so borders are squared
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-avatar", children, **kwargs)
        self._attr_names += [
            "size",
            "font_size",
            "color",
            "text_color",
            "icon",
            "square",
            "rounded",
        ]
        self._event_names += [
        ]


class QBadge(HtmlElement):
    """
    Properties

    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param floating: Tell QBadge if it should float to the top right side of the relative positioned parent element or not
    :param transparent: Applies a 0.8 opacity; Useful especially for floating QBadge
    :param multi_line: Content can wrap to multiple lines
    :param label: Badge's content as string; overrides default slot if specified
    :param align: Sets vertical-align CSS prop
    :param outline: Use 'outline' design (colored text and borders only)
    :param rounded: Makes a rounded shaped badge

    Events

    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param floating: Tell QBadge if it should float to the top right side of the relative positioned parent element or not
    :param transparent: Applies a 0.8 opacity; Useful especially for floating QBadge
    :param multi_line: Content can wrap to multiple lines
    :param label: Badge's content as string; overrides default slot if specified
    :param align: Sets vertical-align CSS prop
    :param outline: Use 'outline' design (colored text and borders only)
    :param rounded: Makes a rounded shaped badge
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-badge", children, **kwargs)
        self._attr_names += [
            "color",
            "text_color",
            "floating",
            "transparent",
            "multi_line",
            "label",
            "align",
            "outline",
            "rounded",
        ]
        self._event_names += [
        ]


class QBanner(HtmlElement):
    """
    Properties

    :param inline_actions: Display actions on same row as content
    :param dense: Dense mode; occupies less space
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param dark: Notify the component that the background is a dark color

    Events

    :param inline_actions: Display actions on same row as content
    :param dense: Dense mode; occupies less space
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param dark: Notify the component that the background is a dark color
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-banner", children, **kwargs)
        self._attr_names += [
            "inline_actions",
            "dense",
            "rounded",
            "dark",
        ]
        self._event_names += [
        ]


class QBar(HtmlElement):
    """
    Properties

    :param dense: Dense mode; occupies less space
    :param dark: The component background color lights up the parent's background (as opposed to default behavior which is to darken it); Works unless you specify a CSS background color for it

    Events

    :param dense: Dense mode; occupies less space
    :param dark: The component background color lights up the parent's background (as opposed to default behavior which is to darken it); Works unless you specify a CSS background color for it
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-bar", children, **kwargs)
        self._attr_names += [
            "dense",
            "dark",
        ]
        self._event_names += [
        ]


class QBreadcrumbs(HtmlElement):
    """
    Properties

    :param separator: The string used to separate the breadcrumbs
    :param active_color: The color of the active breadcrumb, which can be any color from the Quasar Color Palette
    :param gutter: The gutter value allows you control over the space between the breadcrumb elements.
    :param separator_color: The color used to color the separator, which can be any color from the Quasar Color Palette
    :param align: Specify how to align the breadcrumbs horizontally

    Events

    :param separator: The string used to separate the breadcrumbs
    :param active_color: The color of the active breadcrumb, which can be any color from the Quasar Color Palette
    :param gutter: The gutter value allows you control over the space between the breadcrumb elements.
    :param separator_color: The color used to color the separator, which can be any color from the Quasar Color Palette
    :param align: Specify how to align the breadcrumbs horizontally
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-breadcrumbs", children, **kwargs)
        self._attr_names += [
            "separator",
            "active_color",
            "gutter",
            "separator_color",
            "align",
        ]
        self._event_names += [
        ]


class QBreadcrumbsEl(HtmlElement):
    """
    Properties

    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param exact: Equivalent to Vue Router <router-link> 'exact' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param exact_active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param target: Native <a> link target attribute; Use it only along with 'href' prop; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param disable: Put component in disabled mode
    :param label: The label text for the breadcrumb
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param tag: HTML tag to use

    Events

    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param exact: Equivalent to Vue Router <router-link> 'exact' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param exact_active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param target: Native <a> link target attribute; Use it only along with 'href' prop; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param disable: Put component in disabled mode
    :param label: The label text for the breadcrumb
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param tag: HTML tag to use
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-breadcrumbs-el", children, **kwargs)
        self._attr_names += [
            "to",
            "exact",
            "replace",
            "active_class",
            "exact_active_class",
            "href",
            "target",
            "disable",
            "label",
            "icon",
            "tag",
        ]
        self._event_names += [
            "click",
        ]


class QBtn(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param type: 1) Define the button native type attribute (submit, reset, button) or 2) render component with <a> tag so you can access events even if disable or 3) Use 'href' prop and specify 'type' as a media tag
    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to' and 'replace' props
    :param target: Native <a> link target attribute; Use it only with 'to' or 'href' props
    :param label: The text that will be shown on the button
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_right: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param outline: Use 'outline' design
    :param flat: Use 'flat' design
    :param unelevated: Remove shadow
    :param rounded: Applies a more prominent border-radius for a squared shape button
    :param push: Use 'push' design
    :param square: Removes border-radius so borders are squared
    :param glossy: Applies a glossy effect
    :param fab: Makes button size and shape to fit a Floating Action Button
    :param fab_mini: Makes button size and shape to fit a small Floating Action Button
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param no_caps: Avoid turning label text into caps (which happens by default)
    :param no_wrap: Avoid label text wrapping
    :param dense: Dense mode; occupies less space
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param tabindex: Tabindex HTML attribute value
    :param align: Label or content alignment
    :param stack: Stack icon and label vertically instead of on same line (like it is by default)
    :param stretch: When used on flexbox parent, button will stretch to parent's height
    :param loading: Put button into loading state (displays a QSpinner -- can be overridden by using a 'loading' slot)
    :param disable: Put component in disabled mode
    :param round: Makes a circle shaped button
    :param percentage: Percentage (0.0 < x < 100.0); To be used along 'loading' prop; Display a progress bar on the background
    :param dark_percentage: Progress bar on the background should have dark color; To be used along with 'percentage' and 'loading' props

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param type: 1) Define the button native type attribute (submit, reset, button) or 2) render component with <a> tag so you can access events even if disable or 3) Use 'href' prop and specify 'type' as a media tag
    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to' and 'replace' props
    :param target: Native <a> link target attribute; Use it only with 'to' or 'href' props
    :param label: The text that will be shown on the button
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_right: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param outline: Use 'outline' design
    :param flat: Use 'flat' design
    :param unelevated: Remove shadow
    :param rounded: Applies a more prominent border-radius for a squared shape button
    :param push: Use 'push' design
    :param square: Removes border-radius so borders are squared
    :param glossy: Applies a glossy effect
    :param fab: Makes button size and shape to fit a Floating Action Button
    :param fab_mini: Makes button size and shape to fit a small Floating Action Button
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param no_caps: Avoid turning label text into caps (which happens by default)
    :param no_wrap: Avoid label text wrapping
    :param dense: Dense mode; occupies less space
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param tabindex: Tabindex HTML attribute value
    :param align: Label or content alignment
    :param stack: Stack icon and label vertically instead of on same line (like it is by default)
    :param stretch: When used on flexbox parent, button will stretch to parent's height
    :param loading: Put button into loading state (displays a QSpinner -- can be overridden by using a 'loading' slot)
    :param disable: Put component in disabled mode
    :param round: Makes a circle shaped button
    :param percentage: Percentage (0.0 < x < 100.0); To be used along 'loading' prop; Display a progress bar on the background
    :param dark_percentage: Progress bar on the background should have dark color; To be used along with 'percentage' and 'loading' props
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-btn", children, **kwargs)
        self._attr_names += [
            "size",
            "type",
            "to",
            "replace",
            "href",
            "target",
            "label",
            "icon",
            "icon_right",
            "outline",
            "flat",
            "unelevated",
            "rounded",
            "push",
            "square",
            "glossy",
            "fab",
            "fab_mini",
            "padding",
            "color",
            "text_color",
            "no_caps",
            "no_wrap",
            "dense",
            "ripple",
            "tabindex",
            "align",
            "stack",
            "stretch",
            "loading",
            "disable",
            "round",
            "percentage",
            "dark_percentage",
        ]
        self._event_names += [
            "click",
        ]


class QBtnDropdown(HtmlElement):
    """
    Properties

    :param transition_show: One of Quasar's embedded transitions
    :param transition_hide: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param model_value: Controls Menu show/hidden state; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param type: 1) Define the button native type attribute (submit, reset, button) or 2) render component with <a> tag so you can access events even if disable or 3) Use 'href' prop and specify 'type' as a media tag
    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to' and 'replace' props
    :param target: Native <a> link target attribute; Use it only with 'to' or 'href' props
    :param label: The text that will be shown on the button
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_right: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param outline: Use 'outline' design
    :param flat: Use 'flat' design
    :param unelevated: Remove shadow
    :param rounded: Applies a more prominent border-radius for a squared shape button
    :param push: Use 'push' design
    :param square: Removes border-radius so borders are squared
    :param glossy: Applies a glossy effect
    :param fab: Makes button size and shape to fit a Floating Action Button
    :param fab_mini: Makes button size and shape to fit a small Floating Action Button
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param no_caps: Avoid turning label text into caps (which happens by default)
    :param no_wrap: Avoid label text wrapping
    :param dense: Dense mode; occupies less space
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param tabindex: Tabindex HTML attribute value
    :param align: Label or content alignment
    :param stack: Stack icon and label vertically instead of on same line (like it is by default)
    :param stretch: When used on flexbox parent, button will stretch to parent's height
    :param loading: Put button into loading state (displays a QSpinner -- can be overridden by using a 'loading' slot)
    :param disable: Put component in disabled mode
    :param split: Split dropdown icon into its own button
    :param dropdown_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param disable_main_btn: Disable main button (useful along with 'split' prop)
    :param disable_dropdown: Disables dropdown (dropdown button if using along 'split' prop)
    :param no_icon_animation: Disables the rotation of the dropdown icon when state is toggled
    :param content_style: Style definitions to be attributed to the menu
    :param content_class: Class definitions to be attributed to the menu
    :param cover: Allows the menu to cover the button. When used, the 'menu-self' and 'menu-fit' props are no longer effective
    :param persistent: Allows the menu to not be dismissed by a click/tap outside of the menu or by hitting the ESC key
    :param no_route_dismiss: Changing route app won't dismiss the popup; No need to set it if 'persistent' prop is also set
    :param auto_close: Allows any click/tap in the menu to close it; Useful instead of attaching events to each menu item that should close the menu on click/tap
    :param menu_anchor: Two values setting the starting position or anchor point of the menu relative to its target
    :param menu_self: Two values setting the menu's own position relative to its target
    :param menu_offset: An array of two numbers to offset the menu horizontally and vertically in pixels
    :param toggle_aria_label: aria-label to be used on the dropdown toggle element

    Events

    :param transition_show: One of Quasar's embedded transitions
    :param transition_hide: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param model_value: Controls Menu show/hidden state; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param type: 1) Define the button native type attribute (submit, reset, button) or 2) render component with <a> tag so you can access events even if disable or 3) Use 'href' prop and specify 'type' as a media tag
    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to' and 'replace' props
    :param target: Native <a> link target attribute; Use it only with 'to' or 'href' props
    :param label: The text that will be shown on the button
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_right: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param outline: Use 'outline' design
    :param flat: Use 'flat' design
    :param unelevated: Remove shadow
    :param rounded: Applies a more prominent border-radius for a squared shape button
    :param push: Use 'push' design
    :param square: Removes border-radius so borders are squared
    :param glossy: Applies a glossy effect
    :param fab: Makes button size and shape to fit a Floating Action Button
    :param fab_mini: Makes button size and shape to fit a small Floating Action Button
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param no_caps: Avoid turning label text into caps (which happens by default)
    :param no_wrap: Avoid label text wrapping
    :param dense: Dense mode; occupies less space
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param tabindex: Tabindex HTML attribute value
    :param align: Label or content alignment
    :param stack: Stack icon and label vertically instead of on same line (like it is by default)
    :param stretch: When used on flexbox parent, button will stretch to parent's height
    :param loading: Put button into loading state (displays a QSpinner -- can be overridden by using a 'loading' slot)
    :param disable: Put component in disabled mode
    :param split: Split dropdown icon into its own button
    :param dropdown_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param disable_main_btn: Disable main button (useful along with 'split' prop)
    :param disable_dropdown: Disables dropdown (dropdown button if using along 'split' prop)
    :param no_icon_animation: Disables the rotation of the dropdown icon when state is toggled
    :param content_style: Style definitions to be attributed to the menu
    :param content_class: Class definitions to be attributed to the menu
    :param cover: Allows the menu to cover the button. When used, the 'menu-self' and 'menu-fit' props are no longer effective
    :param persistent: Allows the menu to not be dismissed by a click/tap outside of the menu or by hitting the ESC key
    :param no_route_dismiss: Changing route app won't dismiss the popup; No need to set it if 'persistent' prop is also set
    :param auto_close: Allows any click/tap in the menu to close it; Useful instead of attaching events to each menu item that should close the menu on click/tap
    :param menu_anchor: Two values setting the starting position or anchor point of the menu relative to its target
    :param menu_self: Two values setting the menu's own position relative to its target
    :param menu_offset: An array of two numbers to offset the menu horizontally and vertically in pixels
    :param toggle_aria_label: aria-label to be used on the dropdown toggle element
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-btn-dropdown", children, **kwargs)
        self._attr_names += [
            "transition_show",
            "transition_hide",
            "transition_duration",
            "model_value",
            "size",
            "type",
            "to",
            "replace",
            "href",
            "target",
            "label",
            "icon",
            "icon_right",
            "outline",
            "flat",
            "unelevated",
            "rounded",
            "push",
            "square",
            "glossy",
            "fab",
            "fab_mini",
            "padding",
            "color",
            "text_color",
            "no_caps",
            "no_wrap",
            "dense",
            "ripple",
            "tabindex",
            "align",
            "stack",
            "stretch",
            "loading",
            "disable",
            "split",
            "dropdown_icon",
            "disable_main_btn",
            "disable_dropdown",
            "no_icon_animation",
            "content_style",
            "content_class",
            "cover",
            "persistent",
            "no_route_dismiss",
            "auto_close",
            "menu_anchor",
            "menu_self",
            "menu_offset",
            "toggle_aria_label",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "show",
            "before_show",
            "hide",
            "before_hide",
            "click",
        ]


class QBtnGroup(HtmlElement):
    """
    Properties

    :param spread: Spread horizontally to all available space
    :param outline: Use 'outline' design for buttons
    :param flat: Use 'flat' design for buttons
    :param unelevated: Remove shadow on buttons
    :param rounded: Applies a more prominent border-radius for squared shape buttons
    :param square: Removes border-radius so borders are squared
    :param push: Use 'push' design for buttons
    :param stretch: When used on flexbox parent, buttons will stretch to parent's height
    :param glossy: Applies a glossy effect

    Events

    :param spread: Spread horizontally to all available space
    :param outline: Use 'outline' design for buttons
    :param flat: Use 'flat' design for buttons
    :param unelevated: Remove shadow on buttons
    :param rounded: Applies a more prominent border-radius for squared shape buttons
    :param square: Removes border-radius so borders are squared
    :param push: Use 'push' design for buttons
    :param stretch: When used on flexbox parent, buttons will stretch to parent's height
    :param glossy: Applies a glossy effect
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-btn-group", children, **kwargs)
        self._attr_names += [
            "spread",
            "outline",
            "flat",
            "unelevated",
            "rounded",
            "square",
            "push",
            "stretch",
            "glossy",
        ]
        self._event_names += [
        ]


class QBtnToggle(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param options: Array of Objects defining each option
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param toggle_color: Color name for component from the Quasar Color Palette
    :param toggle_text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param spread: Spread horizontally to all available space
    :param outline: Use 'outline' design
    :param flat: Use 'flat' design
    :param unelevated: Remove shadow
    :param rounded: Applies a more prominent border-radius for a squared shape button
    :param push: Use 'push' design
    :param glossy: Applies a glossy effect
    :param size: Button size name or a CSS unit including unit name
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param no_caps: Avoid turning label text into caps (which happens by default)
    :param no_wrap: Avoid label text wrapping
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param dense: Dense mode; occupies less space
    :param readonly: Put component in readonly mode
    :param disable: Put component in disabled mode
    :param stack: Stack icon and label vertically instead of on same line (like it is by default)
    :param stretch: When used on flexbox parent, button will stretch to parent's height
    :param clearable: Clears model on click of the already selected button

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param options: Array of Objects defining each option
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param toggle_color: Color name for component from the Quasar Color Palette
    :param toggle_text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param spread: Spread horizontally to all available space
    :param outline: Use 'outline' design
    :param flat: Use 'flat' design
    :param unelevated: Remove shadow
    :param rounded: Applies a more prominent border-radius for a squared shape button
    :param push: Use 'push' design
    :param glossy: Applies a glossy effect
    :param size: Button size name or a CSS unit including unit name
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param no_caps: Avoid turning label text into caps (which happens by default)
    :param no_wrap: Avoid label text wrapping
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param dense: Dense mode; occupies less space
    :param readonly: Put component in readonly mode
    :param disable: Put component in disabled mode
    :param stack: Stack icon and label vertically instead of on same line (like it is by default)
    :param stretch: When used on flexbox parent, button will stretch to parent's height
    :param clearable: Clears model on click of the already selected button
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-btn-toggle", children, **kwargs)
        self._attr_names += [
            "name",
            "model_value",
            "options",
            "color",
            "text_color",
            "toggle_color",
            "toggle_text_color",
            "spread",
            "outline",
            "flat",
            "unelevated",
            "rounded",
            "push",
            "glossy",
            "size",
            "padding",
            "no_caps",
            "no_wrap",
            "ripple",
            "dense",
            "readonly",
            "disable",
            "stack",
            "stretch",
            "clearable",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "clear",
        ]


class QCard(HtmlElement):
    """
    Properties

    :param dark: Notify the component that the background is a dark color
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param tag: HTML tag to use

    Events

    :param dark: Notify the component that the background is a dark color
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param tag: HTML tag to use
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-card", children, **kwargs)
        self._attr_names += [
            "dark",
            "square",
            "flat",
            "bordered",
            "tag",
        ]
        self._event_names += [
        ]


class QCardActions(HtmlElement):
    """
    Properties

    :param align: Specify how to align the actions
    :param vertical: Display actions one below the other

    Events

    :param align: Specify how to align the actions
    :param vertical: Display actions one below the other
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-card-actions", children, **kwargs)
        self._attr_names += [
            "align",
            "vertical",
        ]
        self._event_names += [
        ]


class QCardSection(HtmlElement):
    """
    Properties

    :param horizontal: Display a horizontal section (will have no padding and can contain other QCardSection)
    :param tag: HTML tag to use

    Events

    :param horizontal: Display a horizontal section (will have no padding and can contain other QCardSection)
    :param tag: HTML tag to use
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-card-section", children, **kwargs)
        self._attr_names += [
            "horizontal",
            "tag",
        ]
        self._event_names += [
        ]


class QCarousel(HtmlElement):
    """
    Properties

    :param fullscreen: Fullscreen mode
    :param no_route_fullscreen_exit: Changing route app won't exit fullscreen
    :param model_value: Model of the component defining the current panel's name; If a Number is used, it does not define the panel's index, but rather the panel's name which can also be an Integer; Either use this property (along with a listener for 'update:model-value' event) OR use the v-model directive.
    :param keep_alive: Equivalent to using Vue's native <keep-alive> component on the content
    :param keep_alive_include: Equivalent to using Vue's native include prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_exclude: Equivalent to using Vue's native exclude prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_max: Equivalent to using Vue's native max prop for <keep-alive>
    :param animated: Enable transitions between panel (also see 'transition-prev' and 'transition-next' props)
    :param infinite: Makes component appear as infinite (when reaching last panel, next one will become the first one)
    :param swipeable: Enable swipe events (may interfere with content's touch/mouse events)
    :param vertical: Default transitions and swipe actions will be on the vertical axis
    :param transition_prev: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_next: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param dark: Notify the component that the background is a dark color
    :param height: Height of Carousel in CSS units, including unit name
    :param padding: Applies a default padding to each slide, according to the usage of 'arrows' and 'navigation' props
    :param control_color: Color name for QCarousel button controls (arrows, navigation) from the Quasar Color Palette
    :param control_text_color: Color name for text color of QCarousel button controls (arrows, navigation) from the Quasar Color Palette
    :param control_type: Type of button to use for controls (arrows, navigation)
    :param autoplay: Jump to next slide (if 'true' or val > 0) or previous slide (if val < 0) at fixed time intervals (in milliseconds); 'false' disables autoplay, 'true' enables it for 5000ms intervals
    :param arrows: Show navigation arrow buttons
    :param prev_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param next_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param navigation: Show navigation dots
    :param navigation_position: Side to stick navigation to
    :param navigation_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param navigation_active_icon: Icon name following Quasar convention for the active (current slide) navigation icon; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param thumbnails: Show thumbnails

    Events

    :param fullscreen: Fullscreen mode
    :param no_route_fullscreen_exit: Changing route app won't exit fullscreen
    :param model_value: Model of the component defining the current panel's name; If a Number is used, it does not define the panel's index, but rather the panel's name which can also be an Integer; Either use this property (along with a listener for 'update:model-value' event) OR use the v-model directive.
    :param keep_alive: Equivalent to using Vue's native <keep-alive> component on the content
    :param keep_alive_include: Equivalent to using Vue's native include prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_exclude: Equivalent to using Vue's native exclude prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_max: Equivalent to using Vue's native max prop for <keep-alive>
    :param animated: Enable transitions between panel (also see 'transition-prev' and 'transition-next' props)
    :param infinite: Makes component appear as infinite (when reaching last panel, next one will become the first one)
    :param swipeable: Enable swipe events (may interfere with content's touch/mouse events)
    :param vertical: Default transitions and swipe actions will be on the vertical axis
    :param transition_prev: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_next: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param dark: Notify the component that the background is a dark color
    :param height: Height of Carousel in CSS units, including unit name
    :param padding: Applies a default padding to each slide, according to the usage of 'arrows' and 'navigation' props
    :param control_color: Color name for QCarousel button controls (arrows, navigation) from the Quasar Color Palette
    :param control_text_color: Color name for text color of QCarousel button controls (arrows, navigation) from the Quasar Color Palette
    :param control_type: Type of button to use for controls (arrows, navigation)
    :param autoplay: Jump to next slide (if 'true' or val > 0) or previous slide (if val < 0) at fixed time intervals (in milliseconds); 'false' disables autoplay, 'true' enables it for 5000ms intervals
    :param arrows: Show navigation arrow buttons
    :param prev_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param next_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param navigation: Show navigation dots
    :param navigation_position: Side to stick navigation to
    :param navigation_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param navigation_active_icon: Icon name following Quasar convention for the active (current slide) navigation icon; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param thumbnails: Show thumbnails
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-carousel", children, **kwargs)
        self._attr_names += [
            "fullscreen",
            "no_route_fullscreen_exit",
            "model_value",
            "keep_alive",
            "keep_alive_include",
            "keep_alive_exclude",
            "keep_alive_max",
            "animated",
            "infinite",
            "swipeable",
            "vertical",
            "transition_prev",
            "transition_next",
            "transition_duration",
            "dark",
            "height",
            "padding",
            "control_color",
            "control_text_color",
            "control_type",
            "autoplay",
            "arrows",
            "prev_icon",
            "next_icon",
            "navigation",
            "navigation_position",
            "navigation_icon",
            "navigation_active_icon",
            "thumbnails",
        ]
        self._event_names += [
            "fullscreen",
            ("update_model_value", "update:model-value"),
            "before_transition",
            "transition",
        ]


class QCarouselControl(HtmlElement):
    """
    Properties

    :param position: Side/corner to stick to
    :param offset: An array of two numbers to offset the component horizontally and vertically (in pixels)

    Events

    :param position: Side/corner to stick to
    :param offset: An array of two numbers to offset the component horizontally and vertically (in pixels)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-carousel-control", children, **kwargs)
        self._attr_names += [
            "position",
            "offset",
        ]
        self._event_names += [
        ]


class QCarouselSlide(HtmlElement):
    """
    Properties

    :param name: Slide name
    :param disable: Put component in disabled mode
    :param img_src: URL pointing to a slide background image (use public folder)

    Events

    :param name: Slide name
    :param disable: Put component in disabled mode
    :param img_src: URL pointing to a slide background image (use public folder)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-carousel-slide", children, **kwargs)
        self._attr_names += [
            "name",
            "disable",
            "img_src",
        ]
        self._event_names += [
        ]


class QChatMessage(HtmlElement):
    """
    Properties

    :param sent: Render as a sent message (so from current user)
    :param label: Renders a label header/section only
    :param bg_color: Color name (from the Quasar Color Palette) for chat bubble background
    :param text_color: Color name (from the Quasar Color Palette) for chat bubble text
    :param name: Author's name
    :param avatar: URL to the avatar image of the author
    :param text: Array of strings that are the message body. Strings are not sanitized (see details in docs)
    :param stamp: Creation timestamp
    :param size: 1-12 out of 12 (same as col-*)
    :param label_html: Render the label as HTML; This can lead to XSS attacks so make sure that you sanitize the message first
    :param name_html: Render the name as HTML; This can lead to XSS attacks so make sure that you sanitize the message first
    :param text_html: Render the text as HTML; This can lead to XSS attacks so make sure that you sanitize the message first
    :param stamp_html: Render the stamp as HTML; This can lead to XSS attacks so make sure that you sanitize the message first

    Events

    :param sent: Render as a sent message (so from current user)
    :param label: Renders a label header/section only
    :param bg_color: Color name (from the Quasar Color Palette) for chat bubble background
    :param text_color: Color name (from the Quasar Color Palette) for chat bubble text
    :param name: Author's name
    :param avatar: URL to the avatar image of the author
    :param text: Array of strings that are the message body. Strings are not sanitized (see details in docs)
    :param stamp: Creation timestamp
    :param size: 1-12 out of 12 (same as col-*)
    :param label_html: Render the label as HTML; This can lead to XSS attacks so make sure that you sanitize the message first
    :param name_html: Render the name as HTML; This can lead to XSS attacks so make sure that you sanitize the message first
    :param text_html: Render the text as HTML; This can lead to XSS attacks so make sure that you sanitize the message first
    :param stamp_html: Render the stamp as HTML; This can lead to XSS attacks so make sure that you sanitize the message first
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-chat-message", children, **kwargs)
        self._attr_names += [
            "sent",
            "label",
            "bg_color",
            "text_color",
            "name",
            "avatar",
            "text",
            "stamp",
            "size",
            "label_html",
            "name_html",
            "text_html",
            "stamp_html",
        ]
        self._event_names += [
        ]


class QCheckbox(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param val: Works when model ('value') is Array. It tells the component which value should add/remove when ticked/unticked
    :param true_value: What model value should be considered as checked/ticked/on?
    :param false_value: What model value should be considered as unchecked/unticked/off?
    :param indeterminate_value: What model value should be considered as 'indeterminate'?
    :param toggle_order: Determines toggle order of the two states ('t' stands for state of true, 'f' for state of false); If 'toggle-indeterminate' is true, then the order is: indet -> first state -> second state -> indet (and repeat), otherwise: indet -> first state -> second state -> first state -> second state -> ...
    :param toggle_indeterminate: When user clicks/taps on the component, should we toggle through the indeterminate state too?
    :param label: Label to display along the component (or use the default slot instead of this prop)
    :param left_label: Label (if any specified) should be displayed on the left side of the component
    :param checked_icon: The icon to be used when the model is truthy (instead of the default design)
    :param unchecked_icon: The icon to be used when the toggle is falsy (instead of the default design)
    :param indeterminate_icon: The icon to be used when the model is indeterminate (instead of the default design)
    :param color: Color name for component from the Quasar Color Palette
    :param keep_color: Should the color (if specified any) be kept when the component is unticked/ off?
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param disable: Put component in disabled mode
    :param tabindex: Tabindex HTML attribute value

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param val: Works when model ('value') is Array. It tells the component which value should add/remove when ticked/unticked
    :param true_value: What model value should be considered as checked/ticked/on?
    :param false_value: What model value should be considered as unchecked/unticked/off?
    :param indeterminate_value: What model value should be considered as 'indeterminate'?
    :param toggle_order: Determines toggle order of the two states ('t' stands for state of true, 'f' for state of false); If 'toggle-indeterminate' is true, then the order is: indet -> first state -> second state -> indet (and repeat), otherwise: indet -> first state -> second state -> first state -> second state -> ...
    :param toggle_indeterminate: When user clicks/taps on the component, should we toggle through the indeterminate state too?
    :param label: Label to display along the component (or use the default slot instead of this prop)
    :param left_label: Label (if any specified) should be displayed on the left side of the component
    :param checked_icon: The icon to be used when the model is truthy (instead of the default design)
    :param unchecked_icon: The icon to be used when the toggle is falsy (instead of the default design)
    :param indeterminate_icon: The icon to be used when the model is indeterminate (instead of the default design)
    :param color: Color name for component from the Quasar Color Palette
    :param keep_color: Should the color (if specified any) be kept when the component is unticked/ off?
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param disable: Put component in disabled mode
    :param tabindex: Tabindex HTML attribute value
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-checkbox", children, **kwargs)
        self._attr_names += [
            "name",
            "size",
            "model_value",
            "val",
            "true_value",
            "false_value",
            "indeterminate_value",
            "toggle_order",
            "toggle_indeterminate",
            "label",
            "left_label",
            "checked_icon",
            "unchecked_icon",
            "indeterminate_icon",
            "color",
            "keep_color",
            "dark",
            "dense",
            "disable",
            "tabindex",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
        ]


class QChip(HtmlElement):
    """
    Properties

    :param dense: Dense mode; occupies less space
    :param size: QChip size name or a CSS unit including unit name
    :param dark: Notify the component that the background is a dark color
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_right: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_remove: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_selected: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param label: Chip's content as string; overrides default slot if specified
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param model_value: Model of the component determining if QChip should be rendered or not
    :param selected: Model for QChip if it's selected or not
    :param square: Sets a low value for border-radius instead of the default one, making it close to a square
    :param outline: Display using the 'outline' design
    :param clickable: Is QChip clickable? If it's the case, then it will add hover effects and emit 'click' events
    :param removable: If set, then it displays a 'remove' icon that when clicked the QChip emits 'remove' event
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param remove_aria_label: aria-label to be used on the remove icon
    :param tabindex: Tabindex HTML attribute value
    :param disable: Put component in disabled mode

    Events

    :param dense: Dense mode; occupies less space
    :param size: QChip size name or a CSS unit including unit name
    :param dark: Notify the component that the background is a dark color
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_right: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_remove: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_selected: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param label: Chip's content as string; overrides default slot if specified
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param model_value: Model of the component determining if QChip should be rendered or not
    :param selected: Model for QChip if it's selected or not
    :param square: Sets a low value for border-radius instead of the default one, making it close to a square
    :param outline: Display using the 'outline' design
    :param clickable: Is QChip clickable? If it's the case, then it will add hover effects and emit 'click' events
    :param removable: If set, then it displays a 'remove' icon that when clicked the QChip emits 'remove' event
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param remove_aria_label: aria-label to be used on the remove icon
    :param tabindex: Tabindex HTML attribute value
    :param disable: Put component in disabled mode
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-chip", children, **kwargs)
        self._attr_names += [
            "dense",
            "size",
            "dark",
            "icon",
            "icon_right",
            "icon_remove",
            "icon_selected",
            "label",
            "color",
            "text_color",
            "model_value",
            "selected",
            "square",
            "outline",
            "clickable",
            "removable",
            "ripple",
            "remove_aria_label",
            "tabindex",
            "disable",
        ]
        self._event_names += [
            "click",
            ("update_selected", "update:selected"),
            "remove",
        ]


class QCircularProgress(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param value: Current progress (must be between min/max)
    :param min: Minimum value defining 'no progress' (must be lower than 'max')
    :param max: Maximum value defining 100% progress made (must be higher than 'min')
    :param color: Color name for the arc progress from the Quasar Color Palette
    :param center_color: Color name for the center part of the component from the Quasar Color Palette
    :param track_color: Color name for the track of the component from the Quasar Color Palette
    :param font_size: Size of text in CSS units, including unit name. Suggestion: use 'em' units to sync with component size
    :param rounded: Rounding the arc of progress
    :param thickness: Thickness of progress arc as a ratio (0.0 < x < 1.0) of component size
    :param angle: Angle to rotate progress arc by
    :param indeterminate: Put component into 'indeterminate' state; Ignores 'value' prop
    :param show_value: Enables the default slot and uses it (if available), otherwise it displays the 'value' prop as text; Make sure the text has enough space to be displayed inside the component
    :param reverse: Reverses the direction of progress; Only for determined state
    :param instant_feedback: No animation when model changes
    :param animation_speed: Animation speed (in milliseconds, without unit)

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param value: Current progress (must be between min/max)
    :param min: Minimum value defining 'no progress' (must be lower than 'max')
    :param max: Maximum value defining 100% progress made (must be higher than 'min')
    :param color: Color name for the arc progress from the Quasar Color Palette
    :param center_color: Color name for the center part of the component from the Quasar Color Palette
    :param track_color: Color name for the track of the component from the Quasar Color Palette
    :param font_size: Size of text in CSS units, including unit name. Suggestion: use 'em' units to sync with component size
    :param rounded: Rounding the arc of progress
    :param thickness: Thickness of progress arc as a ratio (0.0 < x < 1.0) of component size
    :param angle: Angle to rotate progress arc by
    :param indeterminate: Put component into 'indeterminate' state; Ignores 'value' prop
    :param show_value: Enables the default slot and uses it (if available), otherwise it displays the 'value' prop as text; Make sure the text has enough space to be displayed inside the component
    :param reverse: Reverses the direction of progress; Only for determined state
    :param instant_feedback: No animation when model changes
    :param animation_speed: Animation speed (in milliseconds, without unit)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-circular-progress", children, **kwargs)
        self._attr_names += [
            "size",
            "value",
            "min",
            "max",
            "color",
            "center_color",
            "track_color",
            "font_size",
            "rounded",
            "thickness",
            "angle",
            "indeterminate",
            "show_value",
            "reverse",
            "instant_feedback",
            "animation_speed",
        ]
        self._event_names += [
        ]


class QColor(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param default_value: The default value to show when the model doesn't have one
    :param default_view: The default view of the picker
    :param format_model: Forces a certain model format upon the model
    :param palette: Use a custom palette of colors for the palette tab
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param no_header: Do not render header
    :param no_header_tabs: Do not render header tabs (only the input)
    :param no_footer: Do not render footer; Useful when you want a specific view ('default-view' prop) and don't want the user to be able to switch it
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param dark: Notify the component that the background is a dark color

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param default_value: The default value to show when the model doesn't have one
    :param default_view: The default view of the picker
    :param format_model: Forces a certain model format upon the model
    :param palette: Use a custom palette of colors for the palette tab
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param no_header: Do not render header
    :param no_header_tabs: Do not render header tabs (only the input)
    :param no_footer: Do not render footer; Useful when you want a specific view ('default-view' prop) and don't want the user to be able to switch it
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param dark: Notify the component that the background is a dark color
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-color", children, **kwargs)
        self._attr_names += [
            "name",
            "model_value",
            "default_value",
            "default_view",
            "format_model",
            "palette",
            "square",
            "flat",
            "bordered",
            "no_header",
            "no_header_tabs",
            "no_footer",
            "disable",
            "readonly",
            "dark",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "change",
        ]


class QDate(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param landscape: Display the component in landscape mode
    :param mask: Mask (formatting string) used for parsing and formatting value
    :param locale: Locale formatting options
    :param calendar: Specify calendar type
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param readonly: Put component in readonly mode
    :param disable: Put component in disabled mode
    :param model_value: Date(s) of the component; Must be Array if using 'multiple' prop; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param title: When specified, it overrides the default header title; Makes sense when not in 'minimal' mode
    :param subtitle: When specified, it overrides the default header subtitle; Makes sense when not in 'minimal' mode
    :param default_year_month: The default year and month to display (in YYYY/MM format) when model is unfilled (undefined or null); Please ensure it is within the navigation min/max year-month (if using them)
    :param default_view: The view which will be displayed by default
    :param years_in_month_view: Show the years selector in months view
    :param events: A list of events to highlight on the calendar; If using a function, it receives the date as a String and must return a Boolean (matches or not); If using a function then for best performance, reference it from your scope and do not define it inline
    :param event_color: Color name (from the Quasar Color Palette); If using a function, it receives the date as a String and must return a String (color for the received date); If using a function then for best performance, reference it from your scope and do not define it inline
    :param options: Optionally configure the days that are selectable; If using a function, it receives the date as a String and must return a Boolean (is date acceptable or not); If using a function then for best performance, reference it from your scope and do not define it inline; Incompatible with 'range' prop
    :param navigation_min_year_month: Lock user from navigating below a specific year+month (in YYYY/MM format); This prop is not used to correct the model; You might want to also use 'default-year-month' prop
    :param navigation_max_year_month: Lock user from navigating above a specific year+month (in YYYY/MM format); This prop is not used to correct the model; You might want to also use 'default-year-month' prop
    :param no_unset: Remove ability to unselect a date; It does not apply to selecting a range over already selected dates
    :param first_day_of_week: Sets the day of the week that is considered the first day (0 - Sunday, 1 - Monday, ...); This day will show in the left-most column of the calendar
    :param today_btn: Display a button that selects the current day
    :param minimal: Don’t display the header
    :param multiple: Allow multiple selection; Model must be Array
    :param range: Allow range selection; Partial compatibility with 'options' prop: selected ranges might also include 'unselectable' days
    :param emit_immediately: Emit model when user browses month and year too; ONLY for single selection (non-multiple, non-range)

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param landscape: Display the component in landscape mode
    :param mask: Mask (formatting string) used for parsing and formatting value
    :param locale: Locale formatting options
    :param calendar: Specify calendar type
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param readonly: Put component in readonly mode
    :param disable: Put component in disabled mode
    :param model_value: Date(s) of the component; Must be Array if using 'multiple' prop; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param title: When specified, it overrides the default header title; Makes sense when not in 'minimal' mode
    :param subtitle: When specified, it overrides the default header subtitle; Makes sense when not in 'minimal' mode
    :param default_year_month: The default year and month to display (in YYYY/MM format) when model is unfilled (undefined or null); Please ensure it is within the navigation min/max year-month (if using them)
    :param default_view: The view which will be displayed by default
    :param years_in_month_view: Show the years selector in months view
    :param events: A list of events to highlight on the calendar; If using a function, it receives the date as a String and must return a Boolean (matches or not); If using a function then for best performance, reference it from your scope and do not define it inline
    :param event_color: Color name (from the Quasar Color Palette); If using a function, it receives the date as a String and must return a String (color for the received date); If using a function then for best performance, reference it from your scope and do not define it inline
    :param options: Optionally configure the days that are selectable; If using a function, it receives the date as a String and must return a Boolean (is date acceptable or not); If using a function then for best performance, reference it from your scope and do not define it inline; Incompatible with 'range' prop
    :param navigation_min_year_month: Lock user from navigating below a specific year+month (in YYYY/MM format); This prop is not used to correct the model; You might want to also use 'default-year-month' prop
    :param navigation_max_year_month: Lock user from navigating above a specific year+month (in YYYY/MM format); This prop is not used to correct the model; You might want to also use 'default-year-month' prop
    :param no_unset: Remove ability to unselect a date; It does not apply to selecting a range over already selected dates
    :param first_day_of_week: Sets the day of the week that is considered the first day (0 - Sunday, 1 - Monday, ...); This day will show in the left-most column of the calendar
    :param today_btn: Display a button that selects the current day
    :param minimal: Don’t display the header
    :param multiple: Allow multiple selection; Model must be Array
    :param range: Allow range selection; Partial compatibility with 'options' prop: selected ranges might also include 'unselectable' days
    :param emit_immediately: Emit model when user browses month and year too; ONLY for single selection (non-multiple, non-range)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-date", children, **kwargs)
        self._attr_names += [
            "name",
            "landscape",
            "mask",
            "locale",
            "calendar",
            "color",
            "text_color",
            "dark",
            "square",
            "flat",
            "bordered",
            "readonly",
            "disable",
            "model_value",
            "title",
            "subtitle",
            "default_year_month",
            "default_view",
            "years_in_month_view",
            "events",
            "event_color",
            "options",
            "navigation_min_year_month",
            "navigation_max_year_month",
            "no_unset",
            "first_day_of_week",
            "today_btn",
            "minimal",
            "multiple",
            "range",
            "emit_immediately",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "navigation",
            "range_start",
            "range_end",
        ]


class QDialog(HtmlElement):
    """
    Properties

    :param transition_show: One of Quasar's embedded transitions
    :param transition_hide: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param model_value: Model of the component defining shown/hidden state; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param persistent: User cannot dismiss Dialog if clicking outside of it or hitting ESC key; Also, an app route change won't dismiss it
    :param no_esc_dismiss: User cannot dismiss Dialog by hitting ESC key; No need to set it if 'persistent' prop is also set
    :param no_backdrop_dismiss: User cannot dismiss Dialog by clicking outside of it; No need to set it if 'persistent' prop is also set
    :param no_route_dismiss: Changing route app won't dismiss Dialog; No need to set it if 'persistent' prop is also set
    :param auto_close: Any click/tap inside of the dialog will close it
    :param seamless: Put Dialog into seamless mode; Does not use a backdrop so user is able to interact with the rest of the page too
    :param maximized: Put Dialog into maximized mode
    :param full_width: Dialog will try to render with same width as the window
    :param full_height: Dialog will try to render with same height as the window
    :param position: Stick dialog to one of the sides (top, right, bottom or left)
    :param square: Forces content to have squared borders
    :param no_refocus: (Accessibility) When Dialog gets hidden, do not refocus on the DOM element that previously had focus
    :param no_focus: (Accessibility) When Dialog gets shown, do not switch focus on it
    :param no_shake: Do not shake up the Dialog to catch user's attention
    :param allow_focus_outside: Allow elements outside of the Dialog to be focusable; By default, for accessibility reasons, QDialog does not allow outer focus

    Events

    :param transition_show: One of Quasar's embedded transitions
    :param transition_hide: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param model_value: Model of the component defining shown/hidden state; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param persistent: User cannot dismiss Dialog if clicking outside of it or hitting ESC key; Also, an app route change won't dismiss it
    :param no_esc_dismiss: User cannot dismiss Dialog by hitting ESC key; No need to set it if 'persistent' prop is also set
    :param no_backdrop_dismiss: User cannot dismiss Dialog by clicking outside of it; No need to set it if 'persistent' prop is also set
    :param no_route_dismiss: Changing route app won't dismiss Dialog; No need to set it if 'persistent' prop is also set
    :param auto_close: Any click/tap inside of the dialog will close it
    :param seamless: Put Dialog into seamless mode; Does not use a backdrop so user is able to interact with the rest of the page too
    :param maximized: Put Dialog into maximized mode
    :param full_width: Dialog will try to render with same width as the window
    :param full_height: Dialog will try to render with same height as the window
    :param position: Stick dialog to one of the sides (top, right, bottom or left)
    :param square: Forces content to have squared borders
    :param no_refocus: (Accessibility) When Dialog gets hidden, do not refocus on the DOM element that previously had focus
    :param no_focus: (Accessibility) When Dialog gets shown, do not switch focus on it
    :param no_shake: Do not shake up the Dialog to catch user's attention
    :param allow_focus_outside: Allow elements outside of the Dialog to be focusable; By default, for accessibility reasons, QDialog does not allow outer focus
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-dialog", children, **kwargs)
        self._attr_names += [
            "transition_show",
            "transition_hide",
            "transition_duration",
            "model_value",
            "persistent",
            "no_esc_dismiss",
            "no_backdrop_dismiss",
            "no_route_dismiss",
            "auto_close",
            "seamless",
            "maximized",
            "full_width",
            "full_height",
            "position",
            "square",
            "no_refocus",
            "no_focus",
            "no_shake",
            "allow_focus_outside",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "show",
            "before_show",
            "hide",
            "before_hide",
            "shake",
            "escape_key",
        ]


class QDrawer(HtmlElement):
    """
    Properties

    :param model_value: Model of the component defining shown/hidden state; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param side: Side to attach to
    :param overlay: Puts drawer into overlay mode (does not occupy space on screen, narrowing the page)
    :param width: Width of drawer (in pixels)
    :param mini: Puts drawer into mini mode
    :param mini_width: Width of drawer (in pixels) when in mini mode
    :param mini_to_overlay: Mini mode will expand as an overlay
    :param no_mini_animation: Disables animation of the drawer when toggling mini mode
    :param dark: Notify the component that the background is a dark color
    :param breakpoint: Breakpoint (in pixels) of layout width up to which mobile mode is used
    :param behavior: Overrides the default dynamic mode into which the drawer is put on
    :param bordered: Applies a default border to the component
    :param elevated: Adds a default shadow to the header
    :param persistent: Prevents drawer from auto-closing when app's route changes
    :param show_if_above: Forces drawer to be shown on screen on initial render if the layout width is above breakpoint, regardless of v-model; This is the default behavior when SSR is taken over by client on initial render
    :param no_swipe_open: Disables the default behavior where drawer can be swiped into view; Useful for iOS platforms where it might interfere with Safari's 'swipe to go to previous/next page' feature
    :param no_swipe_close: Disables the default behavior where drawer can be swiped out of view (applies to drawer content only); Useful for iOS platforms where it might interfere with Safari's 'swipe to go to previous/next page' feature
    :param no_swipe_backdrop: Disables the default behavior where drawer backdrop can be swiped

    Events

    :param model_value: Model of the component defining shown/hidden state; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param side: Side to attach to
    :param overlay: Puts drawer into overlay mode (does not occupy space on screen, narrowing the page)
    :param width: Width of drawer (in pixels)
    :param mini: Puts drawer into mini mode
    :param mini_width: Width of drawer (in pixels) when in mini mode
    :param mini_to_overlay: Mini mode will expand as an overlay
    :param no_mini_animation: Disables animation of the drawer when toggling mini mode
    :param dark: Notify the component that the background is a dark color
    :param breakpoint: Breakpoint (in pixels) of layout width up to which mobile mode is used
    :param behavior: Overrides the default dynamic mode into which the drawer is put on
    :param bordered: Applies a default border to the component
    :param elevated: Adds a default shadow to the header
    :param persistent: Prevents drawer from auto-closing when app's route changes
    :param show_if_above: Forces drawer to be shown on screen on initial render if the layout width is above breakpoint, regardless of v-model; This is the default behavior when SSR is taken over by client on initial render
    :param no_swipe_open: Disables the default behavior where drawer can be swiped into view; Useful for iOS platforms where it might interfere with Safari's 'swipe to go to previous/next page' feature
    :param no_swipe_close: Disables the default behavior where drawer can be swiped out of view (applies to drawer content only); Useful for iOS platforms where it might interfere with Safari's 'swipe to go to previous/next page' feature
    :param no_swipe_backdrop: Disables the default behavior where drawer backdrop can be swiped
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-drawer", children, **kwargs)
        self._attr_names += [
            "model_value",
            "side",
            "overlay",
            "width",
            "mini",
            "mini_width",
            "mini_to_overlay",
            "no_mini_animation",
            "dark",
            "breakpoint",
            "behavior",
            "bordered",
            "elevated",
            "persistent",
            "show_if_above",
            "no_swipe_open",
            "no_swipe_close",
            "no_swipe_backdrop",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "show",
            "before_show",
            "hide",
            "before_hide",
            "on_layout",
            "click",
            "mouseover",
            "mouseout",
            "mini_state",
        ]


class QEditor(HtmlElement):
    """
    Properties

    :param fullscreen: Fullscreen mode
    :param no_route_fullscreen_exit: Changing route app won't exit fullscreen
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param readonly: Put component in readonly mode
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no borders)
    :param dense: Dense mode; toolbar buttons are shown on one-line only
    :param dark: Notify the component that the background is a dark color
    :param disable: Put component in disabled mode
    :param min_height: CSS unit for the minimum height of the editable area
    :param max_height: CSS unit for maximum height of the input area
    :param height: CSS value to set the height of the editable area
    :param definitions: Definition of commands and their buttons to be included in the 'toolbar' prop
    :param fonts: Object with definitions of fonts
    :param toolbar: An array of arrays of Objects/Strings that you use to define the construction of the elements and commands available in the toolbar
    :param toolbar_color: Font color (from the Quasar Palette) of buttons and text in the toolbar
    :param toolbar_text_color: Text color (from the Quasar Palette) of toolbar commands
    :param toolbar_toggle_color: Choose the active color (from the Quasar Palette) of toolbar commands button
    :param toolbar_bg: Toolbar background color (from Quasar Palette)
    :param toolbar_outline: Toolbar buttons are rendered "outlined"
    :param toolbar_push: Toolbar buttons are rendered as a "push-button" type
    :param toolbar_rounded: Toolbar buttons are rendered "rounded"
    :param paragraph_tag: Paragraph tag to be used
    :param content_style: Object with CSS properties and values for styling the container of QEditor
    :param content_class: CSS classes for the input area
    :param placeholder: Text to display as placeholder

    Events

    :param fullscreen: Fullscreen mode
    :param no_route_fullscreen_exit: Changing route app won't exit fullscreen
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param readonly: Put component in readonly mode
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no borders)
    :param dense: Dense mode; toolbar buttons are shown on one-line only
    :param dark: Notify the component that the background is a dark color
    :param disable: Put component in disabled mode
    :param min_height: CSS unit for the minimum height of the editable area
    :param max_height: CSS unit for maximum height of the input area
    :param height: CSS value to set the height of the editable area
    :param definitions: Definition of commands and their buttons to be included in the 'toolbar' prop
    :param fonts: Object with definitions of fonts
    :param toolbar: An array of arrays of Objects/Strings that you use to define the construction of the elements and commands available in the toolbar
    :param toolbar_color: Font color (from the Quasar Palette) of buttons and text in the toolbar
    :param toolbar_text_color: Text color (from the Quasar Palette) of toolbar commands
    :param toolbar_toggle_color: Choose the active color (from the Quasar Palette) of toolbar commands button
    :param toolbar_bg: Toolbar background color (from Quasar Palette)
    :param toolbar_outline: Toolbar buttons are rendered "outlined"
    :param toolbar_push: Toolbar buttons are rendered as a "push-button" type
    :param toolbar_rounded: Toolbar buttons are rendered "rounded"
    :param paragraph_tag: Paragraph tag to be used
    :param content_style: Object with CSS properties and values for styling the container of QEditor
    :param content_class: CSS classes for the input area
    :param placeholder: Text to display as placeholder
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-editor", children, **kwargs)
        self._attr_names += [
            "fullscreen",
            "no_route_fullscreen_exit",
            "model_value",
            "readonly",
            "square",
            "flat",
            "dense",
            "dark",
            "disable",
            "min_height",
            "max_height",
            "height",
            "definitions",
            "fonts",
            "toolbar",
            "toolbar_color",
            "toolbar_text_color",
            "toolbar_toggle_color",
            "toolbar_bg",
            "toolbar_outline",
            "toolbar_push",
            "toolbar_rounded",
            "paragraph_tag",
            "content_style",
            "content_class",
            "placeholder",
        ]
        self._event_names += [
            "fullscreen",
            ("update_model_value", "update:model-value"),
            "dropdown_show",
            "dropdown_before_show",
            "dropdown_hide",
            "dropdown_before_hide",
            "link_show",
            "link_hide",
        ]


class QExpansionItem(HtmlElement):
    """
    Properties

    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param exact: Equivalent to Vue Router <router-link> 'exact' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param exact_active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param target: Native <a> link target attribute; Use it only along with 'href' prop; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param disable: Put component in disabled mode
    :param model_value: Model of the component defining 'open' state; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param expand_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param expanded_icon: Expand icon name (following Quasar convention) for when QExpansionItem is expanded; When used, it also disables the rotation animation of the expand icon; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param expand_icon_class: Apply custom class(es) to the expand icon item section
    :param toggle_aria_label: aria-label to be used on the expansion toggle element
    :param label: Header label (unless using 'header' slot)
    :param label_lines: Apply ellipsis when there's not enough space to render on the specified number of lines; If more than one line specified, then it will only work on webkit browsers because it uses the '-webkit-line-clamp' CSS property!
    :param caption: Header sub-label (unless using 'header' slot)
    :param caption_lines: Apply ellipsis when there's not enough space to render on the specified number of lines; If more than one line specified, then it will only work on webkit browsers because it uses the '-webkit-line-clamp' CSS property!
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param duration: Animation duration (in milliseconds)
    :param header_inset_level: Apply an inset to header (unless using 'header' slot); Useful when header avatar/left side is missing but you want to align content with other items that do have a left side, or when you're building a menu
    :param content_inset_level: Apply an inset to content (changes content padding)
    :param expand_separator: Apply a top and bottom separator when expansion item is opened
    :param default_opened: Puts expansion item into open state on initial render; Overridden by v-model if used
    :param hide_expand_icon: Do not show the expand icon
    :param expand_icon_toggle: Applies the expansion events to the expand icon only and not to the whole header
    :param switch_toggle_side: Switch expand icon side (from default 'right' to 'left')
    :param dense_toggle: Use dense mode for expand icon
    :param group: Register expansion item into a group (unique name that must be applied to all expansion items in that group) for coordinated open/close state within the group a.k.a. 'accordion mode'
    :param popup: Put expansion list into 'popup' mode
    :param header_style: Apply custom style to the header
    :param header_class: Apply custom class(es) to the header

    Events

    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param exact: Equivalent to Vue Router <router-link> 'exact' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param exact_active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param target: Native <a> link target attribute; Use it only along with 'href' prop; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param disable: Put component in disabled mode
    :param model_value: Model of the component defining 'open' state; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param expand_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param expanded_icon: Expand icon name (following Quasar convention) for when QExpansionItem is expanded; When used, it also disables the rotation animation of the expand icon; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param expand_icon_class: Apply custom class(es) to the expand icon item section
    :param toggle_aria_label: aria-label to be used on the expansion toggle element
    :param label: Header label (unless using 'header' slot)
    :param label_lines: Apply ellipsis when there's not enough space to render on the specified number of lines; If more than one line specified, then it will only work on webkit browsers because it uses the '-webkit-line-clamp' CSS property!
    :param caption: Header sub-label (unless using 'header' slot)
    :param caption_lines: Apply ellipsis when there's not enough space to render on the specified number of lines; If more than one line specified, then it will only work on webkit browsers because it uses the '-webkit-line-clamp' CSS property!
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param duration: Animation duration (in milliseconds)
    :param header_inset_level: Apply an inset to header (unless using 'header' slot); Useful when header avatar/left side is missing but you want to align content with other items that do have a left side, or when you're building a menu
    :param content_inset_level: Apply an inset to content (changes content padding)
    :param expand_separator: Apply a top and bottom separator when expansion item is opened
    :param default_opened: Puts expansion item into open state on initial render; Overridden by v-model if used
    :param hide_expand_icon: Do not show the expand icon
    :param expand_icon_toggle: Applies the expansion events to the expand icon only and not to the whole header
    :param switch_toggle_side: Switch expand icon side (from default 'right' to 'left')
    :param dense_toggle: Use dense mode for expand icon
    :param group: Register expansion item into a group (unique name that must be applied to all expansion items in that group) for coordinated open/close state within the group a.k.a. 'accordion mode'
    :param popup: Put expansion list into 'popup' mode
    :param header_style: Apply custom style to the header
    :param header_class: Apply custom class(es) to the header
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-expansion-item", children, **kwargs)
        self._attr_names += [
            "to",
            "exact",
            "replace",
            "active_class",
            "exact_active_class",
            "href",
            "target",
            "disable",
            "model_value",
            "icon",
            "expand_icon",
            "expanded_icon",
            "expand_icon_class",
            "toggle_aria_label",
            "label",
            "label_lines",
            "caption",
            "caption_lines",
            "dark",
            "dense",
            "duration",
            "header_inset_level",
            "content_inset_level",
            "expand_separator",
            "default_opened",
            "hide_expand_icon",
            "expand_icon_toggle",
            "switch_toggle_side",
            "dense_toggle",
            "group",
            "popup",
            "header_style",
            "header_class",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "show",
            "before_show",
            "hide",
            "before_hide",
            "after_show",
            "after_hide",
        ]


class QFab(HtmlElement):
    """
    Properties

    :param type: Define the button HTML DOM type
    :param outline: Use 'outline' design for Fab button
    :param push: Use 'push' design for Fab button
    :param flat: Use 'flat' design for Fab button
    :param unelevated: Remove shadow
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param glossy: Apply the glossy effect over the button
    :param external_label: Display label besides the FABs, as external content
    :param label: The label that will be shown when Fab is extended
    :param label_position: Position of the label around the icon
    :param hide_label: Hide the label; Useful for animation purposes where you toggle the visibility of the label
    :param label_class: Class definitions to be attributed to the label container
    :param label_style: Style definitions to be attributed to the label container
    :param square: Apply a rectangle aspect to the FAB
    :param disable: Put component in disabled mode
    :param tabindex: Tabindex HTML attribute value
    :param model_value: Controls state of fab actions (showing/hidden); Works best with v-model directive, otherwise use along listening to 'update:modelValue' event
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param active_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param hide_icon: Hide the icon (don't use any)
    :param direction: Direction to expand Fab Actions to
    :param vertical_actions_align: The side of the Fab where Fab Actions will expand (only when direction is 'up' or 'down')
    :param persistent: By default, Fab Actions are hidden when user navigates to another route and this prop disables this behavior

    Events

    :param type: Define the button HTML DOM type
    :param outline: Use 'outline' design for Fab button
    :param push: Use 'push' design for Fab button
    :param flat: Use 'flat' design for Fab button
    :param unelevated: Remove shadow
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param glossy: Apply the glossy effect over the button
    :param external_label: Display label besides the FABs, as external content
    :param label: The label that will be shown when Fab is extended
    :param label_position: Position of the label around the icon
    :param hide_label: Hide the label; Useful for animation purposes where you toggle the visibility of the label
    :param label_class: Class definitions to be attributed to the label container
    :param label_style: Style definitions to be attributed to the label container
    :param square: Apply a rectangle aspect to the FAB
    :param disable: Put component in disabled mode
    :param tabindex: Tabindex HTML attribute value
    :param model_value: Controls state of fab actions (showing/hidden); Works best with v-model directive, otherwise use along listening to 'update:modelValue' event
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param active_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param hide_icon: Hide the icon (don't use any)
    :param direction: Direction to expand Fab Actions to
    :param vertical_actions_align: The side of the Fab where Fab Actions will expand (only when direction is 'up' or 'down')
    :param persistent: By default, Fab Actions are hidden when user navigates to another route and this prop disables this behavior
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-fab", children, **kwargs)
        self._attr_names += [
            "type",
            "outline",
            "push",
            "flat",
            "unelevated",
            "padding",
            "color",
            "text_color",
            "glossy",
            "external_label",
            "label",
            "label_position",
            "hide_label",
            "label_class",
            "label_style",
            "square",
            "disable",
            "tabindex",
            "model_value",
            "icon",
            "active_icon",
            "hide_icon",
            "direction",
            "vertical_actions_align",
            "persistent",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "show",
            "before_show",
            "hide",
            "before_hide",
        ]


class QFabAction(HtmlElement):
    """
    Properties

    :param type: Define the button HTML DOM type
    :param outline: Use 'outline' design for Fab button
    :param push: Use 'push' design for Fab button
    :param flat: Use 'flat' design for Fab button
    :param unelevated: Remove shadow
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param glossy: Apply the glossy effect over the button
    :param external_label: Display label besides the FABs, as external content
    :param label: The label that will be shown when Fab is extended
    :param label_position: Position of the label around the icon
    :param hide_label: Hide the label; Useful for animation purposes where you toggle the visibility of the label
    :param label_class: Class definitions to be attributed to the label container
    :param label_style: Style definitions to be attributed to the label container
    :param square: Apply a rectangle aspect to the FAB
    :param disable: Put component in disabled mode
    :param tabindex: Tabindex HTML attribute value
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param anchor: How to align the Fab Action relative to Fab expand side; By default it uses the align specified in QFab
    :param to: Equivalent to Vue Router <router-link> 'to' property
    :param replace: Equivalent to Vue Router <router-link> 'replace' property

    Events

    :param type: Define the button HTML DOM type
    :param outline: Use 'outline' design for Fab button
    :param push: Use 'push' design for Fab button
    :param flat: Use 'flat' design for Fab button
    :param unelevated: Remove shadow
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param glossy: Apply the glossy effect over the button
    :param external_label: Display label besides the FABs, as external content
    :param label: The label that will be shown when Fab is extended
    :param label_position: Position of the label around the icon
    :param hide_label: Hide the label; Useful for animation purposes where you toggle the visibility of the label
    :param label_class: Class definitions to be attributed to the label container
    :param label_style: Style definitions to be attributed to the label container
    :param square: Apply a rectangle aspect to the FAB
    :param disable: Put component in disabled mode
    :param tabindex: Tabindex HTML attribute value
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param anchor: How to align the Fab Action relative to Fab expand side; By default it uses the align specified in QFab
    :param to: Equivalent to Vue Router <router-link> 'to' property
    :param replace: Equivalent to Vue Router <router-link> 'replace' property
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-fab-action", children, **kwargs)
        self._attr_names += [
            "type",
            "outline",
            "push",
            "flat",
            "unelevated",
            "padding",
            "color",
            "text_color",
            "glossy",
            "external_label",
            "label",
            "label_position",
            "hide_label",
            "label_class",
            "label_style",
            "square",
            "disable",
            "tabindex",
            "icon",
            "anchor",
            "to",
            "replace",
        ]
        self._event_names += [
            "click",
        ]


class QField(HtmlElement):
    """
    Properties

    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param error: Does field have validation errors?
    :param error_message: Validation error message (gets displayed only if 'error' is set to 'true')
    :param no_error_icon: Hide error icon when there is an error
    :param rules: Array of Functions/Strings; If String, then it must be a name of one of the embedded validation rules
    :param reactive_rules: By default a change in the rules does not trigger a new validation until the model changes; If set to true then a change in the rules will trigger a validation; Has a performance penalty, so use it only when you really need it
    :param lazy_rules: If set to boolean true then it checks validation status against the 'rules' only after field loses focus for first time; If set to 'ondemand' then it will trigger only when component's validate() method is manually called or when the wrapper QForm submits itself
    :param label: A text label that will “float” up above the input field, once the field gets focus
    :param stack_label: Label will be always shown above the field regardless of field content (if any)
    :param hint: Helper (hint) text which gets placed below your wrapped form component
    :param hide_hint: Hide the helper (hint) text when field doesn't have focus
    :param prefix: Prefix
    :param suffix: Suffix
    :param label_color: Color name for the label from the Quasar Color Palette; Overrides the 'color' prop; The difference from 'color' prop is that the label will always have this color, even when field is not focused
    :param color: Color name for component from the Quasar Color Palette
    :param bg_color: Color name for component from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param loading: Signals the user a process is in progress by displaying a spinner; Spinner can be customized by using the 'loading' slot.
    :param clearable: Appends clearable icon when a value (not undefined or null) is set; When clicked, model becomes null
    :param clear_icon: Custom icon to use for the clear button when using along with 'clearable' prop
    :param filled: Use 'filled' design for the field
    :param outlined: Use 'outlined' design for the field
    :param borderless: Use 'borderless' design for the field
    :param standout: Use 'standout' design for the field; Specifies classes to be applied when focused (overriding default ones)
    :param label_slot: Enables label slot; You need to set it to force use of the 'label' slot if the 'label' prop is not set
    :param bottom_slots: Enables bottom slots ('error', 'hint', 'counter')
    :param hide_bottom_space: Do not reserve space for hint/error/counter anymore when these are not used; As a result, it also disables the animation for those; It also allows the hint/error area to stretch vertically based on its content
    :param counter: Show an automatic counter on bottom right
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param square: Remove border-radius so borders are squared; Overrides 'rounded' prop
    :param dense: Dense mode; occupies less space
    :param item_aligned: Match inner content alignment to that of QItem
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param autofocus: Focus field on initial component render
    :param for: Used to specify the 'id' of the control and also the 'for' attribute of the label that wraps it; If no 'name' prop is specified, then it is used for this attribute as well
    :param name: Used to specify the name of the control; Useful if dealing with forms; If not specified, it takes the value of 'for' prop, if it exists
    :param maxlength: Specify a max length of model

    Events

    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param error: Does field have validation errors?
    :param error_message: Validation error message (gets displayed only if 'error' is set to 'true')
    :param no_error_icon: Hide error icon when there is an error
    :param rules: Array of Functions/Strings; If String, then it must be a name of one of the embedded validation rules
    :param reactive_rules: By default a change in the rules does not trigger a new validation until the model changes; If set to true then a change in the rules will trigger a validation; Has a performance penalty, so use it only when you really need it
    :param lazy_rules: If set to boolean true then it checks validation status against the 'rules' only after field loses focus for first time; If set to 'ondemand' then it will trigger only when component's validate() method is manually called or when the wrapper QForm submits itself
    :param label: A text label that will “float” up above the input field, once the field gets focus
    :param stack_label: Label will be always shown above the field regardless of field content (if any)
    :param hint: Helper (hint) text which gets placed below your wrapped form component
    :param hide_hint: Hide the helper (hint) text when field doesn't have focus
    :param prefix: Prefix
    :param suffix: Suffix
    :param label_color: Color name for the label from the Quasar Color Palette; Overrides the 'color' prop; The difference from 'color' prop is that the label will always have this color, even when field is not focused
    :param color: Color name for component from the Quasar Color Palette
    :param bg_color: Color name for component from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param loading: Signals the user a process is in progress by displaying a spinner; Spinner can be customized by using the 'loading' slot.
    :param clearable: Appends clearable icon when a value (not undefined or null) is set; When clicked, model becomes null
    :param clear_icon: Custom icon to use for the clear button when using along with 'clearable' prop
    :param filled: Use 'filled' design for the field
    :param outlined: Use 'outlined' design for the field
    :param borderless: Use 'borderless' design for the field
    :param standout: Use 'standout' design for the field; Specifies classes to be applied when focused (overriding default ones)
    :param label_slot: Enables label slot; You need to set it to force use of the 'label' slot if the 'label' prop is not set
    :param bottom_slots: Enables bottom slots ('error', 'hint', 'counter')
    :param hide_bottom_space: Do not reserve space for hint/error/counter anymore when these are not used; As a result, it also disables the animation for those; It also allows the hint/error area to stretch vertically based on its content
    :param counter: Show an automatic counter on bottom right
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param square: Remove border-radius so borders are squared; Overrides 'rounded' prop
    :param dense: Dense mode; occupies less space
    :param item_aligned: Match inner content alignment to that of QItem
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param autofocus: Focus field on initial component render
    :param for: Used to specify the 'id' of the control and also the 'for' attribute of the label that wraps it; If no 'name' prop is specified, then it is used for this attribute as well
    :param name: Used to specify the name of the control; Useful if dealing with forms; If not specified, it takes the value of 'for' prop, if it exists
    :param maxlength: Specify a max length of model
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-field", children, **kwargs)
        self._attr_names += [
            "model_value",
            "error",
            "error_message",
            "no_error_icon",
            "rules",
            "reactive_rules",
            "lazy_rules",
            "label",
            "stack_label",
            "hint",
            "hide_hint",
            "prefix",
            "suffix",
            "label_color",
            "color",
            "bg_color",
            "dark",
            "loading",
            "clearable",
            "clear_icon",
            "filled",
            "outlined",
            "borderless",
            "standout",
            "label_slot",
            "bottom_slots",
            "hide_bottom_space",
            "counter",
            "rounded",
            "square",
            "dense",
            "item_aligned",
            "disable",
            "readonly",
            "autofocus",
            "for",
            "name",
            "maxlength",
        ]
        self._event_names += [
            "clear",
            ("update_model_value", "update:model-value"),
            "focus",
            "blur",
        ]


class QFile(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms; If not specified, it takes the value of 'for' prop, if it exists
    :param multiple: Allow multiple file uploads
    :param accept: Comma separated list of unique file type specifiers. Maps to 'accept' attribute of native input type=file element
    :param capture: Optionally, specify that a new file should be captured, and which device should be used to capture that new media of a type defined by the 'accept' prop. Maps to 'capture' attribute of native input type=file element
    :param max_file_size: Maximum size of individual file in bytes
    :param max_total_size: Maximum size of all files combined in bytes
    :param max_files: Maximum number of files to contain
    :param filter: Custom filter for added files; Only files that pass this filter will be added to the queue and uploaded; For best performance, reference it from your scope and do not define it inline
    :param model_value: Model of the component; Must be FileList or Array if using 'multiple' prop; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param error: Does field have validation errors?
    :param error_message: Validation error message (gets displayed only if 'error' is set to 'true')
    :param no_error_icon: Hide error icon when there is an error
    :param rules: Array of Functions/Strings; If String, then it must be a name of one of the embedded validation rules
    :param reactive_rules: By default a change in the rules does not trigger a new validation until the model changes; If set to true then a change in the rules will trigger a validation; Has a performance penalty, so use it only when you really need it
    :param lazy_rules: If set to boolean true then it checks validation status against the 'rules' only after field loses focus for first time; If set to 'ondemand' then it will trigger only when component's validate() method is manually called or when the wrapper QForm submits itself
    :param label: A text label that will “float” up above the input field, once the field gets focus
    :param stack_label: Label will be always shown above the field regardless of field content (if any)
    :param hint: Helper (hint) text which gets placed below your wrapped form component
    :param hide_hint: Hide the helper (hint) text when field doesn't have focus
    :param prefix: Prefix
    :param suffix: Suffix
    :param label_color: Color name for the label from the Quasar Color Palette; Overrides the 'color' prop; The difference from 'color' prop is that the label will always have this color, even when field is not focused
    :param color: Color name for component from the Quasar Color Palette
    :param bg_color: Color name for component from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param loading: Signals the user a process is in progress by displaying a spinner; Spinner can be customized by using the 'loading' slot.
    :param clearable: Appends clearable icon when a value (not undefined or null) is set; When clicked, model becomes null
    :param clear_icon: Custom icon to use for the clear button when using along with 'clearable' prop
    :param filled: Use 'filled' design for the field
    :param outlined: Use 'outlined' design for the field
    :param borderless: Use 'borderless' design for the field
    :param standout: Use 'standout' design for the field; Specifies classes to be applied when focused (overriding default ones)
    :param label_slot: Enables label slot; You need to set it to force use of the 'label' slot if the 'label' prop is not set
    :param bottom_slots: Enables bottom slots ('error', 'hint', 'counter')
    :param hide_bottom_space: Do not reserve space for hint/error/counter anymore when these are not used; As a result, it also disables the animation for those; It also allows the hint/error area to stretch vertically based on its content
    :param counter: Show an automatic counter on bottom right
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param square: Remove border-radius so borders are squared; Overrides 'rounded' prop
    :param dense: Dense mode; occupies less space
    :param item_aligned: Match inner content alignment to that of QItem
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param autofocus: Focus field on initial component render
    :param for: Used to specify the 'id' of the control and also the 'for' attribute of the label that wraps it; If no 'name' prop is specified, then it is used for this attribute as well
    :param append: Append file(s) to current model rather than replacing them; Has effect only when using 'multiple' mode
    :param display_value: Override default selection string, if not using 'file' or 'selected' scoped slots and if not using 'use-chips' prop
    :param use_chips: Use QChip to show picked files
    :param counter_label: Label for the counter; The 'counter' prop is necessary to enable this one
    :param tabindex: Tabindex HTML attribute value
    :param input_class: Class definitions to be attributed to the underlying selection container
    :param input_style: Style definitions to be attributed to the underlying selection container

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms; If not specified, it takes the value of 'for' prop, if it exists
    :param multiple: Allow multiple file uploads
    :param accept: Comma separated list of unique file type specifiers. Maps to 'accept' attribute of native input type=file element
    :param capture: Optionally, specify that a new file should be captured, and which device should be used to capture that new media of a type defined by the 'accept' prop. Maps to 'capture' attribute of native input type=file element
    :param max_file_size: Maximum size of individual file in bytes
    :param max_total_size: Maximum size of all files combined in bytes
    :param max_files: Maximum number of files to contain
    :param filter: Custom filter for added files; Only files that pass this filter will be added to the queue and uploaded; For best performance, reference it from your scope and do not define it inline
    :param model_value: Model of the component; Must be FileList or Array if using 'multiple' prop; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param error: Does field have validation errors?
    :param error_message: Validation error message (gets displayed only if 'error' is set to 'true')
    :param no_error_icon: Hide error icon when there is an error
    :param rules: Array of Functions/Strings; If String, then it must be a name of one of the embedded validation rules
    :param reactive_rules: By default a change in the rules does not trigger a new validation until the model changes; If set to true then a change in the rules will trigger a validation; Has a performance penalty, so use it only when you really need it
    :param lazy_rules: If set to boolean true then it checks validation status against the 'rules' only after field loses focus for first time; If set to 'ondemand' then it will trigger only when component's validate() method is manually called or when the wrapper QForm submits itself
    :param label: A text label that will “float” up above the input field, once the field gets focus
    :param stack_label: Label will be always shown above the field regardless of field content (if any)
    :param hint: Helper (hint) text which gets placed below your wrapped form component
    :param hide_hint: Hide the helper (hint) text when field doesn't have focus
    :param prefix: Prefix
    :param suffix: Suffix
    :param label_color: Color name for the label from the Quasar Color Palette; Overrides the 'color' prop; The difference from 'color' prop is that the label will always have this color, even when field is not focused
    :param color: Color name for component from the Quasar Color Palette
    :param bg_color: Color name for component from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param loading: Signals the user a process is in progress by displaying a spinner; Spinner can be customized by using the 'loading' slot.
    :param clearable: Appends clearable icon when a value (not undefined or null) is set; When clicked, model becomes null
    :param clear_icon: Custom icon to use for the clear button when using along with 'clearable' prop
    :param filled: Use 'filled' design for the field
    :param outlined: Use 'outlined' design for the field
    :param borderless: Use 'borderless' design for the field
    :param standout: Use 'standout' design for the field; Specifies classes to be applied when focused (overriding default ones)
    :param label_slot: Enables label slot; You need to set it to force use of the 'label' slot if the 'label' prop is not set
    :param bottom_slots: Enables bottom slots ('error', 'hint', 'counter')
    :param hide_bottom_space: Do not reserve space for hint/error/counter anymore when these are not used; As a result, it also disables the animation for those; It also allows the hint/error area to stretch vertically based on its content
    :param counter: Show an automatic counter on bottom right
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param square: Remove border-radius so borders are squared; Overrides 'rounded' prop
    :param dense: Dense mode; occupies less space
    :param item_aligned: Match inner content alignment to that of QItem
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param autofocus: Focus field on initial component render
    :param for: Used to specify the 'id' of the control and also the 'for' attribute of the label that wraps it; If no 'name' prop is specified, then it is used for this attribute as well
    :param append: Append file(s) to current model rather than replacing them; Has effect only when using 'multiple' mode
    :param display_value: Override default selection string, if not using 'file' or 'selected' scoped slots and if not using 'use-chips' prop
    :param use_chips: Use QChip to show picked files
    :param counter_label: Label for the counter; The 'counter' prop is necessary to enable this one
    :param tabindex: Tabindex HTML attribute value
    :param input_class: Class definitions to be attributed to the underlying selection container
    :param input_style: Style definitions to be attributed to the underlying selection container
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-file", children, **kwargs)
        self._attr_names += [
            "name",
            "multiple",
            "accept",
            "capture",
            "max_file_size",
            "max_total_size",
            "max_files",
            "filter",
            "model_value",
            "error",
            "error_message",
            "no_error_icon",
            "rules",
            "reactive_rules",
            "lazy_rules",
            "label",
            "stack_label",
            "hint",
            "hide_hint",
            "prefix",
            "suffix",
            "label_color",
            "color",
            "bg_color",
            "dark",
            "loading",
            "clearable",
            "clear_icon",
            "filled",
            "outlined",
            "borderless",
            "standout",
            "label_slot",
            "bottom_slots",
            "hide_bottom_space",
            "counter",
            "rounded",
            "square",
            "dense",
            "item_aligned",
            "disable",
            "readonly",
            "autofocus",
            "for",
            "append",
            "display_value",
            "use_chips",
            "counter_label",
            "tabindex",
            "input_class",
            "input_style",
        ]
        self._event_names += [
            "rejected",
            "clear",
            ("update_model_value", "update:model-value"),
        ]


class QFooter(HtmlElement):
    """
    Properties

    :param model_value: Model of the component defining if it is shown or hidden to the user; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param reveal: Enable 'reveal' mode; Takes into account user scroll to temporarily show/hide footer
    :param bordered: Applies a default border to the component
    :param elevated: Adds a default shadow to the footer
    :param height_hint: When using SSR, you can optionally hint of the height (in pixels) of the QFooter

    Events

    :param model_value: Model of the component defining if it is shown or hidden to the user; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param reveal: Enable 'reveal' mode; Takes into account user scroll to temporarily show/hide footer
    :param bordered: Applies a default border to the component
    :param elevated: Adds a default shadow to the footer
    :param height_hint: When using SSR, you can optionally hint of the height (in pixels) of the QFooter
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-footer", children, **kwargs)
        self._attr_names += [
            "model_value",
            "reveal",
            "bordered",
            "elevated",
            "height_hint",
        ]
        self._event_names += [
            "reveal",
        ]


class QForm(HtmlElement):
    """
    Properties

    :param autofocus: Focus first focusable element on initial component render
    :param no_error_focus: Do not try to focus on first component that has a validation error when submitting form
    :param no_reset_focus: Do not try to focus on first component when resetting form
    :param greedy: Validate all fields in form (by default it stops after finding the first invalid field with synchronous validation)

    Events

    :param autofocus: Focus first focusable element on initial component render
    :param no_error_focus: Do not try to focus on first component that has a validation error when submitting form
    :param no_reset_focus: Do not try to focus on first component when resetting form
    :param greedy: Validate all fields in form (by default it stops after finding the first invalid field with synchronous validation)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-form", children, **kwargs)
        self._attr_names += [
            "autofocus",
            "no_error_focus",
            "no_reset_focus",
            "greedy",
        ]
        self._event_names += [
            "submit",
            "reset",
            "validation_success",
            "validation_error",
        ]


class QFormChildMixin(HtmlElement):
    """
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-form-child-mixin", children, **kwargs)
        self._attr_names += [
        ]
        self._event_names += [
        ]


class QHeader(HtmlElement):
    """
    Properties

    :param model_value: Model of the component defining if it is shown or hidden to the user; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param reveal: Enable 'reveal' mode; Takes into account user scroll to temporarily show/hide header
    :param reveal_offset: Amount of scroll (in pixels) that should trigger a 'reveal' state change
    :param bordered: Applies a default border to the component
    :param elevated: Adds a default shadow to the header
    :param height_hint: When using SSR, you can optionally hint of the height (in pixels) of the QHeader

    Events

    :param model_value: Model of the component defining if it is shown or hidden to the user; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param reveal: Enable 'reveal' mode; Takes into account user scroll to temporarily show/hide header
    :param reveal_offset: Amount of scroll (in pixels) that should trigger a 'reveal' state change
    :param bordered: Applies a default border to the component
    :param elevated: Adds a default shadow to the header
    :param height_hint: When using SSR, you can optionally hint of the height (in pixels) of the QHeader
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-header", children, **kwargs)
        self._attr_names += [
            "model_value",
            "reveal",
            "reveal_offset",
            "bordered",
            "elevated",
            "height_hint",
        ]
        self._event_names += [
            "reveal",
        ]


class QIcon(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param tag: HTML tag to render, unless no icon is supplied or it's an svg icon
    :param name: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param color: Color name for component from the Quasar Color Palette
    :param left: Useful if icon is on the left side of something: applies a standard margin on the right side of Icon
    :param right: Useful if icon is on the right side of something: applies a standard margin on the left side of Icon

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param tag: HTML tag to render, unless no icon is supplied or it's an svg icon
    :param name: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param color: Color name for component from the Quasar Color Palette
    :param left: Useful if icon is on the left side of something: applies a standard margin on the right side of Icon
    :param right: Useful if icon is on the right side of something: applies a standard margin on the left side of Icon
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-icon", children, **kwargs)
        self._attr_names += [
            "size",
            "tag",
            "name",
            "color",
            "left",
            "right",
        ]
        self._event_names += [
        ]


class QImg(HtmlElement):
    """
    Properties

    :param ratio: Force the component to maintain an aspect ratio
    :param src: Path to image
    :param srcset: Same syntax as <img> srcset attribute
    :param sizes: Same syntax as <img> sizes attribute
    :param placeholder_src: While waiting for your image to load, you can use a placeholder image
    :param initial_ratio: Use it when not specifying 'ratio' but still wanting an initial aspect ratio
    :param width: Forces image width; Must also include the unit (px or %)
    :param height: Forces image height; Must also include the unit (px or %)
    :param loading: Lazy or immediate load; Same syntax as <img> loading attribute
    :param crossorigin: Same syntax as <img> crossorigin attribute
    :param decoding: Same syntax as <img> decoding attribute
    :param referrerpolicy: Same syntax as <img> referrerpolicy attribute
    :param fetchpriority: Provides a hint of the relative priority to use when fetching the image
    :param fit: How the image will fit into the container; Equivalent of the object-fit prop; Can be coordinated with 'position' prop
    :param position: The alignment of the image into the container; Equivalent of the object-position CSS prop
    :param alt: Specifies an alternate text for the image, if the image cannot be displayed
    :param draggable: Adds the native 'draggable' attribute
    :param img_class: CSS classes to be attributed to the native img element
    :param img_style: Apply CSS to the native img element
    :param spinner_color: Color name for default Spinner (unless using a 'loading' slot)
    :param spinner_size: Size in CSS units, including unit name, for default Spinner (unless using a 'loading' slot)
    :param no_spinner: Do not display the default spinner while waiting for the image to be loaded; It is overriden by the 'loading' slot when one is present
    :param no_native_menu: Disables the native context menu for the image
    :param no_transition: Disable default transition when switching between old and new image

    Events

    :param ratio: Force the component to maintain an aspect ratio
    :param src: Path to image
    :param srcset: Same syntax as <img> srcset attribute
    :param sizes: Same syntax as <img> sizes attribute
    :param placeholder_src: While waiting for your image to load, you can use a placeholder image
    :param initial_ratio: Use it when not specifying 'ratio' but still wanting an initial aspect ratio
    :param width: Forces image width; Must also include the unit (px or %)
    :param height: Forces image height; Must also include the unit (px or %)
    :param loading: Lazy or immediate load; Same syntax as <img> loading attribute
    :param crossorigin: Same syntax as <img> crossorigin attribute
    :param decoding: Same syntax as <img> decoding attribute
    :param referrerpolicy: Same syntax as <img> referrerpolicy attribute
    :param fetchpriority: Provides a hint of the relative priority to use when fetching the image
    :param fit: How the image will fit into the container; Equivalent of the object-fit prop; Can be coordinated with 'position' prop
    :param position: The alignment of the image into the container; Equivalent of the object-position CSS prop
    :param alt: Specifies an alternate text for the image, if the image cannot be displayed
    :param draggable: Adds the native 'draggable' attribute
    :param img_class: CSS classes to be attributed to the native img element
    :param img_style: Apply CSS to the native img element
    :param spinner_color: Color name for default Spinner (unless using a 'loading' slot)
    :param spinner_size: Size in CSS units, including unit name, for default Spinner (unless using a 'loading' slot)
    :param no_spinner: Do not display the default spinner while waiting for the image to be loaded; It is overriden by the 'loading' slot when one is present
    :param no_native_menu: Disables the native context menu for the image
    :param no_transition: Disable default transition when switching between old and new image
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-img", children, **kwargs)
        self._attr_names += [
            "ratio",
            "src",
            "srcset",
            "sizes",
            "placeholder_src",
            "initial_ratio",
            "width",
            "height",
            "loading",
            "crossorigin",
            "decoding",
            "referrerpolicy",
            "fetchpriority",
            "fit",
            "position",
            "alt",
            "draggable",
            "img_class",
            "img_style",
            "spinner_color",
            "spinner_size",
            "no_spinner",
            "no_native_menu",
            "no_transition",
        ]
        self._event_names += [
            "load",
            "error",
        ]


class QInfiniteScroll(HtmlElement):
    """
    Properties

    :param offset: Offset (pixels) to bottom of Infinite Scroll container from which the component should start loading more content in advance
    :param debounce: Debounce amount (in milliseconds)
    :param initial_index: Initialize the pagination index (used for the @load event)
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    :param disable: Put component in disabled mode
    :param reverse: Scroll area should behave like a messenger - starting scrolled to bottom and loading when reaching the top

    Events

    :param offset: Offset (pixels) to bottom of Infinite Scroll container from which the component should start loading more content in advance
    :param debounce: Debounce amount (in milliseconds)
    :param initial_index: Initialize the pagination index (used for the @load event)
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    :param disable: Put component in disabled mode
    :param reverse: Scroll area should behave like a messenger - starting scrolled to bottom and loading when reaching the top
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-infinite-scroll", children, **kwargs)
        self._attr_names += [
            "offset",
            "debounce",
            "initial_index",
            "scroll_target",
            "disable",
            "reverse",
        ]
        self._event_names += [
            "load",
        ]


class QInnerLoading(HtmlElement):
    """
    Properties

    :param transition_show: One of Quasar's embedded transitions
    :param transition_hide: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param size: Size in CSS units, including unit name, or standard size name (xs|sm|md|lg|xl), for the inner Spinner (unless using the default slot)
    :param showing: State - loading or not
    :param color: Color name for component from the Quasar Color Palette for the inner Spinner (unless using the default slot)
    :param label: Add a label; Gets overriden when using the default slot
    :param label_class: Add CSS class(es) to the label; Works along the 'label' prop only
    :param label_style: Apply custom style to the label; Works along the 'label' prop only
    :param dark: Notify the component that the background is a dark color

    Events

    :param transition_show: One of Quasar's embedded transitions
    :param transition_hide: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param size: Size in CSS units, including unit name, or standard size name (xs|sm|md|lg|xl), for the inner Spinner (unless using the default slot)
    :param showing: State - loading or not
    :param color: Color name for component from the Quasar Color Palette for the inner Spinner (unless using the default slot)
    :param label: Add a label; Gets overriden when using the default slot
    :param label_class: Add CSS class(es) to the label; Works along the 'label' prop only
    :param label_style: Apply custom style to the label; Works along the 'label' prop only
    :param dark: Notify the component that the background is a dark color
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-inner-loading", children, **kwargs)
        self._attr_names += [
            "transition_show",
            "transition_hide",
            "transition_duration",
            "size",
            "showing",
            "color",
            "label",
            "label_class",
            "label_style",
            "dark",
        ]
        self._event_names += [
        ]


class QInput(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms; If not specified, it takes the value of 'for' prop, if it exists
    :param mask: Custom mask or one of the predefined mask names
    :param fill_mask: Fills string with specified characters (or underscore if value is not string) to fill mask's length
    :param reverse_fill_mask: Fills string from the right side of the mask
    :param unmasked_value: Model will be unmasked (won't contain tokens/separation characters)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param error: Does field have validation errors?
    :param error_message: Validation error message (gets displayed only if 'error' is set to 'true')
    :param no_error_icon: Hide error icon when there is an error
    :param rules: Array of Functions/Strings; If String, then it must be a name of one of the embedded validation rules
    :param reactive_rules: By default a change in the rules does not trigger a new validation until the model changes; If set to true then a change in the rules will trigger a validation; Has a performance penalty, so use it only when you really need it
    :param lazy_rules: If set to boolean true then it checks validation status against the 'rules' only after field loses focus for first time; If set to 'ondemand' then it will trigger only when component's validate() method is manually called or when the wrapper QForm submits itself
    :param label: A text label that will “float” up above the input field, once the field gets focus
    :param stack_label: Label will be always shown above the field regardless of field content (if any)
    :param hint: Helper (hint) text which gets placed below your wrapped form component
    :param hide_hint: Hide the helper (hint) text when field doesn't have focus
    :param prefix: Prefix
    :param suffix: Suffix
    :param label_color: Color name for the label from the Quasar Color Palette; Overrides the 'color' prop; The difference from 'color' prop is that the label will always have this color, even when field is not focused
    :param color: Color name for component from the Quasar Color Palette
    :param bg_color: Color name for component from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param loading: Signals the user a process is in progress by displaying a spinner; Spinner can be customized by using the 'loading' slot.
    :param clearable: Appends clearable icon when a value (not undefined or null) is set; When clicked, model becomes null
    :param clear_icon: Custom icon to use for the clear button when using along with 'clearable' prop
    :param filled: Use 'filled' design for the field
    :param outlined: Use 'outlined' design for the field
    :param borderless: Use 'borderless' design for the field
    :param standout: Use 'standout' design for the field; Specifies classes to be applied when focused (overriding default ones)
    :param label_slot: Enables label slot; You need to set it to force use of the 'label' slot if the 'label' prop is not set
    :param bottom_slots: Enables bottom slots ('error', 'hint', 'counter')
    :param hide_bottom_space: Do not reserve space for hint/error/counter anymore when these are not used; As a result, it also disables the animation for those; It also allows the hint/error area to stretch vertically based on its content
    :param counter: Show an automatic counter on bottom right
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param square: Remove border-radius so borders are squared; Overrides 'rounded' prop
    :param dense: Dense mode; occupies less space
    :param item_aligned: Match inner content alignment to that of QItem
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param autofocus: Focus field on initial component render
    :param for: Used to specify the 'id' of the control and also the 'for' attribute of the label that wraps it; If no 'name' prop is specified, then it is used for this attribute as well
    :param shadow_text: Text to be displayed as shadow at the end of the text in the control; Does NOT applies to type=file
    :param type: Input type
    :param debounce: Debounce amount (in milliseconds) when updating model
    :param maxlength: Specify a max length of model
    :param autogrow: Make field autogrow along with its content (uses a textarea)
    :param input_class: Class definitions to be attributed to the underlying input tag
    :param input_style: Style definitions to be attributed to the underlying input tag

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms; If not specified, it takes the value of 'for' prop, if it exists
    :param mask: Custom mask or one of the predefined mask names
    :param fill_mask: Fills string with specified characters (or underscore if value is not string) to fill mask's length
    :param reverse_fill_mask: Fills string from the right side of the mask
    :param unmasked_value: Model will be unmasked (won't contain tokens/separation characters)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param error: Does field have validation errors?
    :param error_message: Validation error message (gets displayed only if 'error' is set to 'true')
    :param no_error_icon: Hide error icon when there is an error
    :param rules: Array of Functions/Strings; If String, then it must be a name of one of the embedded validation rules
    :param reactive_rules: By default a change in the rules does not trigger a new validation until the model changes; If set to true then a change in the rules will trigger a validation; Has a performance penalty, so use it only when you really need it
    :param lazy_rules: If set to boolean true then it checks validation status against the 'rules' only after field loses focus for first time; If set to 'ondemand' then it will trigger only when component's validate() method is manually called or when the wrapper QForm submits itself
    :param label: A text label that will “float” up above the input field, once the field gets focus
    :param stack_label: Label will be always shown above the field regardless of field content (if any)
    :param hint: Helper (hint) text which gets placed below your wrapped form component
    :param hide_hint: Hide the helper (hint) text when field doesn't have focus
    :param prefix: Prefix
    :param suffix: Suffix
    :param label_color: Color name for the label from the Quasar Color Palette; Overrides the 'color' prop; The difference from 'color' prop is that the label will always have this color, even when field is not focused
    :param color: Color name for component from the Quasar Color Palette
    :param bg_color: Color name for component from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param loading: Signals the user a process is in progress by displaying a spinner; Spinner can be customized by using the 'loading' slot.
    :param clearable: Appends clearable icon when a value (not undefined or null) is set; When clicked, model becomes null
    :param clear_icon: Custom icon to use for the clear button when using along with 'clearable' prop
    :param filled: Use 'filled' design for the field
    :param outlined: Use 'outlined' design for the field
    :param borderless: Use 'borderless' design for the field
    :param standout: Use 'standout' design for the field; Specifies classes to be applied when focused (overriding default ones)
    :param label_slot: Enables label slot; You need to set it to force use of the 'label' slot if the 'label' prop is not set
    :param bottom_slots: Enables bottom slots ('error', 'hint', 'counter')
    :param hide_bottom_space: Do not reserve space for hint/error/counter anymore when these are not used; As a result, it also disables the animation for those; It also allows the hint/error area to stretch vertically based on its content
    :param counter: Show an automatic counter on bottom right
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param square: Remove border-radius so borders are squared; Overrides 'rounded' prop
    :param dense: Dense mode; occupies less space
    :param item_aligned: Match inner content alignment to that of QItem
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param autofocus: Focus field on initial component render
    :param for: Used to specify the 'id' of the control and also the 'for' attribute of the label that wraps it; If no 'name' prop is specified, then it is used for this attribute as well
    :param shadow_text: Text to be displayed as shadow at the end of the text in the control; Does NOT applies to type=file
    :param type: Input type
    :param debounce: Debounce amount (in milliseconds) when updating model
    :param maxlength: Specify a max length of model
    :param autogrow: Make field autogrow along with its content (uses a textarea)
    :param input_class: Class definitions to be attributed to the underlying input tag
    :param input_style: Style definitions to be attributed to the underlying input tag
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-input", children, **kwargs)
        self._attr_names += [
            "name",
            "mask",
            "fill_mask",
            "reverse_fill_mask",
            "unmasked_value",
            "model_value",
            "error",
            "error_message",
            "no_error_icon",
            "rules",
            "reactive_rules",
            "lazy_rules",
            "label",
            "stack_label",
            "hint",
            "hide_hint",
            "prefix",
            "suffix",
            "label_color",
            "color",
            "bg_color",
            "dark",
            "loading",
            "clearable",
            "clear_icon",
            "filled",
            "outlined",
            "borderless",
            "standout",
            "label_slot",
            "bottom_slots",
            "hide_bottom_space",
            "counter",
            "rounded",
            "square",
            "dense",
            "item_aligned",
            "disable",
            "readonly",
            "autofocus",
            "for",
            "shadow_text",
            "type",
            "debounce",
            "maxlength",
            "autogrow",
            "input_class",
            "input_style",
        ]
        self._event_names += [
            "clear",
            ("update_model_value", "update:model-value"),
            "focus",
            "blur",
        ]


class QIntersection(HtmlElement):
    """
    Properties

    :param tag: HTML tag to use
    :param once: Get triggered only once
    :param ssr_prerender: Pre-render content on server side if using SSR (use it to pre-render above the fold content)
    :param root: [Intersection API root prop] Lets you define an alternative to the viewport as your root (through its DOM element); It is important to keep in mind that root needs to be an ancestor of the observed element
    :param margin: [Intersection API rootMargin prop] Allows you to specify the margins for the root, effectively allowing you to either grow or shrink the area used for intersections
    :param threshold: [Intersection API threshold prop] Threshold(s) at which to trigger, specified as a ratio, or list of ratios, of (visible area / total area) of the observed element
    :param transition: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param disable: Disable visibility observable (content will remain as it was, visible or hidden)

    Events

    :param tag: HTML tag to use
    :param once: Get triggered only once
    :param ssr_prerender: Pre-render content on server side if using SSR (use it to pre-render above the fold content)
    :param root: [Intersection API root prop] Lets you define an alternative to the viewport as your root (through its DOM element); It is important to keep in mind that root needs to be an ancestor of the observed element
    :param margin: [Intersection API rootMargin prop] Allows you to specify the margins for the root, effectively allowing you to either grow or shrink the area used for intersections
    :param threshold: [Intersection API threshold prop] Threshold(s) at which to trigger, specified as a ratio, or list of ratios, of (visible area / total area) of the observed element
    :param transition: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param disable: Disable visibility observable (content will remain as it was, visible or hidden)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-intersection", children, **kwargs)
        self._attr_names += [
            "tag",
            "once",
            "ssr_prerender",
            "root",
            "margin",
            "threshold",
            "transition",
            "transition_duration",
            "disable",
        ]
        self._event_names += [
            "visibility",
        ]


class QItem(HtmlElement):
    """
    Properties

    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param exact: Equivalent to Vue Router <router-link> 'exact' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param exact_active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param target: Native <a> link target attribute; Use it only along with 'href' prop; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param disable: Put component in disabled mode
    :param active: Put item into 'active' state
    :param dark: Notify the component that the background is a dark color
    :param clickable: Is QItem clickable? If it's the case, then it will add hover effects and emit 'click' events
    :param dense: Dense mode; occupies less space
    :param inset_level: Apply an inset; Useful when avatar/left side is missing but you want to align content with other items that do have a left side, or when you're building a menu
    :param tabindex: Tabindex HTML attribute value
    :param tag: HTML tag to render; Suggestion: use 'label' when encapsulating a QCheckbox/QRadio/QToggle so that when user clicks/taps on the whole item it will trigger a model change for the mentioned components
    :param manual_focus: Put item into a manual focus state; Enables 'focused' prop which will determine if item is focused or not, rather than relying on native hover/focus states
    :param focused: Determines focus state, ONLY if 'manual-focus' is enabled / set to true

    Events

    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param exact: Equivalent to Vue Router <router-link> 'exact' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param exact_active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param target: Native <a> link target attribute; Use it only along with 'href' prop; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param disable: Put component in disabled mode
    :param active: Put item into 'active' state
    :param dark: Notify the component that the background is a dark color
    :param clickable: Is QItem clickable? If it's the case, then it will add hover effects and emit 'click' events
    :param dense: Dense mode; occupies less space
    :param inset_level: Apply an inset; Useful when avatar/left side is missing but you want to align content with other items that do have a left side, or when you're building a menu
    :param tabindex: Tabindex HTML attribute value
    :param tag: HTML tag to render; Suggestion: use 'label' when encapsulating a QCheckbox/QRadio/QToggle so that when user clicks/taps on the whole item it will trigger a model change for the mentioned components
    :param manual_focus: Put item into a manual focus state; Enables 'focused' prop which will determine if item is focused or not, rather than relying on native hover/focus states
    :param focused: Determines focus state, ONLY if 'manual-focus' is enabled / set to true
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-item", children, **kwargs)
        self._attr_names += [
            "to",
            "exact",
            "replace",
            "active_class",
            "exact_active_class",
            "href",
            "target",
            "disable",
            "active",
            "dark",
            "clickable",
            "dense",
            "inset_level",
            "tabindex",
            "tag",
            "manual_focus",
            "focused",
        ]
        self._event_names += [
            "click",
        ]


class QItemLabel(HtmlElement):
    """
    Properties

    :param overline: Renders an overline label
    :param caption: Renders a caption label
    :param header: Renders a header label
    :param lines: Apply ellipsis when there's not enough space to render on the specified number of lines;

    Events

    :param overline: Renders an overline label
    :param caption: Renders a caption label
    :param header: Renders a header label
    :param lines: Apply ellipsis when there's not enough space to render on the specified number of lines;
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-item-label", children, **kwargs)
        self._attr_names += [
            "overline",
            "caption",
            "header",
            "lines",
        ]
        self._event_names += [
        ]


class QItemSection(HtmlElement):
    """
    Properties

    :param avatar: Render an avatar item side (does not needs 'side' prop to be set)
    :param thumbnail: Render a thumbnail item side (does not needs 'side' prop to be set)
    :param side: Renders as a side of the item
    :param top: Align content to top (useful for multi-line items)
    :param no_wrap: Do not wrap text (useful for item's main content)

    Events

    :param avatar: Render an avatar item side (does not needs 'side' prop to be set)
    :param thumbnail: Render a thumbnail item side (does not needs 'side' prop to be set)
    :param side: Renders as a side of the item
    :param top: Align content to top (useful for multi-line items)
    :param no_wrap: Do not wrap text (useful for item's main content)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-item-section", children, **kwargs)
        self._attr_names += [
            "avatar",
            "thumbnail",
            "side",
            "top",
            "no_wrap",
        ]
        self._event_names += [
        ]


class QKnob(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Any number to indicate the given value of the knob. Either use this property (along with a listener for 'update:modelValue' event) OR use the v-model directive
    :param min: The minimum value that the model (the knob value) should start at
    :param max: The maximum value that the model (the knob value) should go to
    :param inner_min: Inner minimum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be higher or equal to 'min' prop; Defaults to 'min' prop
    :param inner_max: Inner maximum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be lower or equal to 'max' prop; Defaults to 'max' prop
    :param step: A number representing steps in the value of the model, while adjusting the knob
    :param reverse: Reverses the direction of progress
    :param instant_feedback: No animation when model changes
    :param color: Color name for component from the Quasar Color Palette
    :param center_color: Color name for the center part of the component from the Quasar Color Palette
    :param track_color: Color name for the track of the component from the Quasar Color Palette
    :param font_size: Size of text in CSS units, including unit name. Suggestion: use 'em' units to sync with component size
    :param thickness: Thickness of progress arc as a ratio (0.0 < x < 1.0) of component size
    :param angle: Angle to rotate progress arc by
    :param show_value: Enables the default slot and uses it (if available), otherwise it displays the 'value' prop as text; Make sure the text has enough space to be displayed inside the component
    :param tabindex: Tabindex HTML attribute value
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Any number to indicate the given value of the knob. Either use this property (along with a listener for 'update:modelValue' event) OR use the v-model directive
    :param min: The minimum value that the model (the knob value) should start at
    :param max: The maximum value that the model (the knob value) should go to
    :param inner_min: Inner minimum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be higher or equal to 'min' prop; Defaults to 'min' prop
    :param inner_max: Inner maximum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be lower or equal to 'max' prop; Defaults to 'max' prop
    :param step: A number representing steps in the value of the model, while adjusting the knob
    :param reverse: Reverses the direction of progress
    :param instant_feedback: No animation when model changes
    :param color: Color name for component from the Quasar Color Palette
    :param center_color: Color name for the center part of the component from the Quasar Color Palette
    :param track_color: Color name for the track of the component from the Quasar Color Palette
    :param font_size: Size of text in CSS units, including unit name. Suggestion: use 'em' units to sync with component size
    :param thickness: Thickness of progress arc as a ratio (0.0 < x < 1.0) of component size
    :param angle: Angle to rotate progress arc by
    :param show_value: Enables the default slot and uses it (if available), otherwise it displays the 'value' prop as text; Make sure the text has enough space to be displayed inside the component
    :param tabindex: Tabindex HTML attribute value
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-knob", children, **kwargs)
        self._attr_names += [
            "name",
            "size",
            "model_value",
            "min",
            "max",
            "inner_min",
            "inner_max",
            "step",
            "reverse",
            "instant_feedback",
            "color",
            "center_color",
            "track_color",
            "font_size",
            "thickness",
            "angle",
            "show_value",
            "tabindex",
            "disable",
            "readonly",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "change",
            "drag_value",
        ]


class QLayout(HtmlElement):
    """
    Properties

    :param view: Defines how your layout components (header/footer/drawer) should be placed on screen; See docs examples
    :param container: Containerize the layout which means it changes the default behavior of expanding to the whole window; Useful (but not limited to) for when using on a QDialog

    Events

    :param view: Defines how your layout components (header/footer/drawer) should be placed on screen; See docs examples
    :param container: Containerize the layout which means it changes the default behavior of expanding to the whole window; Useful (but not limited to) for when using on a QDialog
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-layout", children, **kwargs)
        self._attr_names += [
            "view",
            "container",
        ]
        self._event_names += [
            "resize",
            "scroll",
            "scroll_height",
        ]


class QLinearProgress(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param value: Progress value (0.0 < x < 1.0)
    :param buffer: Optional buffer value (0.0 < x < 1.0)
    :param color: Color name for component from the Quasar Color Palette
    :param track_color: Color name for component's track from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param reverse: Reverse direction of progress
    :param stripe: Draw stripes; For determinate state only (for performance reasons)
    :param indeterminate: Put component into indeterminate mode
    :param query: Put component into query mode
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param instant_feedback: No transition when model changes
    :param animation_speed: Animation speed (in milliseconds, without unit)

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param value: Progress value (0.0 < x < 1.0)
    :param buffer: Optional buffer value (0.0 < x < 1.0)
    :param color: Color name for component from the Quasar Color Palette
    :param track_color: Color name for component's track from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param reverse: Reverse direction of progress
    :param stripe: Draw stripes; For determinate state only (for performance reasons)
    :param indeterminate: Put component into indeterminate mode
    :param query: Put component into query mode
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param instant_feedback: No transition when model changes
    :param animation_speed: Animation speed (in milliseconds, without unit)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-linear-progress", children, **kwargs)
        self._attr_names += [
            "size",
            "value",
            "buffer",
            "color",
            "track_color",
            "dark",
            "reverse",
            "stripe",
            "indeterminate",
            "query",
            "rounded",
            "instant_feedback",
            "animation_speed",
        ]
        self._event_names += [
        ]


class QList(HtmlElement):
    """
    Properties

    :param bordered: Applies a default border to the component
    :param dense: Dense mode; occupies less space
    :param separator: Applies a separator between contained items
    :param dark: Notify the component that the background is a dark color
    :param padding: Applies a material design-like padding on top and bottom
    :param tag: HTML tag to use

    Events

    :param bordered: Applies a default border to the component
    :param dense: Dense mode; occupies less space
    :param separator: Applies a separator between contained items
    :param dark: Notify the component that the background is a dark color
    :param padding: Applies a material design-like padding on top and bottom
    :param tag: HTML tag to use
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-list", children, **kwargs)
        self._attr_names += [
            "bordered",
            "dense",
            "separator",
            "dark",
            "padding",
            "tag",
        ]
        self._event_names += [
        ]


class QMarkupTable(HtmlElement):
    """
    Properties

    :param dense: Dense mode; occupies less space
    :param dark: Notify the component that the background is a dark color
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param square: Removes border-radius so borders are squared
    :param separator: Use a separator/border between rows, columns or all cells
    :param wrap_cells: Wrap text within table cells

    Events

    :param dense: Dense mode; occupies less space
    :param dark: Notify the component that the background is a dark color
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param square: Removes border-radius so borders are squared
    :param separator: Use a separator/border between rows, columns or all cells
    :param wrap_cells: Wrap text within table cells
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-markup-table", children, **kwargs)
        self._attr_names += [
            "dense",
            "dark",
            "flat",
            "bordered",
            "square",
            "separator",
            "wrap_cells",
        ]
        self._event_names += [
        ]


class QMenu(HtmlElement):
    """
    Properties

    :param transition_show: One of Quasar's embedded transitions
    :param transition_hide: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param target: Configure a target element to trigger component toggle; 'true' means it enables the parent DOM element, 'false' means it disables attaching events to any DOM elements; By using a String (CSS selector) or a DOM element it attaches the events to the specified DOM element (if it exists)
    :param no_parent_event: Skips attaching events to the target DOM element (that trigger the element to get shown)
    :param context_menu: Allows the component to behave like a context menu, which opens with a right mouse click (or long tap on mobile)
    :param model_value: Model of the component defining shown/hidden state; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param dark: Notify the component that the background is a dark color
    :param fit: Allows the menu to match at least the full width of its target
    :param cover: Allows the menu to cover its target. When used, the 'self' and 'fit' props are no longer effective
    :param anchor: Two values setting the starting position or anchor point of the menu relative to its target
    :param self: Two values setting the menu's own position relative to its target
    :param offset: An array of two numbers to offset the menu horizontally and vertically in pixels
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    :param touch_position: Allows for the target position to be set by the mouse position, when the target of the menu is either clicked or touched
    :param persistent: Allows the menu to not be dismissed by a click/tap outside of the menu or by hitting the ESC key
    :param no_route_dismiss: Changing route app won't dismiss the popup; No need to set it if 'persistent' prop is also set
    :param auto_close: Allows any click/tap in the menu to close it; Useful instead of attaching events to each menu item that should close the menu on click/tap
    :param separate_close_popup: Separate from parent menu, marking it as a separate closing point for v-close-popup (without this, chained menus close all together)
    :param square: Forces content to have squared borders
    :param no_refocus: (Accessibility) When Menu gets hidden, do not refocus on the DOM element that previously had focus
    :param no_focus: (Accessibility) When Menu gets shown, do not switch focus on it
    :param max_height: The maximum height of the menu; Size in CSS units, including unit name
    :param max_width: The maximum width of the menu; Size in CSS units, including unit name

    Events

    :param transition_show: One of Quasar's embedded transitions
    :param transition_hide: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param target: Configure a target element to trigger component toggle; 'true' means it enables the parent DOM element, 'false' means it disables attaching events to any DOM elements; By using a String (CSS selector) or a DOM element it attaches the events to the specified DOM element (if it exists)
    :param no_parent_event: Skips attaching events to the target DOM element (that trigger the element to get shown)
    :param context_menu: Allows the component to behave like a context menu, which opens with a right mouse click (or long tap on mobile)
    :param model_value: Model of the component defining shown/hidden state; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param dark: Notify the component that the background is a dark color
    :param fit: Allows the menu to match at least the full width of its target
    :param cover: Allows the menu to cover its target. When used, the 'self' and 'fit' props are no longer effective
    :param anchor: Two values setting the starting position or anchor point of the menu relative to its target
    :param self: Two values setting the menu's own position relative to its target
    :param offset: An array of two numbers to offset the menu horizontally and vertically in pixels
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    :param touch_position: Allows for the target position to be set by the mouse position, when the target of the menu is either clicked or touched
    :param persistent: Allows the menu to not be dismissed by a click/tap outside of the menu or by hitting the ESC key
    :param no_route_dismiss: Changing route app won't dismiss the popup; No need to set it if 'persistent' prop is also set
    :param auto_close: Allows any click/tap in the menu to close it; Useful instead of attaching events to each menu item that should close the menu on click/tap
    :param separate_close_popup: Separate from parent menu, marking it as a separate closing point for v-close-popup (without this, chained menus close all together)
    :param square: Forces content to have squared borders
    :param no_refocus: (Accessibility) When Menu gets hidden, do not refocus on the DOM element that previously had focus
    :param no_focus: (Accessibility) When Menu gets shown, do not switch focus on it
    :param max_height: The maximum height of the menu; Size in CSS units, including unit name
    :param max_width: The maximum width of the menu; Size in CSS units, including unit name
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-menu", children, **kwargs)
        self._attr_names += [
            "transition_show",
            "transition_hide",
            "transition_duration",
            "target",
            "no_parent_event",
            "context_menu",
            "model_value",
            "dark",
            "fit",
            "cover",
            "anchor",
            "self",
            "offset",
            "scroll_target",
            "touch_position",
            "persistent",
            "no_route_dismiss",
            "auto_close",
            "separate_close_popup",
            "square",
            "no_refocus",
            "no_focus",
            "max_height",
            "max_width",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "show",
            "before_show",
            "hide",
            "before_hide",
            "escape_key",
        ]


class QNoSsr(HtmlElement):
    """
    Properties

    :param tag: HTML tag to use
    :param placeholder: Text to display on server-side render (unless using 'placeholder' slot)

    Events

    :param tag: HTML tag to use
    :param placeholder: Text to display on server-side render (unless using 'placeholder' slot)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-no-ssr", children, **kwargs)
        self._attr_names += [
            "tag",
            "placeholder",
        ]
        self._event_names += [
        ]


class QOptionGroup(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param options: Array of objects with value, label, and disable (optional) props. The binary components will be created according to this array; Props from QToggle, QCheckbox or QRadio can also be added as key/value pairs to control the components singularly
    :param name: Used to specify the name of the controls; Useful if dealing with forms submitted directly to a URL
    :param type: The type of input component to be used
    :param color: Color name for component from the Quasar Color Palette
    :param keep_color: Should the color (if specified any) be kept when input components are unticked?
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param left_label: Label (if any specified) should be displayed on the left side of the input components
    :param inline: Show input components as inline-block rather than each having their own row
    :param disable: Put component in disabled mode

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param options: Array of objects with value, label, and disable (optional) props. The binary components will be created according to this array; Props from QToggle, QCheckbox or QRadio can also be added as key/value pairs to control the components singularly
    :param name: Used to specify the name of the controls; Useful if dealing with forms submitted directly to a URL
    :param type: The type of input component to be used
    :param color: Color name for component from the Quasar Color Palette
    :param keep_color: Should the color (if specified any) be kept when input components are unticked?
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param left_label: Label (if any specified) should be displayed on the left side of the input components
    :param inline: Show input components as inline-block rather than each having their own row
    :param disable: Put component in disabled mode
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-option-group", children, **kwargs)
        self._attr_names += [
            "size",
            "model_value",
            "options",
            "name",
            "type",
            "color",
            "keep_color",
            "dark",
            "dense",
            "left_label",
            "inline",
            "disable",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
        ]


class QPage(HtmlElement):
    """
    Properties

    :param padding: Applies a default responsive page padding
    :param style_fn: Override default CSS style applied to the component (sets minHeight); Function(offset: Number) => CSS props/value: Object; For best performance, reference it from your scope and do not define it inline

    Events

    :param padding: Applies a default responsive page padding
    :param style_fn: Override default CSS style applied to the component (sets minHeight); Function(offset: Number) => CSS props/value: Object; For best performance, reference it from your scope and do not define it inline
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-page", children, **kwargs)
        self._attr_names += [
            "padding",
            "style_fn",
        ]
        self._event_names += [
        ]


class QPageContainer(HtmlElement):
    """
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-page-container", children, **kwargs)
        self._attr_names += [
        ]
        self._event_names += [
        ]


class QPageScroller(HtmlElement):
    """
    Properties

    :param position: Page side/corner to stick to
    :param offset: An array of two numbers to offset the component horizontally and vertically in pixels
    :param expand: By default the component shrinks to content's size; By using this prop you make the component fully expand horizontally or vertically, based on 'position' prop
    :param scroll_offset: Scroll offset (in pixels) from which point the component is shown on page; Measured from the top of the page (or from the bottom if in 'reverse' mode)
    :param reverse: Work in reverse (shows when scrolling to the top of the page and scrolls to bottom when triggered)
    :param duration: Duration (in milliseconds) of the scrolling until it reaches its target

    Events

    :param position: Page side/corner to stick to
    :param offset: An array of two numbers to offset the component horizontally and vertically in pixels
    :param expand: By default the component shrinks to content's size; By using this prop you make the component fully expand horizontally or vertically, based on 'position' prop
    :param scroll_offset: Scroll offset (in pixels) from which point the component is shown on page; Measured from the top of the page (or from the bottom if in 'reverse' mode)
    :param reverse: Work in reverse (shows when scrolling to the top of the page and scrolls to bottom when triggered)
    :param duration: Duration (in milliseconds) of the scrolling until it reaches its target
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-page-scroller", children, **kwargs)
        self._attr_names += [
            "position",
            "offset",
            "expand",
            "scroll_offset",
            "reverse",
            "duration",
        ]
        self._event_names += [
        ]


class QPageSticky(HtmlElement):
    """
    Properties

    :param position: Page side/corner to stick to
    :param offset: An array of two numbers to offset the component horizontally and vertically in pixels
    :param expand: By default the component shrinks to content's size; By using this prop you make the component fully expand horizontally or vertically, based on 'position' prop

    Events

    :param position: Page side/corner to stick to
    :param offset: An array of two numbers to offset the component horizontally and vertically in pixels
    :param expand: By default the component shrinks to content's size; By using this prop you make the component fully expand horizontally or vertically, based on 'position' prop
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-page-sticky", children, **kwargs)
        self._attr_names += [
            "position",
            "offset",
            "expand",
        ]
        self._event_names += [
        ]


class QPagination(HtmlElement):
    """
    Properties

    :param model_value: Current page (must be between min/max)
    :param min: Minimum page (must be lower than 'max')
    :param max: Number of last page (must be higher than 'min')
    :param dark: Notify the component that the background is a dark color (useful when you are using it along with the 'input' prop)
    :param size: Button size in CSS units, including unit name
    :param disable: Put component in disabled mode
    :param input: Use an input instead of buttons
    :param icon_prev: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_next: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_first: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_last: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param to_fn: Generate link for page buttons; For best performance, reference it from your scope and do not define it inline
    :param boundary_links: Show boundary button links
    :param boundary_numbers: Always show first and last page buttons (if not using 'input')
    :param direction_links: Show direction buttons
    :param ellipses: Show ellipses (...) when pages are available
    :param max_pages: Maximum number of page links to display at a time; 0 means Infinite
    :param flat: Use 'flat' design for non-active buttons (it's the default option)
    :param outline: Use 'outline' design for non-active buttons
    :param unelevated: Remove shadow for non-active buttons
    :param push: Use 'push' design for non-active buttons
    :param color: Color name from the Quasar Color Palette for the non-active buttons
    :param text_color: Text color name from the Quasar Color Palette for the ACTIVE buttons
    :param active_design: The design of the ACTIVE button, similar to the flat/outline/push/unelevated props (but those are used for non-active buttons)
    :param active_color: Color name from the Quasar Color Palette for the ACTIVE button
    :param active_text_color: Text color name from the Quasar Color Palette for the ACTIVE button
    :param round: Makes a circle shaped button for all buttons
    :param rounded: Applies a more prominent border-radius for a squared shape button for all buttons
    :param glossy: Applies a glossy effect for all buttons
    :param gutter: Apply custom gutter; Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl)
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param input_style: Style definitions to be attributed to the input (if using one)
    :param input_class: Class definitions to be attributed to the input (if using one)
    :param ripple: Configure buttons material ripple (disable it by setting it to 'false' or supply a config object); Does not applies to boundary and ellipsis buttons

    Events

    :param model_value: Current page (must be between min/max)
    :param min: Minimum page (must be lower than 'max')
    :param max: Number of last page (must be higher than 'min')
    :param dark: Notify the component that the background is a dark color (useful when you are using it along with the 'input' prop)
    :param size: Button size in CSS units, including unit name
    :param disable: Put component in disabled mode
    :param input: Use an input instead of buttons
    :param icon_prev: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_next: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_first: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_last: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param to_fn: Generate link for page buttons; For best performance, reference it from your scope and do not define it inline
    :param boundary_links: Show boundary button links
    :param boundary_numbers: Always show first and last page buttons (if not using 'input')
    :param direction_links: Show direction buttons
    :param ellipses: Show ellipses (...) when pages are available
    :param max_pages: Maximum number of page links to display at a time; 0 means Infinite
    :param flat: Use 'flat' design for non-active buttons (it's the default option)
    :param outline: Use 'outline' design for non-active buttons
    :param unelevated: Remove shadow for non-active buttons
    :param push: Use 'push' design for non-active buttons
    :param color: Color name from the Quasar Color Palette for the non-active buttons
    :param text_color: Text color name from the Quasar Color Palette for the ACTIVE buttons
    :param active_design: The design of the ACTIVE button, similar to the flat/outline/push/unelevated props (but those are used for non-active buttons)
    :param active_color: Color name from the Quasar Color Palette for the ACTIVE button
    :param active_text_color: Text color name from the Quasar Color Palette for the ACTIVE button
    :param round: Makes a circle shaped button for all buttons
    :param rounded: Applies a more prominent border-radius for a squared shape button for all buttons
    :param glossy: Applies a glossy effect for all buttons
    :param gutter: Apply custom gutter; Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl)
    :param padding: Apply custom padding (vertical [horizontal]); Size in CSS units, including unit name or standard size name (none|xs|sm|md|lg|xl); Also removes the min width and height when set
    :param input_style: Style definitions to be attributed to the input (if using one)
    :param input_class: Class definitions to be attributed to the input (if using one)
    :param ripple: Configure buttons material ripple (disable it by setting it to 'false' or supply a config object); Does not applies to boundary and ellipsis buttons
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-pagination", children, **kwargs)
        self._attr_names += [
            "model_value",
            "min",
            "max",
            "dark",
            "size",
            "disable",
            "input",
            "icon_prev",
            "icon_next",
            "icon_first",
            "icon_last",
            "to_fn",
            "boundary_links",
            "boundary_numbers",
            "direction_links",
            "ellipses",
            "max_pages",
            "flat",
            "outline",
            "unelevated",
            "push",
            "color",
            "text_color",
            "active_design",
            "active_color",
            "active_text_color",
            "round",
            "rounded",
            "glossy",
            "gutter",
            "padding",
            "input_style",
            "input_class",
            "ripple",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
        ]


class QParallax(HtmlElement):
    """
    Properties

    :param src: Path to image (unless a 'media' slot is used)
    :param height: Height of component (in pixels)
    :param speed: Speed of parallax effect (0.0 < x < 1.0)
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one

    Events

    :param src: Path to image (unless a 'media' slot is used)
    :param height: Height of component (in pixels)
    :param speed: Speed of parallax effect (0.0 < x < 1.0)
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-parallax", children, **kwargs)
        self._attr_names += [
            "src",
            "height",
            "speed",
            "scroll_target",
        ]
        self._event_names += [
            "scroll",
        ]


class QPopupEdit(HtmlElement):
    """
    Properties

    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param title: Optional title (unless 'title' slot is used)
    :param buttons: Show Set and Cancel buttons
    :param label_set: Override Set button label
    :param label_cancel: Override Cancel button label
    :param auto_save: Automatically save the model (if changed) when user clicks/taps outside of the popup; It does not apply to ESC key
    :param color: Color name for component from the Quasar Color Palette
    :param validate: Validates model then triggers 'save' and closes Popup; Returns a Boolean ('true' means valid, 'false' means abort); Syntax: validate(value); For best performance, reference it from your scope and do not define it inline
    :param disable: Put component in disabled mode
    :param fit: Allows the menu to match at least the full width of its target
    :param cover: Allows the menu to cover its target. When used, the 'self' and 'fit' props are no longer effective
    :param anchor: Two values setting the starting position or anchor point of the menu relative to its target
    :param self: Two values setting the menu's own position relative to its target
    :param offset: An array of two numbers to offset the menu horizontally and vertically in pixels
    :param touch_position: Allows for the target position to be set by the mouse position, when the target of the menu is either clicked or touched
    :param persistent: Avoid menu closing by hitting ESC key or by clicking/tapping outside of the Popup
    :param separate_close_popup: Separate from parent menu, marking it as a separate closing point for v-close-popup (without this, chained menus close all together)
    :param square: Forces menu to have squared borders
    :param max_height: The maximum height of the menu; Size in CSS units, including unit name
    :param max_width: The maximum width of the menu; Size in CSS units, including unit name

    Events

    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param title: Optional title (unless 'title' slot is used)
    :param buttons: Show Set and Cancel buttons
    :param label_set: Override Set button label
    :param label_cancel: Override Cancel button label
    :param auto_save: Automatically save the model (if changed) when user clicks/taps outside of the popup; It does not apply to ESC key
    :param color: Color name for component from the Quasar Color Palette
    :param validate: Validates model then triggers 'save' and closes Popup; Returns a Boolean ('true' means valid, 'false' means abort); Syntax: validate(value); For best performance, reference it from your scope and do not define it inline
    :param disable: Put component in disabled mode
    :param fit: Allows the menu to match at least the full width of its target
    :param cover: Allows the menu to cover its target. When used, the 'self' and 'fit' props are no longer effective
    :param anchor: Two values setting the starting position or anchor point of the menu relative to its target
    :param self: Two values setting the menu's own position relative to its target
    :param offset: An array of two numbers to offset the menu horizontally and vertically in pixels
    :param touch_position: Allows for the target position to be set by the mouse position, when the target of the menu is either clicked or touched
    :param persistent: Avoid menu closing by hitting ESC key or by clicking/tapping outside of the Popup
    :param separate_close_popup: Separate from parent menu, marking it as a separate closing point for v-close-popup (without this, chained menus close all together)
    :param square: Forces menu to have squared borders
    :param max_height: The maximum height of the menu; Size in CSS units, including unit name
    :param max_width: The maximum width of the menu; Size in CSS units, including unit name
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-popup-edit", children, **kwargs)
        self._attr_names += [
            "model_value",
            "title",
            "buttons",
            "label_set",
            "label_cancel",
            "auto_save",
            "color",
            "validate",
            "disable",
            "fit",
            "cover",
            "anchor",
            "self",
            "offset",
            "touch_position",
            "persistent",
            "separate_close_popup",
            "square",
            "max_height",
            "max_width",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "before_show",
            "show",
            "before_hide",
            "hide",
            "save",
            "cancel",
        ]


class QPopupProxy(HtmlElement):
    """
    Properties

    :param target: Configure a target element to trigger component toggle; 'true' means it enables the parent DOM element, 'false' means it disables attaching events to any DOM elements; By using a String (CSS selector) or a DOM element it attaches the events to the specified DOM element (if it exists)
    :param no_parent_event: Skips attaching events to the target DOM element (that trigger the element to get shown)
    :param context_menu: Allows the component to behave like a context menu, which opens with a right mouse click (or long tap on mobile)
    :param model_value: Defines the state of the component (shown/hidden); Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param breakpoint: Breakpoint (in pixels) of window width/height (whichever is smaller) from where a Menu will get to be used instead of a Dialog

    Events

    :param target: Configure a target element to trigger component toggle; 'true' means it enables the parent DOM element, 'false' means it disables attaching events to any DOM elements; By using a String (CSS selector) or a DOM element it attaches the events to the specified DOM element (if it exists)
    :param no_parent_event: Skips attaching events to the target DOM element (that trigger the element to get shown)
    :param context_menu: Allows the component to behave like a context menu, which opens with a right mouse click (or long tap on mobile)
    :param model_value: Defines the state of the component (shown/hidden); Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param breakpoint: Breakpoint (in pixels) of window width/height (whichever is smaller) from where a Menu will get to be used instead of a Dialog
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-popup-proxy", children, **kwargs)
        self._attr_names += [
            "target",
            "no_parent_event",
            "context_menu",
            "model_value",
            "breakpoint",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "before_show",
            "show",
            "before_hide",
            "hide",
        ]


class QPullToRefresh(HtmlElement):
    """
    Properties

    :param color: Color name for the icon from the Quasar Color Palette
    :param bg_color: Color name for background of the icon container from the Quasar Color Palette
    :param icon: Icon to display when refreshing the content
    :param no_mouse: Don't listen for mouse events
    :param disable: Put component in disabled mode
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one

    Events

    :param color: Color name for the icon from the Quasar Color Palette
    :param bg_color: Color name for background of the icon container from the Quasar Color Palette
    :param icon: Icon to display when refreshing the content
    :param no_mouse: Don't listen for mouse events
    :param disable: Put component in disabled mode
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-pull-to-refresh", children, **kwargs)
        self._attr_names += [
            "color",
            "bg_color",
            "icon",
            "no_mouse",
            "disable",
            "scroll_target",
        ]
        self._event_names += [
            "refresh",
        ]


class QRadio(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param val: The actual value of the option with which model value is changed
    :param label: Label to display along the radio control (or use the default slot instead of this prop)
    :param left_label: Label (if any specified) should be displayed on the left side of the checkbox
    :param checked_icon: The icon to be used when selected (instead of the default design)
    :param unchecked_icon: The icon to be used when un-selected (instead of the default design)
    :param color: Color name for component from the Quasar Color Palette
    :param keep_color: Should the color (if specified any) be kept when checkbox is unticked?
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param disable: Put component in disabled mode
    :param tabindex: Tabindex HTML attribute value

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param val: The actual value of the option with which model value is changed
    :param label: Label to display along the radio control (or use the default slot instead of this prop)
    :param left_label: Label (if any specified) should be displayed on the left side of the checkbox
    :param checked_icon: The icon to be used when selected (instead of the default design)
    :param unchecked_icon: The icon to be used when un-selected (instead of the default design)
    :param color: Color name for component from the Quasar Color Palette
    :param keep_color: Should the color (if specified any) be kept when checkbox is unticked?
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param disable: Put component in disabled mode
    :param tabindex: Tabindex HTML attribute value
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-radio", children, **kwargs)
        self._attr_names += [
            "name",
            "size",
            "model_value",
            "val",
            "label",
            "left_label",
            "checked_icon",
            "unchecked_icon",
            "color",
            "keep_color",
            "dark",
            "dense",
            "disable",
            "tabindex",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
        ]


class QRange(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param min: Minimum value of the model; Set track's minimum value
    :param max: Maximum value of the model; Set track's maximum value
    :param inner_min: Inner minimum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be higher or equal to 'min' prop; Defaults to 'min' prop
    :param inner_max: Inner maximum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be lower or equal to 'max' prop; Defaults to 'max' prop
    :param step: Specify step amount between valid values (> 0.0); When step equals to 0 it defines infinite granularity
    :param snap: Snap on valid values, rather than sliding freely; Suggestion: use with 'step' prop
    :param reverse: Work in reverse (changes direction)
    :param vertical: Display in vertical direction
    :param color: Color name for component from the Quasar Color Palette
    :param track_color: Color name for the track (can be 'transparent' too) from the Quasar Color Palette
    :param track_img: Apply a pattern image on the track
    :param inner_track_color: Color name for the inner track (can be 'transparent' too) from the Quasar Color Palette
    :param inner_track_img: Apply a pattern image on the inner track
    :param selection_color: Color name for the selection bar (can be 'transparent' too) from the Quasar Color Palette
    :param selection_img: Apply a pattern image on the selection bar
    :param label: Popup a label when user clicks/taps on the slider thumb and moves it
    :param label_color: Color name for component from the Quasar Color Palette
    :param label_text_color: Color name for component from the Quasar Color Palette
    :param switch_label_side: Switch the position of the label (top <-> bottom or left <-> right)
    :param label_always: Always display the label
    :param markers: Display markers on the track, one for each possible value for the model or using a custom step (when specifying a Number)
    :param marker_labels: Configure the marker labels (or show the default ones if 'true'); Array of definition Objects or Object with key-value where key is the model and the value is the marker label definition
    :param marker_labels_class: CSS class(es) to apply to the marker labels container
    :param switch_marker_labels_side: Switch the position of the marker labels (top <-> bottom or left <-> right)
    :param track_size: Track size (including CSS unit)
    :param thumb_size: Thumb size (including CSS unit)
    :param thumb_color: Color name for component from the Quasar Color Palette
    :param thumb_path: Set custom thumb svg path
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param tabindex: Tabindex HTML attribute value
    :param model_value: Model of the component of type { min, max } (both values must be between global min/max); Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param drag_range: User can drag range instead of just the two thumbs
    :param drag_only_range: User can drag only the range instead and NOT the two thumbs
    :param left_label_color: Color name for left label background from the Quasar Color Palette
    :param left_label_text_color: Color name for left label text from the Quasar Color Palette
    :param right_label_color: Color name for right label background from the Quasar Color Palette
    :param right_label_text_color: Color name for right label text from the Quasar Color Palette
    :param left_label_value: Override default label for min value
    :param right_label_value: Override default label for max value
    :param left_thumb_color: Color name (from the Quasar Color Palette) for left thumb
    :param right_thumb_color: Color name (from the Quasar Color Palette) for right thumb

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param min: Minimum value of the model; Set track's minimum value
    :param max: Maximum value of the model; Set track's maximum value
    :param inner_min: Inner minimum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be higher or equal to 'min' prop; Defaults to 'min' prop
    :param inner_max: Inner maximum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be lower or equal to 'max' prop; Defaults to 'max' prop
    :param step: Specify step amount between valid values (> 0.0); When step equals to 0 it defines infinite granularity
    :param snap: Snap on valid values, rather than sliding freely; Suggestion: use with 'step' prop
    :param reverse: Work in reverse (changes direction)
    :param vertical: Display in vertical direction
    :param color: Color name for component from the Quasar Color Palette
    :param track_color: Color name for the track (can be 'transparent' too) from the Quasar Color Palette
    :param track_img: Apply a pattern image on the track
    :param inner_track_color: Color name for the inner track (can be 'transparent' too) from the Quasar Color Palette
    :param inner_track_img: Apply a pattern image on the inner track
    :param selection_color: Color name for the selection bar (can be 'transparent' too) from the Quasar Color Palette
    :param selection_img: Apply a pattern image on the selection bar
    :param label: Popup a label when user clicks/taps on the slider thumb and moves it
    :param label_color: Color name for component from the Quasar Color Palette
    :param label_text_color: Color name for component from the Quasar Color Palette
    :param switch_label_side: Switch the position of the label (top <-> bottom or left <-> right)
    :param label_always: Always display the label
    :param markers: Display markers on the track, one for each possible value for the model or using a custom step (when specifying a Number)
    :param marker_labels: Configure the marker labels (or show the default ones if 'true'); Array of definition Objects or Object with key-value where key is the model and the value is the marker label definition
    :param marker_labels_class: CSS class(es) to apply to the marker labels container
    :param switch_marker_labels_side: Switch the position of the marker labels (top <-> bottom or left <-> right)
    :param track_size: Track size (including CSS unit)
    :param thumb_size: Thumb size (including CSS unit)
    :param thumb_color: Color name for component from the Quasar Color Palette
    :param thumb_path: Set custom thumb svg path
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param tabindex: Tabindex HTML attribute value
    :param model_value: Model of the component of type { min, max } (both values must be between global min/max); Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param drag_range: User can drag range instead of just the two thumbs
    :param drag_only_range: User can drag only the range instead and NOT the two thumbs
    :param left_label_color: Color name for left label background from the Quasar Color Palette
    :param left_label_text_color: Color name for left label text from the Quasar Color Palette
    :param right_label_color: Color name for right label background from the Quasar Color Palette
    :param right_label_text_color: Color name for right label text from the Quasar Color Palette
    :param left_label_value: Override default label for min value
    :param right_label_value: Override default label for max value
    :param left_thumb_color: Color name (from the Quasar Color Palette) for left thumb
    :param right_thumb_color: Color name (from the Quasar Color Palette) for right thumb
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-range", children, **kwargs)
        self._attr_names += [
            "name",
            "min",
            "max",
            "inner_min",
            "inner_max",
            "step",
            "snap",
            "reverse",
            "vertical",
            "color",
            "track_color",
            "track_img",
            "inner_track_color",
            "inner_track_img",
            "selection_color",
            "selection_img",
            "label",
            "label_color",
            "label_text_color",
            "switch_label_side",
            "label_always",
            "markers",
            "marker_labels",
            "marker_labels_class",
            "switch_marker_labels_side",
            "track_size",
            "thumb_size",
            "thumb_color",
            "thumb_path",
            "dark",
            "dense",
            "disable",
            "readonly",
            "tabindex",
            "model_value",
            "drag_range",
            "drag_only_range",
            "left_label_color",
            "left_label_text_color",
            "right_label_color",
            "right_label_text_color",
            "left_label_value",
            "right_label_value",
            "left_thumb_color",
            "right_thumb_color",
        ]
        self._event_names += [
            "change",
            "pan",
            ("update_model_value", "update:model-value"),
        ]


class QRating(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param max: Number of icons to display
    :param icon: Icon name following Quasar convention; make sure you have the icon library installed unless you are using 'img:' prefix; If an array is provided each rating value will use the corresponding icon in the array (0 based)
    :param icon_selected: Icon name following Quasar convention to be used when selected (optional); make sure you have the icon library installed unless you are using 'img:' prefix; If an array is provided each rating value will use the corresponding icon in the array (0 based)
    :param icon_half: Icon name following Quasar convention to be used when selected (optional); make sure you have the icon library installed unless you are using 'img:' prefix; If an array is provided each rating value will use the corresponding icon in the array (0 based)
    :param icon_aria_label: Label to be set on aria-label for Icon; If an array is provided each rating value will use the corresponding aria-label in the array (0 based); If string value is provided the rating value will be appended; If not provided the name of the icon will be used
    :param color: Color name for component from the Quasar Color Palette; v1.5.0+: If an array is provided each rating value will use the corresponding color in the array (0 based)
    :param color_selected: Color name from the Quasar Palette for selected icons
    :param color_half: Color name from the Quasar Palette for half selected icons
    :param no_dimming: Does not lower opacity for unselected icons
    :param no_reset: When used, disables default behavior of clicking/tapping on icon which represents current model value to reset model to 0
    :param readonly: Put component in readonly mode
    :param disable: Put component in disabled mode

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param max: Number of icons to display
    :param icon: Icon name following Quasar convention; make sure you have the icon library installed unless you are using 'img:' prefix; If an array is provided each rating value will use the corresponding icon in the array (0 based)
    :param icon_selected: Icon name following Quasar convention to be used when selected (optional); make sure you have the icon library installed unless you are using 'img:' prefix; If an array is provided each rating value will use the corresponding icon in the array (0 based)
    :param icon_half: Icon name following Quasar convention to be used when selected (optional); make sure you have the icon library installed unless you are using 'img:' prefix; If an array is provided each rating value will use the corresponding icon in the array (0 based)
    :param icon_aria_label: Label to be set on aria-label for Icon; If an array is provided each rating value will use the corresponding aria-label in the array (0 based); If string value is provided the rating value will be appended; If not provided the name of the icon will be used
    :param color: Color name for component from the Quasar Color Palette; v1.5.0+: If an array is provided each rating value will use the corresponding color in the array (0 based)
    :param color_selected: Color name from the Quasar Palette for selected icons
    :param color_half: Color name from the Quasar Palette for half selected icons
    :param no_dimming: Does not lower opacity for unselected icons
    :param no_reset: When used, disables default behavior of clicking/tapping on icon which represents current model value to reset model to 0
    :param readonly: Put component in readonly mode
    :param disable: Put component in disabled mode
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-rating", children, **kwargs)
        self._attr_names += [
            "name",
            "size",
            "model_value",
            "max",
            "icon",
            "icon_selected",
            "icon_half",
            "icon_aria_label",
            "color",
            "color_selected",
            "color_half",
            "no_dimming",
            "no_reset",
            "readonly",
            "disable",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
        ]


class QResizeObserver(HtmlElement):
    """
    Properties

    :param debounce: Debounce amount (in milliseconds)

    Events

    :param debounce: Debounce amount (in milliseconds)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-resize-observer", children, **kwargs)
        self._attr_names += [
            "debounce",
        ]
        self._event_names += [
            "resize",
        ]


class QResponsive(HtmlElement):
    """
    Properties

    :param ratio: Aspect ratio for the content; If value is a String, then avoid using a computational statement (like '16/9') and instead specify the String value of the result directly (eg. '1.7777')

    Events

    :param ratio: Aspect ratio for the content; If value is a String, then avoid using a computational statement (like '16/9') and instead specify the String value of the result directly (eg. '1.7777')
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-responsive", children, **kwargs)
        self._attr_names += [
            "ratio",
        ]
        self._event_names += [
        ]


class QRouteTab(HtmlElement):
    """
    Properties

    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param exact: Equivalent to Vue Router <router-link> 'exact' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param exact_active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param target: Native <a> link target attribute; Use it only along with 'href' prop; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param disable: Put component in disabled mode
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param label: A number or string to label the tab
    :param alert: Adds an alert symbol to the tab, notifying the user there are some updates; If its value is not a Boolean, then you can specify a color
    :param alert_icon: Adds a floating icon to the tab, notifying the user there are some updates; It's displayed only if 'alert' is set; Can use the color specified by 'alert' prop
    :param name: Panel name
    :param no_caps: Turns off capitalizing all letters within the tab (which is the default)
    :param content_class: Class definitions to be attributed to the content wrapper
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param tabindex: Tabindex HTML attribute value

    Events

    :param to: Equivalent to Vue Router <router-link> 'to' property; Superseded by 'href' prop if used
    :param exact: Equivalent to Vue Router <router-link> 'exact' property; Superseded by 'href' prop if used
    :param replace: Equivalent to Vue Router <router-link> 'replace' property; Superseded by 'href' prop if used
    :param active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param exact_active_class: Equivalent to Vue Router <router-link> 'active-class' property; Superseded by 'href' prop if used
    :param href: Native <a> link href attribute; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param target: Native <a> link target attribute; Use it only along with 'href' prop; Has priority over the 'to'/'exact'/'replace'/'active-class'/'exact-active-class' props
    :param disable: Put component in disabled mode
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param label: A number or string to label the tab
    :param alert: Adds an alert symbol to the tab, notifying the user there are some updates; If its value is not a Boolean, then you can specify a color
    :param alert_icon: Adds a floating icon to the tab, notifying the user there are some updates; It's displayed only if 'alert' is set; Can use the color specified by 'alert' prop
    :param name: Panel name
    :param no_caps: Turns off capitalizing all letters within the tab (which is the default)
    :param content_class: Class definitions to be attributed to the content wrapper
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param tabindex: Tabindex HTML attribute value
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-route-tab", children, **kwargs)
        self._attr_names += [
            "to",
            "exact",
            "replace",
            "active_class",
            "exact_active_class",
            "href",
            "target",
            "disable",
            "icon",
            "label",
            "alert",
            "alert_icon",
            "name",
            "no_caps",
            "content_class",
            "ripple",
            "tabindex",
        ]
        self._event_names += [
            "click",
        ]


class QScrollArea(HtmlElement):
    """
    Properties

    :param dark: Notify the component that the background is a dark color
    :param bar_style: Object with CSS properties and values for custom styling the scrollbars (both vertical and horizontal)
    :param vertical_bar_style: Object with CSS properties and values for custom styling the vertical scrollbar; Is applied on top of 'bar-style' prop
    :param horizontal_bar_style: Object with CSS properties and values for custom styling the horizontal scrollbar; Is applied on top of 'bar-style' prop
    :param thumb_style: Object with CSS properties and values for custom styling the thumb of scrollbars (both vertical and horizontal)
    :param vertical_thumb_style: Object with CSS properties and values for custom styling the thumb of the vertical scrollbar; Is applied on top of 'thumb-style' prop
    :param horizontal_thumb_style: Object with CSS properties and values for custom styling the thumb of the horizontal scrollbar; Is applied on top of 'thumb-style' prop
    :param content_style: Object with CSS properties and values for styling the container of QScrollArea
    :param content_active_style: Object with CSS properties and values for styling the container of QScrollArea when scroll area becomes active (is mouse hovered)
    :param visible: Manually control the visibility of the scrollbar; Overrides default mouse over/leave behavior
    :param delay: When content changes, the scrollbar appears; this delay defines the amount of time (in milliseconds) before scrollbars disappear again (if component is not hovered)
    :param tabindex: Tabindex HTML attribute value

    Events

    :param dark: Notify the component that the background is a dark color
    :param bar_style: Object with CSS properties and values for custom styling the scrollbars (both vertical and horizontal)
    :param vertical_bar_style: Object with CSS properties and values for custom styling the vertical scrollbar; Is applied on top of 'bar-style' prop
    :param horizontal_bar_style: Object with CSS properties and values for custom styling the horizontal scrollbar; Is applied on top of 'bar-style' prop
    :param thumb_style: Object with CSS properties and values for custom styling the thumb of scrollbars (both vertical and horizontal)
    :param vertical_thumb_style: Object with CSS properties and values for custom styling the thumb of the vertical scrollbar; Is applied on top of 'thumb-style' prop
    :param horizontal_thumb_style: Object with CSS properties and values for custom styling the thumb of the horizontal scrollbar; Is applied on top of 'thumb-style' prop
    :param content_style: Object with CSS properties and values for styling the container of QScrollArea
    :param content_active_style: Object with CSS properties and values for styling the container of QScrollArea when scroll area becomes active (is mouse hovered)
    :param visible: Manually control the visibility of the scrollbar; Overrides default mouse over/leave behavior
    :param delay: When content changes, the scrollbar appears; this delay defines the amount of time (in milliseconds) before scrollbars disappear again (if component is not hovered)
    :param tabindex: Tabindex HTML attribute value
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-scroll-area", children, **kwargs)
        self._attr_names += [
            "dark",
            "bar_style",
            "vertical_bar_style",
            "horizontal_bar_style",
            "thumb_style",
            "vertical_thumb_style",
            "horizontal_thumb_style",
            "content_style",
            "content_active_style",
            "visible",
            "delay",
            "tabindex",
        ]
        self._event_names += [
            "scroll",
        ]


class QScrollObserver(HtmlElement):
    """
    Properties

    :param debounce: Debounce amount (in milliseconds)
    :param axis: Axis on which to detect changes
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one

    Events

    :param debounce: Debounce amount (in milliseconds)
    :param axis: Axis on which to detect changes
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-scroll-observer", children, **kwargs)
        self._attr_names += [
            "debounce",
            "axis",
            "scroll_target",
        ]
        self._event_names += [
            "scroll",
        ]


class QSelect(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms; If not specified, it takes the value of 'for' prop, if it exists
    :param virtual_scroll_horizontal: Make virtual list work in horizontal mode
    :param virtual_scroll_slice_size: Minimum number of items to render in the virtual list
    :param virtual_scroll_slice_ratio_before: Ratio of number of items in visible zone to render before it
    :param virtual_scroll_slice_ratio_after: Ratio of number of items in visible zone to render after it
    :param virtual_scroll_item_size: Default size in pixels (height if vertical, width if horizontal) of an item; This value is used for rendering the initial list; Try to use a value close to the minimum size of an item
    :param virtual_scroll_sticky_size_start: Size in pixels (height if vertical, width if horizontal) of the sticky part (if using one) at the start of the list; A correct value will improve scroll precision
    :param virtual_scroll_sticky_size_end: Size in pixels (height if vertical, width if horizontal) of the sticky part (if using one) at the end of the list; A correct value will improve scroll precision
    :param table_colspan: The number of columns in the table (you need this if you use table-layout: fixed)
    :param model_value: Model of the component; Must be Array if using 'multiple' prop; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param error: Does field have validation errors?
    :param error_message: Validation error message (gets displayed only if 'error' is set to 'true')
    :param no_error_icon: Hide error icon when there is an error
    :param rules: Array of Functions/Strings; If String, then it must be a name of one of the embedded validation rules
    :param reactive_rules: By default a change in the rules does not trigger a new validation until the model changes; If set to true then a change in the rules will trigger a validation; Has a performance penalty, so use it only when you really need it
    :param lazy_rules: If set to boolean true then it checks validation status against the 'rules' only after field loses focus for first time; If set to 'ondemand' then it will trigger only when component's validate() method is manually called or when the wrapper QForm submits itself
    :param label: A text label that will “float” up above the input field, once the field gets focus
    :param stack_label: Label will be always shown above the field regardless of field content (if any)
    :param hint: Helper (hint) text which gets placed below your wrapped form component
    :param hide_hint: Hide the helper (hint) text when field doesn't have focus
    :param prefix: Prefix
    :param suffix: Suffix
    :param label_color: Color name for the label from the Quasar Color Palette; Overrides the 'color' prop; The difference from 'color' prop is that the label will always have this color, even when field is not focused
    :param color: Color name for component from the Quasar Color Palette
    :param bg_color: Color name for component from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param loading: Signals the user a process is in progress by displaying a spinner; Spinner can be customized by using the 'loading' slot.
    :param clearable: Appends clearable icon when a value (not undefined or null) is set; When clicked, model becomes null
    :param clear_icon: Custom icon to use for the clear button when using along with 'clearable' prop
    :param filled: Use 'filled' design for the field
    :param outlined: Use 'outlined' design for the field
    :param borderless: Use 'borderless' design for the field
    :param standout: Use 'standout' design for the field; Specifies classes to be applied when focused (overriding default ones)
    :param label_slot: Enables label slot; You need to set it to force use of the 'label' slot if the 'label' prop is not set
    :param bottom_slots: Enables bottom slots ('error', 'hint', 'counter')
    :param hide_bottom_space: Do not reserve space for hint/error/counter anymore when these are not used; As a result, it also disables the animation for those; It also allows the hint/error area to stretch vertically based on its content
    :param counter: Show an automatic counter on bottom right
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param square: Remove border-radius so borders are squared; Overrides 'rounded' prop
    :param dense: Dense mode; occupies less space
    :param item_aligned: Match inner content alignment to that of QItem
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param autofocus: Focus field on initial component render
    :param for: Used to specify the 'id' of the control and also the 'for' attribute of the label that wraps it; If no 'name' prop is specified, then it is used for this attribute as well
    :param multiple: Allow multiple selection; Model must be Array
    :param display_value: Override default selection string, if not using 'selected' slot/scoped slot and if not using 'use-chips' prop
    :param display_value_html: Force render the selected option(s) as HTML; This can lead to XSS attacks so make sure that you sanitize the content; Does NOT apply when using 'selected' or 'selected-item' slots!
    :param options: Available options that the user can select from. For best performance freeze the list of options.
    :param option_value: Property of option which holds the 'value'; If using a function then for best performance, reference it from your scope and do not define it inline
    :param option_label: Property of option which holds the 'label'; If using a function then for best performance, reference it from your scope and do not define it inline
    :param option_disable: Property of option which tells it's disabled; The value of the property must be a Boolean; If using a function then for best performance, reference it from your scope and do not define it inline
    :param hide_selected: Hides selection; Use the underlying input tag to hold the label (instead of showing it to the right of the input) of the selected option; Only works for non 'multiple' Selects
    :param hide_dropdown_icon: Hides dropdown icon
    :param dropdown_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param max_values: Allow a maximum number of selections that the user can do
    :param options_dense: Dense mode for options list; occupies less space
    :param options_dark: Options menu will be colored with a dark color
    :param options_selected_class: CSS class name for options that are active/selected; Set it to an empty string to stop applying the default (which is text-* where * is the 'color' prop value)
    :param options_html: Force render the options as HTML; This can lead to XSS attacks so make sure that you sanitize the content; Does NOT apply when using 'option' slot!
    :param options_cover: Expanded menu will cover the component (will not work along with 'use-input' prop for obvious reasons)
    :param menu_shrink: Allow the options list to be narrower than the field (only in menu mode)
    :param menu_anchor: Two values setting the starting position or anchor point of the options list relative to the field (only in menu mode)
    :param menu_self: Two values setting the options list's own position relative to its target (only in menu mode)
    :param menu_offset: An array of two numbers to offset the options list horizontally and vertically in pixels (only in menu mode)
    :param popup_content_class: Class definitions to be attributed to the popup content
    :param popup_content_style: Style definitions to be attributed to the popup content
    :param use_input: Use an input tag where users can type
    :param use_chips: Use QChip to show what is currently selected
    :param fill_input: Fills the input with current value; Useful along with 'hide-selected'; Does NOT works along with 'multiple' selection
    :param new_value_mode: Enables creation of new values and defines behavior when a new value is added: 'add' means it adds the value (even if possible duplicate), 'add-unique' adds only unique values, and 'toggle' adds or removes the value (based on if it exists or not already); When using this prop then listening for @new-value becomes optional (only to override the behavior defined by 'new-value-mode')
    :param map_options: Try to map labels of model from 'options' Array; has a small performance penalty; If you are using emit-value you will probably need to use map-options to display the label text in the select field rather than the value;  Refer to the 'Affecting model' section above
    :param emit_value: Update model with the value of the selected option instead of the whole option
    :param input_debounce: Debounce the input model update with an amount of milliseconds
    :param input_class: Class definitions to be attributed to the underlying input tag
    :param input_style: Style definitions to be attributed to the underlying input tag
    :param tabindex: Tabindex HTML attribute value
    :param autocomplete: Autocomplete attribute for field
    :param transition_show: Transition when showing the menu/dialog; One of Quasar's embedded transitions
    :param transition_hide: Transition when hiding the menu/dialog; One of Quasar's embedded transitions
    :param transition_duration: Transition duration when hiding the menu/dialog (in milliseconds, without unit)
    :param behavior: Overrides the default dynamic mode of showing as menu on desktop and dialog on mobiles

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms; If not specified, it takes the value of 'for' prop, if it exists
    :param virtual_scroll_horizontal: Make virtual list work in horizontal mode
    :param virtual_scroll_slice_size: Minimum number of items to render in the virtual list
    :param virtual_scroll_slice_ratio_before: Ratio of number of items in visible zone to render before it
    :param virtual_scroll_slice_ratio_after: Ratio of number of items in visible zone to render after it
    :param virtual_scroll_item_size: Default size in pixels (height if vertical, width if horizontal) of an item; This value is used for rendering the initial list; Try to use a value close to the minimum size of an item
    :param virtual_scroll_sticky_size_start: Size in pixels (height if vertical, width if horizontal) of the sticky part (if using one) at the start of the list; A correct value will improve scroll precision
    :param virtual_scroll_sticky_size_end: Size in pixels (height if vertical, width if horizontal) of the sticky part (if using one) at the end of the list; A correct value will improve scroll precision
    :param table_colspan: The number of columns in the table (you need this if you use table-layout: fixed)
    :param model_value: Model of the component; Must be Array if using 'multiple' prop; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param error: Does field have validation errors?
    :param error_message: Validation error message (gets displayed only if 'error' is set to 'true')
    :param no_error_icon: Hide error icon when there is an error
    :param rules: Array of Functions/Strings; If String, then it must be a name of one of the embedded validation rules
    :param reactive_rules: By default a change in the rules does not trigger a new validation until the model changes; If set to true then a change in the rules will trigger a validation; Has a performance penalty, so use it only when you really need it
    :param lazy_rules: If set to boolean true then it checks validation status against the 'rules' only after field loses focus for first time; If set to 'ondemand' then it will trigger only when component's validate() method is manually called or when the wrapper QForm submits itself
    :param label: A text label that will “float” up above the input field, once the field gets focus
    :param stack_label: Label will be always shown above the field regardless of field content (if any)
    :param hint: Helper (hint) text which gets placed below your wrapped form component
    :param hide_hint: Hide the helper (hint) text when field doesn't have focus
    :param prefix: Prefix
    :param suffix: Suffix
    :param label_color: Color name for the label from the Quasar Color Palette; Overrides the 'color' prop; The difference from 'color' prop is that the label will always have this color, even when field is not focused
    :param color: Color name for component from the Quasar Color Palette
    :param bg_color: Color name for component from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param loading: Signals the user a process is in progress by displaying a spinner; Spinner can be customized by using the 'loading' slot.
    :param clearable: Appends clearable icon when a value (not undefined or null) is set; When clicked, model becomes null
    :param clear_icon: Custom icon to use for the clear button when using along with 'clearable' prop
    :param filled: Use 'filled' design for the field
    :param outlined: Use 'outlined' design for the field
    :param borderless: Use 'borderless' design for the field
    :param standout: Use 'standout' design for the field; Specifies classes to be applied when focused (overriding default ones)
    :param label_slot: Enables label slot; You need to set it to force use of the 'label' slot if the 'label' prop is not set
    :param bottom_slots: Enables bottom slots ('error', 'hint', 'counter')
    :param hide_bottom_space: Do not reserve space for hint/error/counter anymore when these are not used; As a result, it also disables the animation for those; It also allows the hint/error area to stretch vertically based on its content
    :param counter: Show an automatic counter on bottom right
    :param rounded: Applies a small standard border-radius for a squared shape of the component
    :param square: Remove border-radius so borders are squared; Overrides 'rounded' prop
    :param dense: Dense mode; occupies less space
    :param item_aligned: Match inner content alignment to that of QItem
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param autofocus: Focus field on initial component render
    :param for: Used to specify the 'id' of the control and also the 'for' attribute of the label that wraps it; If no 'name' prop is specified, then it is used for this attribute as well
    :param multiple: Allow multiple selection; Model must be Array
    :param display_value: Override default selection string, if not using 'selected' slot/scoped slot and if not using 'use-chips' prop
    :param display_value_html: Force render the selected option(s) as HTML; This can lead to XSS attacks so make sure that you sanitize the content; Does NOT apply when using 'selected' or 'selected-item' slots!
    :param options: Available options that the user can select from. For best performance freeze the list of options.
    :param option_value: Property of option which holds the 'value'; If using a function then for best performance, reference it from your scope and do not define it inline
    :param option_label: Property of option which holds the 'label'; If using a function then for best performance, reference it from your scope and do not define it inline
    :param option_disable: Property of option which tells it's disabled; The value of the property must be a Boolean; If using a function then for best performance, reference it from your scope and do not define it inline
    :param hide_selected: Hides selection; Use the underlying input tag to hold the label (instead of showing it to the right of the input) of the selected option; Only works for non 'multiple' Selects
    :param hide_dropdown_icon: Hides dropdown icon
    :param dropdown_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param max_values: Allow a maximum number of selections that the user can do
    :param options_dense: Dense mode for options list; occupies less space
    :param options_dark: Options menu will be colored with a dark color
    :param options_selected_class: CSS class name for options that are active/selected; Set it to an empty string to stop applying the default (which is text-* where * is the 'color' prop value)
    :param options_html: Force render the options as HTML; This can lead to XSS attacks so make sure that you sanitize the content; Does NOT apply when using 'option' slot!
    :param options_cover: Expanded menu will cover the component (will not work along with 'use-input' prop for obvious reasons)
    :param menu_shrink: Allow the options list to be narrower than the field (only in menu mode)
    :param menu_anchor: Two values setting the starting position or anchor point of the options list relative to the field (only in menu mode)
    :param menu_self: Two values setting the options list's own position relative to its target (only in menu mode)
    :param menu_offset: An array of two numbers to offset the options list horizontally and vertically in pixels (only in menu mode)
    :param popup_content_class: Class definitions to be attributed to the popup content
    :param popup_content_style: Style definitions to be attributed to the popup content
    :param use_input: Use an input tag where users can type
    :param use_chips: Use QChip to show what is currently selected
    :param fill_input: Fills the input with current value; Useful along with 'hide-selected'; Does NOT works along with 'multiple' selection
    :param new_value_mode: Enables creation of new values and defines behavior when a new value is added: 'add' means it adds the value (even if possible duplicate), 'add-unique' adds only unique values, and 'toggle' adds or removes the value (based on if it exists or not already); When using this prop then listening for @new-value becomes optional (only to override the behavior defined by 'new-value-mode')
    :param map_options: Try to map labels of model from 'options' Array; has a small performance penalty; If you are using emit-value you will probably need to use map-options to display the label text in the select field rather than the value;  Refer to the 'Affecting model' section above
    :param emit_value: Update model with the value of the selected option instead of the whole option
    :param input_debounce: Debounce the input model update with an amount of milliseconds
    :param input_class: Class definitions to be attributed to the underlying input tag
    :param input_style: Style definitions to be attributed to the underlying input tag
    :param tabindex: Tabindex HTML attribute value
    :param autocomplete: Autocomplete attribute for field
    :param transition_show: Transition when showing the menu/dialog; One of Quasar's embedded transitions
    :param transition_hide: Transition when hiding the menu/dialog; One of Quasar's embedded transitions
    :param transition_duration: Transition duration when hiding the menu/dialog (in milliseconds, without unit)
    :param behavior: Overrides the default dynamic mode of showing as menu on desktop and dialog on mobiles
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-select", children, **kwargs)
        self._attr_names += [
            "name",
            "virtual_scroll_horizontal",
            "virtual_scroll_slice_size",
            "virtual_scroll_slice_ratio_before",
            "virtual_scroll_slice_ratio_after",
            "virtual_scroll_item_size",
            "virtual_scroll_sticky_size_start",
            "virtual_scroll_sticky_size_end",
            "table_colspan",
            "model_value",
            "error",
            "error_message",
            "no_error_icon",
            "rules",
            "reactive_rules",
            "lazy_rules",
            "label",
            "stack_label",
            "hint",
            "hide_hint",
            "prefix",
            "suffix",
            "label_color",
            "color",
            "bg_color",
            "dark",
            "loading",
            "clearable",
            "clear_icon",
            "filled",
            "outlined",
            "borderless",
            "standout",
            "label_slot",
            "bottom_slots",
            "hide_bottom_space",
            "counter",
            "rounded",
            "square",
            "dense",
            "item_aligned",
            "disable",
            "readonly",
            "autofocus",
            "for",
            "multiple",
            "display_value",
            "display_value_html",
            "options",
            "option_value",
            "option_label",
            "option_disable",
            "hide_selected",
            "hide_dropdown_icon",
            "dropdown_icon",
            "max_values",
            "options_dense",
            "options_dark",
            "options_selected_class",
            "options_html",
            "options_cover",
            "menu_shrink",
            "menu_anchor",
            "menu_self",
            "menu_offset",
            "popup_content_class",
            "popup_content_style",
            "use_input",
            "use_chips",
            "fill_input",
            "new_value_mode",
            "map_options",
            "emit_value",
            "input_debounce",
            "input_class",
            "input_style",
            "tabindex",
            "autocomplete",
            "transition_show",
            "transition_hide",
            "transition_duration",
            "behavior",
        ]
        self._event_names += [
            "virtual_scroll",
            "clear",
            ("update_model_value", "update:model-value"),
            "input_value",
            "remove",
            "add",
            "new_value",
            "filter",
            "filter_abort",
            "popup_show",
            "popup_hide",
        ]


class QSeparator(HtmlElement):
    """
    Properties

    :param dark: Notify the component that the background is a dark color
    :param spaced: If set to true, the corresponding direction margins will be set to 8px; It can also be set to a size in CSS units, including unit name, or one of the xs|sm|md|lg|xl predefined sizes
    :param inset: If set to Boolean true, the left and right margins will be set to 16px. If set to 'item' then it will match a QItem's design. If set to 'item-thumbnail' then it will match the design of a QItem with a thumbnail on the left side
    :param vertical: If set to true, the separator will be vertical.
    :param size: Size in CSS units, including unit name
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param dark: Notify the component that the background is a dark color
    :param spaced: If set to true, the corresponding direction margins will be set to 8px; It can also be set to a size in CSS units, including unit name, or one of the xs|sm|md|lg|xl predefined sizes
    :param inset: If set to Boolean true, the left and right margins will be set to 16px. If set to 'item' then it will match a QItem's design. If set to 'item-thumbnail' then it will match the design of a QItem with a thumbnail on the left side
    :param vertical: If set to true, the separator will be vertical.
    :param size: Size in CSS units, including unit name
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-separator", children, **kwargs)
        self._attr_names += [
            "dark",
            "spaced",
            "inset",
            "vertical",
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSkeleton(HtmlElement):
    """
    Properties

    :param dark: Notify the component that the background is a dark color
    :param type: Type of skeleton placeholder
    :param animation: The animation effect of the skeleton placeholder
    :param animation_speed: Animation speed (in milliseconds, without unit)
    :param square: Removes border-radius so borders are squared
    :param bordered: Applies a default border to the component
    :param size: Size in CSS units, including unit name; Overrides 'height' and 'width' props and applies the value to both height and width
    :param width: Width in CSS units, including unit name; Apply custom width; Use this prop or through CSS; Overridden by 'size' prop if used
    :param height: Height in CSS units, including unit name; Apply custom height; Use this prop or through CSS; Overridden by 'size' prop if used
    :param tag: HTML tag to use

    Events

    :param dark: Notify the component that the background is a dark color
    :param type: Type of skeleton placeholder
    :param animation: The animation effect of the skeleton placeholder
    :param animation_speed: Animation speed (in milliseconds, without unit)
    :param square: Removes border-radius so borders are squared
    :param bordered: Applies a default border to the component
    :param size: Size in CSS units, including unit name; Overrides 'height' and 'width' props and applies the value to both height and width
    :param width: Width in CSS units, including unit name; Apply custom width; Use this prop or through CSS; Overridden by 'size' prop if used
    :param height: Height in CSS units, including unit name; Apply custom height; Use this prop or through CSS; Overridden by 'size' prop if used
    :param tag: HTML tag to use
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-skeleton", children, **kwargs)
        self._attr_names += [
            "dark",
            "type",
            "animation",
            "animation_speed",
            "square",
            "bordered",
            "size",
            "width",
            "height",
            "tag",
        ]
        self._event_names += [
        ]


class QSlideItem(HtmlElement):
    """
    Properties

    :param left_color: Color name for left-side background from the Quasar Color Palette
    :param right_color: Color name for right-side background from the Quasar Color Palette
    :param top_color: Color name for top-side background from the Quasar Color Palette
    :param bottom_color: Color name for bottom-side background from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color

    Events

    :param left_color: Color name for left-side background from the Quasar Color Palette
    :param right_color: Color name for right-side background from the Quasar Color Palette
    :param top_color: Color name for top-side background from the Quasar Color Palette
    :param bottom_color: Color name for bottom-side background from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-slide-item", children, **kwargs)
        self._attr_names += [
            "left_color",
            "right_color",
            "top_color",
            "bottom_color",
            "dark",
        ]
        self._event_names += [
            "left",
            "right",
            "top",
            "bottom",
            "slide",
            "action",
        ]


class QSlideTransition(HtmlElement):
    """
    Properties

    :param appear: If set to true, the transition will be applied on the initial render.
    :param duration: Duration (in milliseconds) enabling animated scroll.

    Events

    :param appear: If set to true, the transition will be applied on the initial render.
    :param duration: Duration (in milliseconds) enabling animated scroll.
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-slide-transition", children, **kwargs)
        self._attr_names += [
            "appear",
            "duration",
        ]
        self._event_names += [
            "show",
            "hide",
        ]


class QSlider(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param min: Minimum value of the model; Set track's minimum value
    :param max: Maximum value of the model; Set track's maximum value
    :param inner_min: Inner minimum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be higher or equal to 'min' prop; Defaults to 'min' prop
    :param inner_max: Inner maximum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be lower or equal to 'max' prop; Defaults to 'max' prop
    :param step: Specify step amount between valid values (> 0.0); When step equals to 0 it defines infinite granularity
    :param snap: Snap on valid values, rather than sliding freely; Suggestion: use with 'step' prop
    :param reverse: Work in reverse (changes direction)
    :param vertical: Display in vertical direction
    :param color: Color name for component from the Quasar Color Palette
    :param track_color: Color name for the track (can be 'transparent' too) from the Quasar Color Palette
    :param track_img: Apply a pattern image on the track
    :param inner_track_color: Color name for the inner track (can be 'transparent' too) from the Quasar Color Palette
    :param inner_track_img: Apply a pattern image on the inner track
    :param selection_color: Color name for the selection bar (can be 'transparent' too) from the Quasar Color Palette
    :param selection_img: Apply a pattern image on the selection bar
    :param label: Popup a label when user clicks/taps on the slider thumb and moves it
    :param label_color: Color name for component from the Quasar Color Palette
    :param label_text_color: Color name for component from the Quasar Color Palette
    :param switch_label_side: Switch the position of the label (top <-> bottom or left <-> right)
    :param label_always: Always display the label
    :param markers: Display markers on the track, one for each possible value for the model or using a custom step (when specifying a Number)
    :param marker_labels: Configure the marker labels (or show the default ones if 'true'); Array of definition Objects or Object with key-value where key is the model and the value is the marker label definition
    :param marker_labels_class: CSS class(es) to apply to the marker labels container
    :param switch_marker_labels_side: Switch the position of the marker labels (top <-> bottom or left <-> right)
    :param track_size: Track size (including CSS unit)
    :param thumb_size: Thumb size (including CSS unit)
    :param thumb_color: Color name for component from the Quasar Color Palette
    :param thumb_path: Set custom thumb svg path
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param tabindex: Tabindex HTML attribute value
    :param model_value: Model of the component (must be between min/max); Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param label_value: Override default label value

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param min: Minimum value of the model; Set track's minimum value
    :param max: Maximum value of the model; Set track's maximum value
    :param inner_min: Inner minimum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be higher or equal to 'min' prop; Defaults to 'min' prop
    :param inner_max: Inner maximum value of the model; Use in case you need the model value to be inside of the track's min-max values; Needs to be lower or equal to 'max' prop; Defaults to 'max' prop
    :param step: Specify step amount between valid values (> 0.0); When step equals to 0 it defines infinite granularity
    :param snap: Snap on valid values, rather than sliding freely; Suggestion: use with 'step' prop
    :param reverse: Work in reverse (changes direction)
    :param vertical: Display in vertical direction
    :param color: Color name for component from the Quasar Color Palette
    :param track_color: Color name for the track (can be 'transparent' too) from the Quasar Color Palette
    :param track_img: Apply a pattern image on the track
    :param inner_track_color: Color name for the inner track (can be 'transparent' too) from the Quasar Color Palette
    :param inner_track_img: Apply a pattern image on the inner track
    :param selection_color: Color name for the selection bar (can be 'transparent' too) from the Quasar Color Palette
    :param selection_img: Apply a pattern image on the selection bar
    :param label: Popup a label when user clicks/taps on the slider thumb and moves it
    :param label_color: Color name for component from the Quasar Color Palette
    :param label_text_color: Color name for component from the Quasar Color Palette
    :param switch_label_side: Switch the position of the label (top <-> bottom or left <-> right)
    :param label_always: Always display the label
    :param markers: Display markers on the track, one for each possible value for the model or using a custom step (when specifying a Number)
    :param marker_labels: Configure the marker labels (or show the default ones if 'true'); Array of definition Objects or Object with key-value where key is the model and the value is the marker label definition
    :param marker_labels_class: CSS class(es) to apply to the marker labels container
    :param switch_marker_labels_side: Switch the position of the marker labels (top <-> bottom or left <-> right)
    :param track_size: Track size (including CSS unit)
    :param thumb_size: Thumb size (including CSS unit)
    :param thumb_color: Color name for component from the Quasar Color Palette
    :param thumb_path: Set custom thumb svg path
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    :param tabindex: Tabindex HTML attribute value
    :param model_value: Model of the component (must be between min/max); Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param label_value: Override default label value
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-slider", children, **kwargs)
        self._attr_names += [
            "name",
            "min",
            "max",
            "inner_min",
            "inner_max",
            "step",
            "snap",
            "reverse",
            "vertical",
            "color",
            "track_color",
            "track_img",
            "inner_track_color",
            "inner_track_img",
            "selection_color",
            "selection_img",
            "label",
            "label_color",
            "label_text_color",
            "switch_label_side",
            "label_always",
            "markers",
            "marker_labels",
            "marker_labels_class",
            "switch_marker_labels_side",
            "track_size",
            "thumb_size",
            "thumb_color",
            "thumb_path",
            "dark",
            "dense",
            "disable",
            "readonly",
            "tabindex",
            "model_value",
            "label_value",
        ]
        self._event_names += [
            "change",
            "pan",
            ("update_model_value", "update:model-value"),
        ]


class QSpace(HtmlElement):
    """
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-space", children, **kwargs)
        self._attr_names += [
        ]
        self._event_names += [
        ]


class QSpinner(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    :param thickness: Override value to use for stroke-width

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    :param thickness: Override value to use for stroke-width
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
            "thickness",
        ]
        self._event_names += [
        ]


class QSpinnerAudio(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-audio", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerBall(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-ball", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerBars(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-bars", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerBox(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-box", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerClock(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-clock", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerComment(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-comment", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerCube(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-cube", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerDots(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-dots", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerFacebook(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-facebook", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerGears(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-gears", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerGrid(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-grid", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerHearts(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-hearts", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerHourglass(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-hourglass", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerInfinity(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-infinity", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerIos(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-ios", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerOrbit(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-orbit", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerOval(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-oval", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerPie(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-pie", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerPuff(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-puff", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerRadio(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-radio", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerRings(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-rings", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSpinnerTail(HtmlElement):
    """
    Properties

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette

    Events

    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param color: Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-spinner-tail", children, **kwargs)
        self._attr_names += [
            "size",
            "color",
        ]
        self._event_names += [
        ]


class QSplitter(HtmlElement):
    """
    Properties

    :param model_value: Model of the component defining the size of first panel (or second if using reverse) in the unit specified (for '%' it's the split ratio percent - 0.0 < x < 100.0; for 'px' it's the size in px); Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param reverse: Apply the model size to the second panel (by default it applies to the first)
    :param unit: CSS unit for the model
    :param emit_immediately: Emit model while user is panning on the separator
    :param horizontal: Allows the splitter to split its two panels horizontally, instead of vertically
    :param limits: An array of two values representing the minimum and maximum split size of the two panels; When 'px' unit is set then you can use Infinity as the second value to make it unbound on the other side
    :param disable: Put component in disabled mode
    :param before_class: Class definitions to be attributed to the 'before' panel
    :param after_class: Class definitions to be attributed to the 'after' panel
    :param separator_class: Class definitions to be attributed to the splitter separator
    :param separator_style: Style definitions to be attributed to the splitter separator
    :param dark: Applies a default lighter color on the separator; To be used when background is darker; Avoid using when you are overriding through separator-class or separator-style props

    Events

    :param model_value: Model of the component defining the size of first panel (or second if using reverse) in the unit specified (for '%' it's the split ratio percent - 0.0 < x < 100.0; for 'px' it's the size in px); Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param reverse: Apply the model size to the second panel (by default it applies to the first)
    :param unit: CSS unit for the model
    :param emit_immediately: Emit model while user is panning on the separator
    :param horizontal: Allows the splitter to split its two panels horizontally, instead of vertically
    :param limits: An array of two values representing the minimum and maximum split size of the two panels; When 'px' unit is set then you can use Infinity as the second value to make it unbound on the other side
    :param disable: Put component in disabled mode
    :param before_class: Class definitions to be attributed to the 'before' panel
    :param after_class: Class definitions to be attributed to the 'after' panel
    :param separator_class: Class definitions to be attributed to the splitter separator
    :param separator_style: Style definitions to be attributed to the splitter separator
    :param dark: Applies a default lighter color on the separator; To be used when background is darker; Avoid using when you are overriding through separator-class or separator-style props
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-splitter", children, **kwargs)
        self._attr_names += [
            "model_value",
            "reverse",
            "unit",
            "emit_immediately",
            "horizontal",
            "limits",
            "disable",
            "before_class",
            "after_class",
            "separator_class",
            "separator_style",
            "dark",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
        ]


class QStep(HtmlElement):
    """
    Properties

    :param name: Panel name
    :param disable: Put component in disabled mode
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param color: Color name for component from the Quasar Color Palette
    :param title: Step title
    :param caption: Step’s additional information that appears beneath the title
    :param prefix: Step's prefix (max 2 characters) which replaces the icon if step does not has error, is being edited or is marked as done
    :param done_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param done_color: Color name for component from the Quasar Color Palette
    :param active_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param active_color: Color name for component from the Quasar Color Palette
    :param error_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param error_color: Color name for component from the Quasar Color Palette
    :param header_nav: Allow navigation through the header
    :param done: Mark the step as 'done'
    :param error: Mark the step as having an error

    Events

    :param name: Panel name
    :param disable: Put component in disabled mode
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param color: Color name for component from the Quasar Color Palette
    :param title: Step title
    :param caption: Step’s additional information that appears beneath the title
    :param prefix: Step's prefix (max 2 characters) which replaces the icon if step does not has error, is being edited or is marked as done
    :param done_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param done_color: Color name for component from the Quasar Color Palette
    :param active_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param active_color: Color name for component from the Quasar Color Palette
    :param error_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param error_color: Color name for component from the Quasar Color Palette
    :param header_nav: Allow navigation through the header
    :param done: Mark the step as 'done'
    :param error: Mark the step as having an error
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-step", children, **kwargs)
        self._attr_names += [
            "name",
            "disable",
            "icon",
            "color",
            "title",
            "caption",
            "prefix",
            "done_icon",
            "done_color",
            "active_icon",
            "active_color",
            "error_icon",
            "error_color",
            "header_nav",
            "done",
            "error",
        ]
        self._event_names += [
        ]


class QStepper(HtmlElement):
    """
    Properties

    :param model_value: Model of the component defining the current panel's name; If a Number is used, it does not define the panel's index, but rather the panel's name which can also be an Integer; Either use this property (along with a listener for 'update:model-value' event) OR use the v-model directive.
    :param keep_alive: Equivalent to using Vue's native <keep-alive> component on the content
    :param keep_alive_include: Equivalent to using Vue's native include prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_exclude: Equivalent to using Vue's native exclude prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_max: Equivalent to using Vue's native max prop for <keep-alive>
    :param animated: Enable transitions between panel (also see 'transition-prev' and 'transition-next' props)
    :param infinite: Makes component appear as infinite (when reaching last panel, next one will become the first one)
    :param swipeable: Enable swipe events (may interfere with content's touch/mouse events)
    :param vertical: Put Stepper in vertical mode (instead of horizontal by default)
    :param transition_prev: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_next: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param dark: Notify the component that the background is a dark color
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param alternative_labels: Use alternative labels - stacks the icon on top of the label (applies only to horizontal stepper)
    :param header_nav: Allow navigation through the header
    :param contracted: Hide header labels on narrow windows
    :param inactive_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param inactive_color: Color name for component from the Quasar Color Palette
    :param done_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param done_color: Color name for component from the Quasar Color Palette
    :param active_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param active_color: Color name for component from the Quasar Color Palette
    :param error_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param error_color: Color name for component from the Quasar Color Palette
    :param header_class: Class definitions to be attributed to the header

    Events

    :param model_value: Model of the component defining the current panel's name; If a Number is used, it does not define the panel's index, but rather the panel's name which can also be an Integer; Either use this property (along with a listener for 'update:model-value' event) OR use the v-model directive.
    :param keep_alive: Equivalent to using Vue's native <keep-alive> component on the content
    :param keep_alive_include: Equivalent to using Vue's native include prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_exclude: Equivalent to using Vue's native exclude prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_max: Equivalent to using Vue's native max prop for <keep-alive>
    :param animated: Enable transitions between panel (also see 'transition-prev' and 'transition-next' props)
    :param infinite: Makes component appear as infinite (when reaching last panel, next one will become the first one)
    :param swipeable: Enable swipe events (may interfere with content's touch/mouse events)
    :param vertical: Put Stepper in vertical mode (instead of horizontal by default)
    :param transition_prev: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_next: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param dark: Notify the component that the background is a dark color
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param alternative_labels: Use alternative labels - stacks the icon on top of the label (applies only to horizontal stepper)
    :param header_nav: Allow navigation through the header
    :param contracted: Hide header labels on narrow windows
    :param inactive_icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param inactive_color: Color name for component from the Quasar Color Palette
    :param done_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param done_color: Color name for component from the Quasar Color Palette
    :param active_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param active_color: Color name for component from the Quasar Color Palette
    :param error_icon: Icon name following Quasar convention; If 'none' (String) is used as value, then it will defer to prefix or the regular icon for this state; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param error_color: Color name for component from the Quasar Color Palette
    :param header_class: Class definitions to be attributed to the header
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-stepper", children, **kwargs)
        self._attr_names += [
            "model_value",
            "keep_alive",
            "keep_alive_include",
            "keep_alive_exclude",
            "keep_alive_max",
            "animated",
            "infinite",
            "swipeable",
            "vertical",
            "transition_prev",
            "transition_next",
            "transition_duration",
            "dark",
            "flat",
            "bordered",
            "alternative_labels",
            "header_nav",
            "contracted",
            "inactive_icon",
            "inactive_color",
            "done_icon",
            "done_color",
            "active_icon",
            "active_color",
            "error_icon",
            "error_color",
            "header_class",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "before_transition",
            "transition",
        ]


class QStepperNavigation(HtmlElement):
    """
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-stepper-navigation", children, **kwargs)
        self._attr_names += [
        ]
        self._event_names += [
        ]


class QTab(HtmlElement):
    """
    Properties

    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param label: A number or string to label the tab
    :param alert: Adds an alert symbol to the tab, notifying the user there are some updates; If its value is not a Boolean, then you can specify a color
    :param alert_icon: Adds a floating icon to the tab, notifying the user there are some updates; It's displayed only if 'alert' is set; Can use the color specified by 'alert' prop
    :param name: Panel name
    :param no_caps: Turns off capitalizing all letters within the tab (which is the default)
    :param content_class: Class definitions to be attributed to the content wrapper
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param tabindex: Tabindex HTML attribute value
    :param disable: Put component in disabled mode

    Events

    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param label: A number or string to label the tab
    :param alert: Adds an alert symbol to the tab, notifying the user there are some updates; If its value is not a Boolean, then you can specify a color
    :param alert_icon: Adds a floating icon to the tab, notifying the user there are some updates; It's displayed only if 'alert' is set; Can use the color specified by 'alert' prop
    :param name: Panel name
    :param no_caps: Turns off capitalizing all letters within the tab (which is the default)
    :param content_class: Class definitions to be attributed to the content wrapper
    :param ripple: Configure material ripple (disable it by setting it to 'false' or supply a config object)
    :param tabindex: Tabindex HTML attribute value
    :param disable: Put component in disabled mode
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-tab", children, **kwargs)
        self._attr_names += [
            "icon",
            "label",
            "alert",
            "alert_icon",
            "name",
            "no_caps",
            "content_class",
            "ripple",
            "tabindex",
            "disable",
        ]
        self._event_names += [
        ]


class QTabPanel(HtmlElement):
    """
    Properties

    :param name: Panel name
    :param disable: Put component in disabled mode
    :param dark: Notify the component that the background is a dark color

    Events

    :param name: Panel name
    :param disable: Put component in disabled mode
    :param dark: Notify the component that the background is a dark color
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-tab-panel", children, **kwargs)
        self._attr_names += [
            "name",
            "disable",
            "dark",
        ]
        self._event_names += [
        ]


class QTabPanels(HtmlElement):
    """
    Properties

    :param model_value: Model of the component defining the current panel's name; If a Number is used, it does not define the panel's index, but rather the panel's name which can also be an Integer; Either use this property (along with a listener for 'update:model-value' event) OR use the v-model directive.
    :param keep_alive: Equivalent to using Vue's native <keep-alive> component on the content
    :param keep_alive_include: Equivalent to using Vue's native include prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_exclude: Equivalent to using Vue's native exclude prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_max: Equivalent to using Vue's native max prop for <keep-alive>
    :param animated: Enable transitions between panel (also see 'transition-prev' and 'transition-next' props)
    :param infinite: Makes component appear as infinite (when reaching last panel, next one will become the first one)
    :param swipeable: Enable swipe events (may interfere with content's touch/mouse events)
    :param vertical: Default transitions and swipe actions will be on the vertical axis
    :param transition_prev: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_next: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_duration: Transition duration (in milliseconds, without unit)

    Events

    :param model_value: Model of the component defining the current panel's name; If a Number is used, it does not define the panel's index, but rather the panel's name which can also be an Integer; Either use this property (along with a listener for 'update:model-value' event) OR use the v-model directive.
    :param keep_alive: Equivalent to using Vue's native <keep-alive> component on the content
    :param keep_alive_include: Equivalent to using Vue's native include prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_exclude: Equivalent to using Vue's native exclude prop for <keep-alive>; Values must be valid Vue component names
    :param keep_alive_max: Equivalent to using Vue's native max prop for <keep-alive>
    :param animated: Enable transitions between panel (also see 'transition-prev' and 'transition-next' props)
    :param infinite: Makes component appear as infinite (when reaching last panel, next one will become the first one)
    :param swipeable: Enable swipe events (may interfere with content's touch/mouse events)
    :param vertical: Default transitions and swipe actions will be on the vertical axis
    :param transition_prev: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_next: One of Quasar's embedded transitions (has effect only if 'animated' prop is set)
    :param transition_duration: Transition duration (in milliseconds, without unit)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-tab-panels", children, **kwargs)
        self._attr_names += [
            "model_value",
            "keep_alive",
            "keep_alive_include",
            "keep_alive_exclude",
            "keep_alive_max",
            "animated",
            "infinite",
            "swipeable",
            "vertical",
            "transition_prev",
            "transition_next",
            "transition_duration",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "before_transition",
            "transition",
        ]


class QTable(HtmlElement):
    """
    Properties

    :param fullscreen: Fullscreen mode
    :param no_route_fullscreen_exit: Changing route app won't exit fullscreen
    :param rows: Rows of data to display
    :param row_key: Property of each row that defines the unique key of each row (the result must be a primitive, not Object, Array, etc); The value of property must be string or a function taking a row and returning the desired (nested) key in the row; If supplying a function then for best performance, reference it from your scope and do not define it inline
    :param virtual_scroll: Display data using QVirtualScroll (for non-grid mode only)
    :param virtual_scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    :param virtual_scroll_slice_size: Minimum number of rows to render in the virtual list
    :param virtual_scroll_slice_ratio_before: Ratio of number of rows in visible zone to render before it
    :param virtual_scroll_slice_ratio_after: Ratio of number of rows in visible zone to render after it
    :param virtual_scroll_item_size: Default size in pixels of a row; This value is used for rendering the initial table; Try to use a value close to the minimum size of a row
    :param virtual_scroll_sticky_size_start: Size in pixels of the sticky header (if using one); A correct value will improve scroll precision; Will be also used for non-virtual-scroll tables for fixing top alignment when using scrollTo method
    :param virtual_scroll_sticky_size_end: Size in pixels of the sticky footer part (if using one); A correct value will improve scroll precision
    :param table_colspan: The number of columns in the table (you need this if you use table-layout: fixed)
    :param color: Color name for component from the Quasar Color Palette
    :param icon_first_page: Icon name following Quasar convention for stepping to first page; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param icon_prev_page: Icon name following Quasar convention for stepping to previous page; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param icon_next_page: Icon name following Quasar convention for stepping to next page; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param icon_last_page: Icon name following Quasar convention for stepping to last page; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param grid: Display data as a grid instead of the default table
    :param grid_header: Display header for grid-mode also
    :param dense: Dense mode; Connect with $q.screen for responsive behavior
    :param columns: The column definitions (Array of Objects)
    :param visible_columns: Array of Strings defining column names ('name' property of each column from 'columns' prop definitions); Columns marked as 'required' are not affected by this property
    :param loading: Put Table into 'loading' state; Notify the user something is happening behind the scenes
    :param title: Table title
    :param hide_header: Hide table header layer
    :param hide_bottom: Hide table bottom layer regardless of what it has to display
    :param hide_selected_banner: Hide the selected rows banner (if any)
    :param hide_no_data: Hide the default no data bottom layer
    :param hide_pagination: Hide the pagination controls at the bottom
    :param dark: Notify the component that the background is a dark color
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param square: Removes border-radius so borders are squared
    :param separator: Use a separator/border between rows, columns or all cells
    :param wrap_cells: Wrap text within table cells
    :param binary_state_sort: Skip the third state (unsorted) when user toggles column sort direction
    :param column_sort_order: Set column sort order: 'ad' (ascending-descending) or 'da' (descending-ascending); It gets applied to all columns unless a column has its own sortOrder specified in the 'columns' definition prop
    :param no_data_label: Override default text to display when no data is available
    :param no_results_label: Override default text to display when user filters the table and no matched results are found
    :param loading_label: Override default text to display when table is in loading state (see 'loading' prop)
    :param selected_rows_label: Text to display when user selected at least one row; For best performance, reference it from your scope and do not define it inline
    :param rows_per_page_label: Text to override default rows per page label at bottom of table
    :param pagination_label: Text to override default pagination label at bottom of table (unless 'pagination' scoped slot is used); For best performance, reference it from your scope and do not define it inline
    :param table_style: CSS style to apply to native HTML <table> element's wrapper (which is a DIV)
    :param table_class: CSS classes to apply to native HTML <table> element's wrapper (which is a DIV)
    :param table_header_style: CSS style to apply to header of native HTML <table> (which is a TR)
    :param table_header_class: CSS classes to apply to header of native HTML <table> (which is a TR)
    :param card_container_style: CSS style to apply to the cards container (when in grid mode)
    :param card_container_class: CSS classes to apply to the cards container (when in grid mode)
    :param card_style: CSS style to apply to the card (when in grid mode) or container card (when not in grid mode)
    :param card_class: CSS classes to apply to the card (when in grid mode) or container card (when not in grid mode)
    :param title_class: CSS classes to apply to the title (if using 'title' prop)
    :param filter: String/Object to filter table with; When using an Object it requires 'filter-method' to also be specified since it will be a custom filtering
    :param filter_method: The actual filtering mechanism; For best performance, reference it from your scope and do not define it inline
    :param pagination: Pagination object; You can also use the 'v-model:pagination' for synching; When not synching it simply initializes the pagination on first render
    :param rows_per_page_options: Options for user to pick (Numbers); Number 0 means 'Show all rows in one page'
    :param selection: Selection type
    :param selected: Keeps the user selection array
    :param expanded: Keeps the array with expanded rows keys
    :param sort_method: The actual sort mechanism. Function (rows, sortBy, descending) => sorted rows; For best performance, reference it from your scope and do not define it inline

    Events

    :param fullscreen: Fullscreen mode
    :param no_route_fullscreen_exit: Changing route app won't exit fullscreen
    :param rows: Rows of data to display
    :param row_key: Property of each row that defines the unique key of each row (the result must be a primitive, not Object, Array, etc); The value of property must be string or a function taking a row and returning the desired (nested) key in the row; If supplying a function then for best performance, reference it from your scope and do not define it inline
    :param virtual_scroll: Display data using QVirtualScroll (for non-grid mode only)
    :param virtual_scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    :param virtual_scroll_slice_size: Minimum number of rows to render in the virtual list
    :param virtual_scroll_slice_ratio_before: Ratio of number of rows in visible zone to render before it
    :param virtual_scroll_slice_ratio_after: Ratio of number of rows in visible zone to render after it
    :param virtual_scroll_item_size: Default size in pixels of a row; This value is used for rendering the initial table; Try to use a value close to the minimum size of a row
    :param virtual_scroll_sticky_size_start: Size in pixels of the sticky header (if using one); A correct value will improve scroll precision; Will be also used for non-virtual-scroll tables for fixing top alignment when using scrollTo method
    :param virtual_scroll_sticky_size_end: Size in pixels of the sticky footer part (if using one); A correct value will improve scroll precision
    :param table_colspan: The number of columns in the table (you need this if you use table-layout: fixed)
    :param color: Color name for component from the Quasar Color Palette
    :param icon_first_page: Icon name following Quasar convention for stepping to first page; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param icon_prev_page: Icon name following Quasar convention for stepping to previous page; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param icon_next_page: Icon name following Quasar convention for stepping to next page; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param icon_last_page: Icon name following Quasar convention for stepping to last page; Make sure you have the icon library installed unless you are using 'img:' prefix
    :param grid: Display data as a grid instead of the default table
    :param grid_header: Display header for grid-mode also
    :param dense: Dense mode; Connect with $q.screen for responsive behavior
    :param columns: The column definitions (Array of Objects)
    :param visible_columns: Array of Strings defining column names ('name' property of each column from 'columns' prop definitions); Columns marked as 'required' are not affected by this property
    :param loading: Put Table into 'loading' state; Notify the user something is happening behind the scenes
    :param title: Table title
    :param hide_header: Hide table header layer
    :param hide_bottom: Hide table bottom layer regardless of what it has to display
    :param hide_selected_banner: Hide the selected rows banner (if any)
    :param hide_no_data: Hide the default no data bottom layer
    :param hide_pagination: Hide the pagination controls at the bottom
    :param dark: Notify the component that the background is a dark color
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param square: Removes border-radius so borders are squared
    :param separator: Use a separator/border between rows, columns or all cells
    :param wrap_cells: Wrap text within table cells
    :param binary_state_sort: Skip the third state (unsorted) when user toggles column sort direction
    :param column_sort_order: Set column sort order: 'ad' (ascending-descending) or 'da' (descending-ascending); It gets applied to all columns unless a column has its own sortOrder specified in the 'columns' definition prop
    :param no_data_label: Override default text to display when no data is available
    :param no_results_label: Override default text to display when user filters the table and no matched results are found
    :param loading_label: Override default text to display when table is in loading state (see 'loading' prop)
    :param selected_rows_label: Text to display when user selected at least one row; For best performance, reference it from your scope and do not define it inline
    :param rows_per_page_label: Text to override default rows per page label at bottom of table
    :param pagination_label: Text to override default pagination label at bottom of table (unless 'pagination' scoped slot is used); For best performance, reference it from your scope and do not define it inline
    :param table_style: CSS style to apply to native HTML <table> element's wrapper (which is a DIV)
    :param table_class: CSS classes to apply to native HTML <table> element's wrapper (which is a DIV)
    :param table_header_style: CSS style to apply to header of native HTML <table> (which is a TR)
    :param table_header_class: CSS classes to apply to header of native HTML <table> (which is a TR)
    :param card_container_style: CSS style to apply to the cards container (when in grid mode)
    :param card_container_class: CSS classes to apply to the cards container (when in grid mode)
    :param card_style: CSS style to apply to the card (when in grid mode) or container card (when not in grid mode)
    :param card_class: CSS classes to apply to the card (when in grid mode) or container card (when not in grid mode)
    :param title_class: CSS classes to apply to the title (if using 'title' prop)
    :param filter: String/Object to filter table with; When using an Object it requires 'filter-method' to also be specified since it will be a custom filtering
    :param filter_method: The actual filtering mechanism; For best performance, reference it from your scope and do not define it inline
    :param pagination: Pagination object; You can also use the 'v-model:pagination' for synching; When not synching it simply initializes the pagination on first render
    :param rows_per_page_options: Options for user to pick (Numbers); Number 0 means 'Show all rows in one page'
    :param selection: Selection type
    :param selected: Keeps the user selection array
    :param expanded: Keeps the array with expanded rows keys
    :param sort_method: The actual sort mechanism. Function (rows, sortBy, descending) => sorted rows; For best performance, reference it from your scope and do not define it inline
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-table", children, **kwargs)
        self._attr_names += [
            "fullscreen",
            "no_route_fullscreen_exit",
            "rows",
            "row_key",
            "virtual_scroll",
            "virtual_scroll_target",
            "virtual_scroll_slice_size",
            "virtual_scroll_slice_ratio_before",
            "virtual_scroll_slice_ratio_after",
            "virtual_scroll_item_size",
            "virtual_scroll_sticky_size_start",
            "virtual_scroll_sticky_size_end",
            "table_colspan",
            "color",
            "icon_first_page",
            "icon_prev_page",
            "icon_next_page",
            "icon_last_page",
            "grid",
            "grid_header",
            "dense",
            "columns",
            "visible_columns",
            "loading",
            "title",
            "hide_header",
            "hide_bottom",
            "hide_selected_banner",
            "hide_no_data",
            "hide_pagination",
            "dark",
            "flat",
            "bordered",
            "square",
            "separator",
            "wrap_cells",
            "binary_state_sort",
            "column_sort_order",
            "no_data_label",
            "no_results_label",
            "loading_label",
            "selected_rows_label",
            "rows_per_page_label",
            "pagination_label",
            "table_style",
            "table_class",
            "table_header_style",
            "table_header_class",
            "card_container_style",
            "card_container_class",
            "card_style",
            "card_class",
            "title_class",
            "filter",
            "filter_method",
            "pagination",
            "rows_per_page_options",
            "selection",
            "selected",
            "expanded",
            "sort_method",
        ]
        self._event_names += [
            "fullscreen",
            "row_click",
            "row_dblclick",
            "row_contextmenu",
            "request",
            "selection",
            ("update_pagination", "update:pagination"),
            ("update_selected", "update:selected"),
            ("update_expanded", "update:expanded"),
            "virtual_scroll",
        ]


class QTabs(HtmlElement):
    """
    Properties

    :param model_value: Model of the component defining current panel name; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param vertical: Use vertical design (tabs one on top of each other rather than one next to the other horizontally)
    :param outside_arrows: Reserve space for arrows to place them on each side of the tabs (the arrows fade when inactive)
    :param mobile_arrows: Force display of arrows (if needed) on mobile
    :param align: Horizontal alignment the tabs within the tabs container
    :param breakpoint: Breakpoint (in pixels) of tabs container width at which the tabs automatically turn to a justify alignment
    :param active_color: The color to be attributed to the text of the active tab
    :param active_bg_color: The color to be attributed to the background of the active tab
    :param indicator_color: The color to be attributed to the indicator (the underline) of the active tab
    :param content_class: Class definitions to be attributed to the content wrapper
    :param active_class: The class to be set on the active tab
    :param left_icon: The name of an icon to replace the default arrow used to scroll through the tabs to the left, when the tabs extend past the width of the tabs container
    :param right_icon: The name of an icon to replace the default arrow used to scroll through the tabs to the right, when the tabs extend past the width of the tabs container
    :param stretch: When used on flexbox parent, tabs will stretch to parent's height
    :param shrink: By default, QTabs is set to grow to the available space; However, you can reverse that with this prop; Useful (and required) when placing the component in a QToolbar
    :param switch_indicator: Switches the indicator position (on left of tab for vertical mode or above the tab for default horizontal mode)
    :param narrow_indicator: Allows the indicator to be the same width as the tab's content (text or icon), instead of the whole width of the tab
    :param inline_label: Allows the text to be inline with the icon, should one be used
    :param no_caps: Turns off capitalizing all letters within the tab (which is the default)
    :param dense: Dense mode; occupies less space

    Events

    :param model_value: Model of the component defining current panel name; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param vertical: Use vertical design (tabs one on top of each other rather than one next to the other horizontally)
    :param outside_arrows: Reserve space for arrows to place them on each side of the tabs (the arrows fade when inactive)
    :param mobile_arrows: Force display of arrows (if needed) on mobile
    :param align: Horizontal alignment the tabs within the tabs container
    :param breakpoint: Breakpoint (in pixels) of tabs container width at which the tabs automatically turn to a justify alignment
    :param active_color: The color to be attributed to the text of the active tab
    :param active_bg_color: The color to be attributed to the background of the active tab
    :param indicator_color: The color to be attributed to the indicator (the underline) of the active tab
    :param content_class: Class definitions to be attributed to the content wrapper
    :param active_class: The class to be set on the active tab
    :param left_icon: The name of an icon to replace the default arrow used to scroll through the tabs to the left, when the tabs extend past the width of the tabs container
    :param right_icon: The name of an icon to replace the default arrow used to scroll through the tabs to the right, when the tabs extend past the width of the tabs container
    :param stretch: When used on flexbox parent, tabs will stretch to parent's height
    :param shrink: By default, QTabs is set to grow to the available space; However, you can reverse that with this prop; Useful (and required) when placing the component in a QToolbar
    :param switch_indicator: Switches the indicator position (on left of tab for vertical mode or above the tab for default horizontal mode)
    :param narrow_indicator: Allows the indicator to be the same width as the tab's content (text or icon), instead of the whole width of the tab
    :param inline_label: Allows the text to be inline with the icon, should one be used
    :param no_caps: Turns off capitalizing all letters within the tab (which is the default)
    :param dense: Dense mode; occupies less space
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-tabs", children, **kwargs)
        self._attr_names += [
            "model_value",
            "vertical",
            "outside_arrows",
            "mobile_arrows",
            "align",
            "breakpoint",
            "active_color",
            "active_bg_color",
            "indicator_color",
            "content_class",
            "active_class",
            "left_icon",
            "right_icon",
            "stretch",
            "shrink",
            "switch_indicator",
            "narrow_indicator",
            "inline_label",
            "no_caps",
            "dense",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
        ]


class QTd(HtmlElement):
    """
    Properties

    :param props: QTable's column scoped slot property
    :param auto_width: Tries to shrink column width size; Useful for columns with a checkbox/radio/toggle
    :param no_hover: Disable hover effect

    Events

    :param props: QTable's column scoped slot property
    :param auto_width: Tries to shrink column width size; Useful for columns with a checkbox/radio/toggle
    :param no_hover: Disable hover effect
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-td", children, **kwargs)
        self._attr_names += [
            "props",
            "auto_width",
            "no_hover",
        ]
        self._event_names += [
        ]


class QTh(HtmlElement):
    """
    Properties

    :param props: QTable's header column scoped slot property
    :param auto_width: Tries to shrink header column width size; Useful for columns with a checkbox/radio/toggle

    Events

    :param props: QTable's header column scoped slot property
    :param auto_width: Tries to shrink header column width size; Useful for columns with a checkbox/radio/toggle
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-th", children, **kwargs)
        self._attr_names += [
            "props",
            "auto_width",
        ]
        self._event_names += [
        ]


class QTime(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param landscape: Display the component in landscape mode
    :param mask: Mask (formatting string) used for parsing and formatting value
    :param locale: Locale formatting options
    :param calendar: Specify calendar type
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param readonly: Put component in readonly mode
    :param disable: Put component in disabled mode
    :param model_value: Time of the component; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param format24h: Forces 24 hour time display instead of AM/PM system
    :param default_date: The default date to use (in YYYY/MM/DD format) when model is unfilled (undefined or null)
    :param options: Optionally configure what time is the user allowed to set; Overridden by 'hour-options', 'minute-options' and 'second-options' if those are set; For best performance, reference it from your scope and do not define it inline
    :param hour_options: Optionally configure what hours is the user allowed to set; Overrides 'options' prop if that is also set
    :param minute_options: Optionally configure what minutes is the user allowed to set; Overrides 'options' prop if that is also set
    :param second_options: Optionally configure what seconds is the user allowed to set; Overrides 'options' prop if that is also set
    :param with_seconds: Allow the time to be set with seconds
    :param now_btn: Display a button that selects the current time

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param landscape: Display the component in landscape mode
    :param mask: Mask (formatting string) used for parsing and formatting value
    :param locale: Locale formatting options
    :param calendar: Specify calendar type
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param readonly: Put component in readonly mode
    :param disable: Put component in disabled mode
    :param model_value: Time of the component; Either use this property (along with a listener for 'update:modelValue' event) OR use v-model directive
    :param format24h: Forces 24 hour time display instead of AM/PM system
    :param default_date: The default date to use (in YYYY/MM/DD format) when model is unfilled (undefined or null)
    :param options: Optionally configure what time is the user allowed to set; Overridden by 'hour-options', 'minute-options' and 'second-options' if those are set; For best performance, reference it from your scope and do not define it inline
    :param hour_options: Optionally configure what hours is the user allowed to set; Overrides 'options' prop if that is also set
    :param minute_options: Optionally configure what minutes is the user allowed to set; Overrides 'options' prop if that is also set
    :param second_options: Optionally configure what seconds is the user allowed to set; Overrides 'options' prop if that is also set
    :param with_seconds: Allow the time to be set with seconds
    :param now_btn: Display a button that selects the current time
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-time", children, **kwargs)
        self._attr_names += [
            "name",
            "landscape",
            "mask",
            "locale",
            "calendar",
            "color",
            "text_color",
            "dark",
            "square",
            "flat",
            "bordered",
            "readonly",
            "disable",
            "model_value",
            "format24h",
            "default_date",
            "options",
            "hour_options",
            "minute_options",
            "second_options",
            "with_seconds",
            "now_btn",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
        ]


class QTimeline(HtmlElement):
    """
    Properties

    :param color: Color name for component from the Quasar Color Palette
    :param side: Side to place the timeline entries in dense and comfortable layout; For loose layout it gets overridden by QTimelineEntry side prop
    :param layout: Layout of the timeline. Dense keeps content and labels on one side. Comfortable keeps content on one side and labels on the opposite side. Loose puts content on both sides.
    :param dark: Notify the component that the background is a dark color

    Events

    :param color: Color name for component from the Quasar Color Palette
    :param side: Side to place the timeline entries in dense and comfortable layout; For loose layout it gets overridden by QTimelineEntry side prop
    :param layout: Layout of the timeline. Dense keeps content and labels on one side. Comfortable keeps content on one side and labels on the opposite side. Loose puts content on both sides.
    :param dark: Notify the component that the background is a dark color
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-timeline", children, **kwargs)
        self._attr_names += [
            "color",
            "side",
            "layout",
            "dark",
        ]
        self._event_names += [
        ]


class QTimelineEntry(HtmlElement):
    """
    Properties

    :param heading: Defines a heading timeline item
    :param tag: Tag to use, if of type 'heading' only
    :param side: Side to place the timeline entry; Works only if QTimeline layout is loose.
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param avatar: URL to the avatar image; Icon takes precedence if used, so it replaces avatar
    :param color: Color name for component from the Quasar Color Palette
    :param title: Title of timeline entry; Is overridden if using 'title' slot
    :param subtitle: Subtitle of timeline entry; Is overridden if using 'subtitle' slot
    :param body: Body content of timeline entry; Use this prop or the default slot

    Events

    :param heading: Defines a heading timeline item
    :param tag: Tag to use, if of type 'heading' only
    :param side: Side to place the timeline entry; Works only if QTimeline layout is loose.
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param avatar: URL to the avatar image; Icon takes precedence if used, so it replaces avatar
    :param color: Color name for component from the Quasar Color Palette
    :param title: Title of timeline entry; Is overridden if using 'title' slot
    :param subtitle: Subtitle of timeline entry; Is overridden if using 'subtitle' slot
    :param body: Body content of timeline entry; Use this prop or the default slot
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-timeline-entry", children, **kwargs)
        self._attr_names += [
            "heading",
            "tag",
            "side",
            "icon",
            "avatar",
            "color",
            "title",
            "subtitle",
            "body",
        ]
        self._event_names += [
        ]


class QToggle(HtmlElement):
    """
    Properties

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param val: Works when model ('value') is Array. It tells the component which value should add/remove when ticked/unticked
    :param true_value: What model value should be considered as checked/ticked/on?
    :param false_value: What model value should be considered as unchecked/unticked/off?
    :param indeterminate_value: What model value should be considered as 'indeterminate'?
    :param toggle_order: Determines toggle order of the two states ('t' stands for state of true, 'f' for state of false); If 'toggle-indeterminate' is true, then the order is: indet -> first state -> second state -> indet (and repeat), otherwise: indet -> first state -> second state -> first state -> second state -> ...
    :param toggle_indeterminate: When user clicks/taps on the component, should we toggle through the indeterminate state too?
    :param label: Label to display along the component (or use the default slot instead of this prop)
    :param left_label: Label (if any specified) should be displayed on the left side of the component
    :param checked_icon: The icon to be used when the toggle is on
    :param unchecked_icon: The icon to be used when the toggle is off
    :param indeterminate_icon: The icon to be used when the model is indeterminate
    :param color: Color name for component from the Quasar Color Palette
    :param keep_color: Should the color (if specified any) be kept when the component is unticked/ off?
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param disable: Put component in disabled mode
    :param tabindex: Tabindex HTML attribute value
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_color: Override default icon color (for truthy state only); Color name for component from the Quasar Color Palette

    Events

    :param name: Used to specify the name of the control; Useful if dealing with forms submitted directly to a URL
    :param size: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)
    :param model_value: Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param val: Works when model ('value') is Array. It tells the component which value should add/remove when ticked/unticked
    :param true_value: What model value should be considered as checked/ticked/on?
    :param false_value: What model value should be considered as unchecked/unticked/off?
    :param indeterminate_value: What model value should be considered as 'indeterminate'?
    :param toggle_order: Determines toggle order of the two states ('t' stands for state of true, 'f' for state of false); If 'toggle-indeterminate' is true, then the order is: indet -> first state -> second state -> indet (and repeat), otherwise: indet -> first state -> second state -> first state -> second state -> ...
    :param toggle_indeterminate: When user clicks/taps on the component, should we toggle through the indeterminate state too?
    :param label: Label to display along the component (or use the default slot instead of this prop)
    :param left_label: Label (if any specified) should be displayed on the left side of the component
    :param checked_icon: The icon to be used when the toggle is on
    :param unchecked_icon: The icon to be used when the toggle is off
    :param indeterminate_icon: The icon to be used when the model is indeterminate
    :param color: Color name for component from the Quasar Color Palette
    :param keep_color: Should the color (if specified any) be kept when the component is unticked/ off?
    :param dark: Notify the component that the background is a dark color
    :param dense: Dense mode; occupies less space
    :param disable: Put component in disabled mode
    :param tabindex: Tabindex HTML attribute value
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param icon_color: Override default icon color (for truthy state only); Color name for component from the Quasar Color Palette
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-toggle", children, **kwargs)
        self._attr_names += [
            "name",
            "size",
            "model_value",
            "val",
            "true_value",
            "false_value",
            "indeterminate_value",
            "toggle_order",
            "toggle_indeterminate",
            "label",
            "left_label",
            "checked_icon",
            "unchecked_icon",
            "indeterminate_icon",
            "color",
            "keep_color",
            "dark",
            "dense",
            "disable",
            "tabindex",
            "icon",
            "icon_color",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
        ]


class QToolbar(HtmlElement):
    """
    Properties

    :param inset: Apply an inset to content (useful for subsequent toolbars)

    Events

    :param inset: Apply an inset to content (useful for subsequent toolbars)
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-toolbar", children, **kwargs)
        self._attr_names += [
            "inset",
        ]
        self._event_names += [
        ]


class QToolbarTitle(HtmlElement):
    """
    Properties

    :param shrink: By default, QToolbarTitle is set to grow to the available space. However, you can reverse that with this prop

    Events

    :param shrink: By default, QToolbarTitle is set to grow to the available space. However, you can reverse that with this prop
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-toolbar-title", children, **kwargs)
        self._attr_names += [
            "shrink",
        ]
        self._event_names += [
        ]


class QTooltip(HtmlElement):
    """
    Properties

    :param transition_show: One of Quasar's embedded transitions
    :param transition_hide: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param model_value: Model of the component defining shown/hidden state; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param max_height: The maximum height of the Tooltip; Size in CSS units, including unit name
    :param max_width: The maximum width of the Tooltip; Size in CSS units, including unit name
    :param anchor: Two values setting the starting position or anchor point of the Tooltip relative to its target
    :param self: Two values setting the Tooltip's own position relative to its target
    :param offset: An array of two numbers to offset the Tooltip horizontally and vertically in pixels
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    :param target: Configure a target element to trigger Tooltip toggle; 'true' means it enables the parent DOM element, 'false' means it disables attaching events to any DOM elements; By using a String (CSS selector) it attaches the events to the specified DOM element (if it exists)
    :param no_parent_event: Skips attaching events to the target DOM element (that trigger the element to get shown)
    :param delay: Configure Tooltip to appear with delay
    :param hide_delay: Configure Tooltip to disappear with delay

    Events

    :param transition_show: One of Quasar's embedded transitions
    :param transition_hide: One of Quasar's embedded transitions
    :param transition_duration: Transition duration (in milliseconds, without unit)
    :param model_value: Model of the component defining shown/hidden state; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive
    :param max_height: The maximum height of the Tooltip; Size in CSS units, including unit name
    :param max_width: The maximum width of the Tooltip; Size in CSS units, including unit name
    :param anchor: Two values setting the starting position or anchor point of the Tooltip relative to its target
    :param self: Two values setting the Tooltip's own position relative to its target
    :param offset: An array of two numbers to offset the Tooltip horizontally and vertically in pixels
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    :param target: Configure a target element to trigger Tooltip toggle; 'true' means it enables the parent DOM element, 'false' means it disables attaching events to any DOM elements; By using a String (CSS selector) it attaches the events to the specified DOM element (if it exists)
    :param no_parent_event: Skips attaching events to the target DOM element (that trigger the element to get shown)
    :param delay: Configure Tooltip to appear with delay
    :param hide_delay: Configure Tooltip to disappear with delay
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-tooltip", children, **kwargs)
        self._attr_names += [
            "transition_show",
            "transition_hide",
            "transition_duration",
            "model_value",
            "max_height",
            "max_width",
            "anchor",
            "self",
            "offset",
            "scroll_target",
            "target",
            "no_parent_event",
            "delay",
            "hide_delay",
        ]
        self._event_names += [
            ("update_model_value", "update:model-value"),
            "show",
            "before_show",
            "hide",
            "before_hide",
        ]


class QTr(HtmlElement):
    """
    Properties

    :param props: QTable's row scoped slot property
    :param no_hover: Disable hover effect

    Events

    :param props: QTable's row scoped slot property
    :param no_hover: Disable hover effect
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-tr", children, **kwargs)
        self._attr_names += [
            "props",
            "no_hover",
        ]
        self._event_names += [
        ]


class QTree(HtmlElement):
    """
    Properties

    :param nodes: The array of nodes that designates the tree structure
    :param node_key: The property name of each node object that holds a unique node id
    :param label_key: The property name of each node object that holds the label of the node
    :param children_key: The property name of each node object that holds the list of children of the node
    :param no_connectors: Do not display the connector lines between nodes
    :param color: Color name for component from the Quasar Color Palette
    :param control_color: Color name for controls (like checkboxes) from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param selected_color: Color name for selected nodes (from the Quasar Color Palette)
    :param dense: Dense mode; occupies less space
    :param dark: Notify the component that the background is a dark color
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param tick_strategy: The type of strategy to use for the selection of the nodes
    :param ticked: Keys of nodes that are ticked
    :param expanded: Keys of nodes that are expanded
    :param selected: Key of node currently selected
    :param no_selection_unset: Do not allow un-selection when clicking currently selected node
    :param default_expand_all: Allow the tree to have all its branches expanded, when first rendered
    :param accordion: Allows the tree to be set in accordion mode
    :param no_transition: Turn off transition effects when expanding/collapsing nodes; Also enhances perf by a lot as a side-effect; Recommended for big trees
    :param filter: The text value to be used for filtering nodes
    :param filter_method: The function to use to filter the tree nodes; For best performance, reference it from your scope and do not define it inline
    :param duration: Toggle animation duration (in milliseconds)
    :param no_nodes_label: Override default such label for when no nodes are available
    :param no_results_label: Override default such label for when no nodes are available due to filtering

    Events

    :param nodes: The array of nodes that designates the tree structure
    :param node_key: The property name of each node object that holds a unique node id
    :param label_key: The property name of each node object that holds the label of the node
    :param children_key: The property name of each node object that holds the list of children of the node
    :param no_connectors: Do not display the connector lines between nodes
    :param color: Color name for component from the Quasar Color Palette
    :param control_color: Color name for controls (like checkboxes) from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param selected_color: Color name for selected nodes (from the Quasar Color Palette)
    :param dense: Dense mode; occupies less space
    :param dark: Notify the component that the background is a dark color
    :param icon: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)
    :param tick_strategy: The type of strategy to use for the selection of the nodes
    :param ticked: Keys of nodes that are ticked
    :param expanded: Keys of nodes that are expanded
    :param selected: Key of node currently selected
    :param no_selection_unset: Do not allow un-selection when clicking currently selected node
    :param default_expand_all: Allow the tree to have all its branches expanded, when first rendered
    :param accordion: Allows the tree to be set in accordion mode
    :param no_transition: Turn off transition effects when expanding/collapsing nodes; Also enhances perf by a lot as a side-effect; Recommended for big trees
    :param filter: The text value to be used for filtering nodes
    :param filter_method: The function to use to filter the tree nodes; For best performance, reference it from your scope and do not define it inline
    :param duration: Toggle animation duration (in milliseconds)
    :param no_nodes_label: Override default such label for when no nodes are available
    :param no_results_label: Override default such label for when no nodes are available due to filtering
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-tree", children, **kwargs)
        self._attr_names += [
            "nodes",
            "node_key",
            "label_key",
            "children_key",
            "no_connectors",
            "color",
            "control_color",
            "text_color",
            "selected_color",
            "dense",
            "dark",
            "icon",
            "tick_strategy",
            "ticked",
            "expanded",
            "selected",
            "no_selection_unset",
            "default_expand_all",
            "accordion",
            "no_transition",
            "filter",
            "filter_method",
            "duration",
            "no_nodes_label",
            "no_results_label",
        ]
        self._event_names += [
            ("update_expanded", "update:expanded"),
            "lazy_load",
            ("update_ticked", "update:ticked"),
            ("update_selected", "update:selected"),
            "after_show",
            "after_hide",
        ]


class QUploader(HtmlElement):
    """
    Properties

    :param factory: Function which should return an Object or a Promise resolving with an Object; For best performance, reference it from your scope and do not define it inline
    :param url: URL or path to the server which handles the upload. Takes String or factory function, which returns String. Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param method: HTTP method to use for upload; Takes String or factory function which returns a String; Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param field_name: Field name for each file upload; This goes into the following header: 'Content-Disposition: form-data; name="__HERE__"; filename="somefile.png"; If using a function then for best performance, reference it from your scope and do not define it inline
    :param headers: Array or a factory function which returns an array; Array consists of objects with header definitions; Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param form_fields: Array or a factory function which returns an array; Array consists of objects with additional fields definitions (used by Form to be uploaded); Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param with_credentials: Sets withCredentials to true on the XHR that manages the upload; Takes boolean or factory function for Boolean; Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param send_raw: Send raw files without wrapping into a Form(); Takes boolean or factory function for Boolean; Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param batch: Upload files in batch (in one XHR request); Takes boolean or factory function for Boolean; Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param multiple: Allow multiple file uploads
    :param accept: Comma separated list of unique file type specifiers. Maps to 'accept' attribute of native input type=file element
    :param capture: Optionally, specify that a new file should be captured, and which device should be used to capture that new media of a type defined by the 'accept' prop. Maps to 'capture' attribute of native input type=file element
    :param max_file_size: Maximum size of individual file in bytes
    :param max_total_size: Maximum size of all files combined in bytes
    :param max_files: Maximum number of files to contain
    :param filter: Custom filter for added files; Only files that pass this filter will be added to the queue and uploaded; For best performance, reference it from your scope and do not define it inline
    :param label: Label for the uploader
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param no_thumbnails: Don't display thumbnails for image files
    :param auto_upload: Upload files immediately when added
    :param hide_upload_btn: Don't show the upload button
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode

    Events

    :param factory: Function which should return an Object or a Promise resolving with an Object; For best performance, reference it from your scope and do not define it inline
    :param url: URL or path to the server which handles the upload. Takes String or factory function, which returns String. Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param method: HTTP method to use for upload; Takes String or factory function which returns a String; Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param field_name: Field name for each file upload; This goes into the following header: 'Content-Disposition: form-data; name="__HERE__"; filename="somefile.png"; If using a function then for best performance, reference it from your scope and do not define it inline
    :param headers: Array or a factory function which returns an array; Array consists of objects with header definitions; Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param form_fields: Array or a factory function which returns an array; Array consists of objects with additional fields definitions (used by Form to be uploaded); Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param with_credentials: Sets withCredentials to true on the XHR that manages the upload; Takes boolean or factory function for Boolean; Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param send_raw: Send raw files without wrapping into a Form(); Takes boolean or factory function for Boolean; Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param batch: Upload files in batch (in one XHR request); Takes boolean or factory function for Boolean; Function is called right before upload; If using a function then for best performance, reference it from your scope and do not define it inline
    :param multiple: Allow multiple file uploads
    :param accept: Comma separated list of unique file type specifiers. Maps to 'accept' attribute of native input type=file element
    :param capture: Optionally, specify that a new file should be captured, and which device should be used to capture that new media of a type defined by the 'accept' prop. Maps to 'capture' attribute of native input type=file element
    :param max_file_size: Maximum size of individual file in bytes
    :param max_total_size: Maximum size of all files combined in bytes
    :param max_files: Maximum number of files to contain
    :param filter: Custom filter for added files; Only files that pass this filter will be added to the queue and uploaded; For best performance, reference it from your scope and do not define it inline
    :param label: Label for the uploader
    :param color: Color name for component from the Quasar Color Palette
    :param text_color: Overrides text color (if needed); Color name from the Quasar Color Palette
    :param dark: Notify the component that the background is a dark color
    :param square: Removes border-radius so borders are squared
    :param flat: Applies a 'flat' design (no default shadow)
    :param bordered: Applies a default border to the component
    :param no_thumbnails: Don't display thumbnails for image files
    :param auto_upload: Upload files immediately when added
    :param hide_upload_btn: Don't show the upload button
    :param disable: Put component in disabled mode
    :param readonly: Put component in readonly mode
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-uploader", children, **kwargs)
        self._attr_names += [
            "factory",
            "url",
            "method",
            "field_name",
            "headers",
            "form_fields",
            "with_credentials",
            "send_raw",
            "batch",
            "multiple",
            "accept",
            "capture",
            "max_file_size",
            "max_total_size",
            "max_files",
            "filter",
            "label",
            "color",
            "text_color",
            "dark",
            "square",
            "flat",
            "bordered",
            "no_thumbnails",
            "auto_upload",
            "hide_upload_btn",
            "disable",
            "readonly",
        ]
        self._event_names += [
            "uploaded",
            "failed",
            "uploading",
            "factory_failed",
            "rejected",
            "added",
            "removed",
            "start",
            "finish",
        ]


class QUploaderAddTrigger(HtmlElement):
    """
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-uploader-add-trigger", children, **kwargs)
        self._attr_names += [
        ]
        self._event_names += [
        ]


class QVideo(HtmlElement):
    """
    Properties

    :param ratio: Aspect ratio for the content; If value is a String, then avoid using a computational statement (like '16/9') and instead specify the String value of the result directly (eg. '1.7777')
    :param src: The source url to display in an iframe
    :param title: (Accessibility) Set the native 'title' attribute value of the inner iframe being used
    :param fetchpriority: Provides a hint of the relative priority to use when fetching the iframe document
    :param loading: Indicates how the browser should load the iframe
    :param referrerpolicy: Indicates which referrer to send when fetching the frame's resource

    Events

    :param ratio: Aspect ratio for the content; If value is a String, then avoid using a computational statement (like '16/9') and instead specify the String value of the result directly (eg. '1.7777')
    :param src: The source url to display in an iframe
    :param title: (Accessibility) Set the native 'title' attribute value of the inner iframe being used
    :param fetchpriority: Provides a hint of the relative priority to use when fetching the iframe document
    :param loading: Indicates how the browser should load the iframe
    :param referrerpolicy: Indicates which referrer to send when fetching the frame's resource
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-video", children, **kwargs)
        self._attr_names += [
            "ratio",
            "src",
            "title",
            "fetchpriority",
            "loading",
            "referrerpolicy",
        ]
        self._event_names += [
        ]


class QVirtualScroll(HtmlElement):
    """
    Properties

    :param virtual_scroll_horizontal: Make virtual list work in horizontal mode
    :param virtual_scroll_slice_size: Minimum number of items to render in the virtual list
    :param virtual_scroll_slice_ratio_before: Ratio of number of items in visible zone to render before it
    :param virtual_scroll_slice_ratio_after: Ratio of number of items in visible zone to render after it
    :param virtual_scroll_item_size: Default size in pixels (height if vertical, width if horizontal) of an item; This value is used for rendering the initial list; Try to use a value close to the minimum size of an item
    :param virtual_scroll_sticky_size_start: Size in pixels (height if vertical, width if horizontal) of the sticky part (if using one) at the start of the list; A correct value will improve scroll precision
    :param virtual_scroll_sticky_size_end: Size in pixels (height if vertical, width if horizontal) of the sticky part (if using one) at the end of the list; A correct value will improve scroll precision
    :param table_colspan: The number of columns in the table (you need this if you use table-layout: fixed)
    :param type: The type of content: list (default) or table
    :param items: Available list items that will be passed to the scoped slot; For best performance freeze the list of items; Required if 'itemsFn' is not supplied
    :param items_size: Number of available items in the list; Required and used only if 'itemsFn' is provided
    :param items_fn: Function to return the scope for the items to be displayed; Should return an array for items starting from 'from' index for size length; For best performance, reference it from your scope and do not define it inline
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one

    Events

    :param virtual_scroll_horizontal: Make virtual list work in horizontal mode
    :param virtual_scroll_slice_size: Minimum number of items to render in the virtual list
    :param virtual_scroll_slice_ratio_before: Ratio of number of items in visible zone to render before it
    :param virtual_scroll_slice_ratio_after: Ratio of number of items in visible zone to render after it
    :param virtual_scroll_item_size: Default size in pixels (height if vertical, width if horizontal) of an item; This value is used for rendering the initial list; Try to use a value close to the minimum size of an item
    :param virtual_scroll_sticky_size_start: Size in pixels (height if vertical, width if horizontal) of the sticky part (if using one) at the start of the list; A correct value will improve scroll precision
    :param virtual_scroll_sticky_size_end: Size in pixels (height if vertical, width if horizontal) of the sticky part (if using one) at the end of the list; A correct value will improve scroll precision
    :param table_colspan: The number of columns in the table (you need this if you use table-layout: fixed)
    :param type: The type of content: list (default) or table
    :param items: Available list items that will be passed to the scoped slot; For best performance freeze the list of items; Required if 'itemsFn' is not supplied
    :param items_size: Number of available items in the list; Required and used only if 'itemsFn' is provided
    :param items_fn: Function to return the scope for the items to be displayed; Should return an array for items starting from 'from' index for size length; For best performance, reference it from your scope and do not define it inline
    :param scroll_target: CSS selector or DOM element to be used as a custom scroll container instead of the auto detected one
    """
    def __init__(self, children=None, **kwargs):
        super().__init__("q-virtual-scroll", children, **kwargs)
        self._attr_names += [
            "virtual_scroll_horizontal",
            "virtual_scroll_slice_size",
            "virtual_scroll_slice_ratio_before",
            "virtual_scroll_slice_ratio_after",
            "virtual_scroll_item_size",
            "virtual_scroll_sticky_size_start",
            "virtual_scroll_sticky_size_end",
            "table_colspan",
            "type",
            "items",
            "items_size",
            "items_fn",
            "scroll_target",
        ]
        self._event_names += [
            "virtual_scroll",
        ]


AbstractElement.register_directive("v-touch-hold")
AbstractElement.register_directive("v-intersection")
AbstractElement.register_directive("v-touch-swipe")
AbstractElement.register_directive("v-scroll-fire")
AbstractElement.register_directive("v-touch-repeat")
AbstractElement.register_directive("v-close-popup")
AbstractElement.register_directive("v-touch-pan")
AbstractElement.register_directive("v-scroll")
AbstractElement.register_directive("v-mutation")
AbstractElement.register_directive("v-morph")
AbstractElement.register_directive("v-ripple")


__all__ = [
    "QAjaxBar",
    "QAvatar",
    "QBadge",
    "QBanner",
    "QBar",
    "QBreadcrumbs",
    "QBreadcrumbsEl",
    "QBtn",
    "QBtnDropdown",
    "QBtnGroup",
    "QBtnToggle",
    "QCard",
    "QCardActions",
    "QCardSection",
    "QCarousel",
    "QCarouselControl",
    "QCarouselSlide",
    "QChatMessage",
    "QCheckbox",
    "QChip",
    "QCircularProgress",
    "QColor",
    "QDate",
    "QDialog",
    "QDrawer",
    "QEditor",
    "QExpansionItem",
    "QFab",
    "QFabAction",
    "QField",
    "QFile",
    "QFooter",
    "QForm",
    "QFormChildMixin",
    "QHeader",
    "QIcon",
    "QImg",
    "QInfiniteScroll",
    "QInnerLoading",
    "QInput",
    "QIntersection",
    "QItem",
    "QItemLabel",
    "QItemSection",
    "QKnob",
    "QLayout",
    "QLinearProgress",
    "QList",
    "QMarkupTable",
    "QMenu",
    "QNoSsr",
    "QOptionGroup",
    "QPage",
    "QPageContainer",
    "QPageScroller",
    "QPageSticky",
    "QPagination",
    "QParallax",
    "QPopupEdit",
    "QPopupProxy",
    "QPullToRefresh",
    "QRadio",
    "QRange",
    "QRating",
    "QResizeObserver",
    "QResponsive",
    "QRouteTab",
    "QScrollArea",
    "QScrollObserver",
    "QSelect",
    "QSeparator",
    "QSkeleton",
    "QSlideItem",
    "QSlideTransition",
    "QSlider",
    "QSpace",
    "QSpinner",
    "QSpinnerAudio",
    "QSpinnerBall",
    "QSpinnerBars",
    "QSpinnerBox",
    "QSpinnerClock",
    "QSpinnerComment",
    "QSpinnerCube",
    "QSpinnerDots",
    "QSpinnerFacebook",
    "QSpinnerGears",
    "QSpinnerGrid",
    "QSpinnerHearts",
    "QSpinnerHourglass",
    "QSpinnerInfinity",
    "QSpinnerIos",
    "QSpinnerOrbit",
    "QSpinnerOval",
    "QSpinnerPie",
    "QSpinnerPuff",
    "QSpinnerRadio",
    "QSpinnerRings",
    "QSpinnerTail",
    "QSplitter",
    "QStep",
    "QStepper",
    "QStepperNavigation",
    "QTab",
    "QTabPanel",
    "QTabPanels",
    "QTable",
    "QTabs",
    "QTd",
    "QTh",
    "QTime",
    "QTimeline",
    "QTimelineEntry",
    "QToggle",
    "QToolbar",
    "QToolbarTitle",
    "QTooltip",
    "QTr",
    "QTree",
    "QUploader",
    "QUploaderAddTrigger",
    "QVideo",
    "QVirtualScroll",
]
