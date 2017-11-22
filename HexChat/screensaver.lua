-- SPDX-License-Identifier: MIT
local lgi = require "lgi"
local Gio = lgi.Gio

hexchat.register("screensaver", "1.0", "Sets user away when the GNOME screensaver is activated")

local bus = Gio.bus_get_sync(Gio.BusType.SESSION)

local function on_active_changed(conn, sender, obj_path, interface, signal, param)
	if param[1] then
		hexchat.command("allserv away")
	else
		hexchat.command("allserv back")
	end
end

bus:signal_subscribe(nil, "org.gnome.ScreenSaver", "ActiveChanged", nil, nil,
                     Gio.DBusSignalFlags.NONE, on_active_changed)
