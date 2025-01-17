# SPDX-License-Identifier: GPL-2.0-or-later

from .gi_composites import GtkTemplate

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject, Gtk  # noqa


@GtkTemplate(ui="/org/freedesktop/Piper/ui/ProfileRow.ui")
class ProfileRow(Gtk.ListBoxRow):
    """A Gtk.ListBoxRow subclass containing the widgets to display a profile in
    the profile poper."""

    __gtype_name__ = "ProfileRow"

    title = GtkTemplate.Child()

    def __init__(self, profile, *args, **kwargs):
        Gtk.ListBoxRow.__init__(self, *args, **kwargs)
        self.init_template()
        self._profile = profile
        self._profile.connect("notify::enabled", self._on_profile_notify_enabled)

        name = profile.name
        if not name:
            name = 'Profile {}'.format(profile.index)

        self.title.set_text(name)
        self.show_all()
        self.set_visible(not profile.disabled)

    def _on_profile_notify_enabled(self, profile, pspec):
        self.set_visible(not profile.disabled)

    @GtkTemplate.Callback
    def _on_delete_button_clicked(self, button):
        self._profile.disabled = True

    def set_active(self):
        """Activates the profile paired with this row."""
        self._profile.set_active()

    @GObject.Property
    def name(self):
        return self.title.get_text()
