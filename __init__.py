bl_info = {
    "name":         "Rigify Generate and Edit",
    "description":  "Scripting tools to automate Rigify generation",
    "author":       "Hilth'kess",
    "blender":      (4, 0, 0),
    "version":      (1, 0, 0, 'α', 0),
    "tracker_url":  "https://github.com/hiltkess/RigEdit/issues",
    "category":     "Rigging",
}

import bpy

# the following two functions will be overwritten later, as long as everything looks good!
def register():   pass
def unregister(): pass


if bpy.app.background:
    print("Rigify Generate and Edit __init__ - is background")

elif bpy.app.version < bl_info['blender']:
    print("Rigify Generate and Edit __init__ - wrong app version")

else:
    from . import rigify_generate_and_edit
    def register():
        rigify_generate_and_edit.register()
    def unregister():
        rigify_generate_and_edit.unregister()

