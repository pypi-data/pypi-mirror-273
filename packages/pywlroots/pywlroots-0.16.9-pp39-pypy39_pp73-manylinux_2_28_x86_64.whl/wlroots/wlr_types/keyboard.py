# Copyright Sean Vig (c) 2020

from __future__ import annotations

import enum
from weakref import WeakKeyDictionary

from pywayland.protocol.wayland import WlKeyboard
from pywayland.server import Signal

from wlroots import Ptr, PtrHasData, ffi, lib
from wlroots.wlr_types.input_device import InputDevice

_weakkeydict: WeakKeyDictionary = WeakKeyDictionary()


@enum.unique
class KeyboardLed(enum.IntFlag):
    NUM_LOCK = lib.WLR_LED_NUM_LOCK
    CAPS_LOCK = lib.WLR_LED_CAPS_LOCK
    SCROLL_LOCK = lib.WLR_LED_SCROLL_LOCK


@enum.unique
class KeyboardModifier(enum.IntFlag):
    SHIFT = lib.WLR_MODIFIER_SHIFT
    CAPS = lib.WLR_MODIFIER_CAPS
    CTRL = lib.WLR_MODIFIER_CTRL
    ALT = lib.WLR_MODIFIER_ALT
    MOD2 = lib.WLR_MODIFIER_MOD2
    MOD3 = lib.WLR_MODIFIER_MOD3
    LOGO = lib.WLR_MODIFIER_LOGO
    MOD5 = lib.WLR_MODIFIER_MOD5


class ModifiersMask:
    def __init__(self, keyboard: Keyboard) -> None:
        """The modifiers mask"""
        self._mask = ffi.new("xkb_mod_mask_t *", 0)
        self._one = ffi.new("uint32_t *", 1)
        self._keyboard = keyboard

    def add(self, modifier: str) -> None:
        """Add a modifier to the mask
        Numlock is Mod2 and Capslock is Lock
        """
        idx = ffi.new("xkb_mod_index_t *")
        idx[0] = lib.xkb_keymap_mod_get_index(
            self._keyboard._ptr.keymap,
            ffi.new("const char []", modifier.encode("ascii")),
        )
        self._mask[0] |= self._one[0] << idx[0]


class KeyboardKeyEvent(Ptr):
    def __init__(self, ptr) -> None:
        """Event that a key has been pressed or release

        This event is emitted before the xkb state of the keyboard has been
        updated (including modifiers).
        """
        self._ptr = ffi.cast("struct wlr_keyboard_key_event *", ptr)

    @property
    def time_msec(self) -> int:
        """Time of the key event"""
        return self._ptr.time_msec

    @property
    def keycode(self) -> int:
        """Keycode triggering the event"""
        return self._ptr.keycode

    @property
    def update_state(self) -> bool:
        """If backend doesn't update modifiers on its own"""
        return self._ptr.update_state

    @property
    def state(self) -> WlKeyboard.key_state:
        """The state of the keycode triggering the event"""
        return WlKeyboard.key_state(self._ptr.state)


class Keyboard(PtrHasData):
    def __init__(self, ptr) -> None:
        """The Keyboard wlroots object

        :param ptr:
            The wlr_keyboard cdata pointer for the given keyboard
        """
        self._ptr = ptr

        self.key_event = Signal(
            ptr=ffi.addressof(self._ptr.events.key), data_wrapper=KeyboardKeyEvent
        )
        # The `modifiers` event signals that the modifier state of the
        # `wlr_keyboard` has been updated. At this time, you can read the
        # modifier state of the `wlr_keyboard` and handle the updated state by
        # sending it to clients.
        self.modifiers_event = Signal(ptr=ffi.addressof(self._ptr.events.modifiers))
        self.keymap_event = Signal(ptr=ffi.addressof(self._ptr.events.keymap))
        self.repeat_info_event = Signal(ptr=ffi.addressof(self._ptr.events.repeat_info))

    @property
    def base(self) -> InputDevice:
        device_ptr = ffi.addressof(self._ptr.base)
        _weakkeydict[device_ptr] = self._ptr
        return InputDevice(device_ptr)

    @classmethod
    def from_input_device(cls, input_device: InputDevice) -> Keyboard:
        ptr = lib.wlr_keyboard_from_input_device(input_device._ptr)
        return cls(ptr)

    def set_keymap(self, keymap) -> None:
        """Set the keymap associated with the keyboard"""
        lib.wlr_keyboard_set_keymap(self._ptr, keymap._keymap)

    def set_repeat_info(self, rate, delay) -> None:
        """Sets the keyboard repeat info

        :param rate:
            The keyrepeats made per second
        :param delay:
            The delay in milliseconds before repeating
        """
        lib.wlr_keyboard_set_repeat_info(self._ptr, rate, delay)

    def notify_modifiers(self, mask: ModifiersMask) -> None:
        """Notify the keyboard that modifiers have been updated"""
        zero = ffi.new("uint32_t *", 0)
        lib.wlr_keyboard_notify_modifiers(
            self._ptr, zero[0], zero[0], mask._mask[0], zero[0]
        )

    @property
    def keycodes(self):
        """Keycodes associated with the keyboard"""
        return self._ptr.keycodes

    @property
    def num_keycodes(self) -> int:
        """The number of keycodes"""
        return self._ptr.num_keycodes

    @property
    def modifiers(self) -> KeyboardModifiers:
        """The modifiers associated with the keyboard"""
        modifiers_ptr = ffi.addressof(self._ptr.modifiers)
        _weakkeydict[modifiers_ptr] = self._ptr
        return KeyboardModifiers(modifiers_ptr)

    @property
    def modifier(self) -> KeyboardModifier:
        """The enum representing the currently active modifier keys"""
        if self._ptr == ffi.NULL:
            raise RuntimeError("Tried to get modifier for NULL keyboard.")
        modifiers = lib.wlr_keyboard_get_modifiers(self._ptr)
        return KeyboardModifier(modifiers)


class KeyboardModifiers(Ptr):
    def __init__(self, ptr) -> None:
        """Modifiers of a given keyboard

        :param ptr:
            The wlr_keyboard_modifiers cdata struct.
        """
        self._ptr = ptr

    @property
    def depressed(self) -> int:
        """Depressed modifiers"""
        return self._ptr.depressed

    @property
    def latched(self) -> int:
        """Latched modifiers"""
        return self._ptr.latched

    @property
    def locked(self) -> int:
        """The locked keyboard modifiers"""
        return self._ptr.locked

    @property
    def group(self) -> int:
        """The modifier group"""
        return self._ptr.group
