# Copyright (c) 2022 Samia
import os
import codecs
import csv

if "bpy" in locals():
    import importlib

    importlib.reload(plt_operator)

else:
    import bpy
    from . import plt_operator

import bpy

bl_info = {
    "name": "Petit Lattice Tools",
    "author": "Samia",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Edit Tab",
    "description": "Petit Lattice Tools",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/samia-done/Petit-Lattice-Tools",
    "tracker_url": "https://github.com/samia-done/Petit-Lattice-Tools/issues",
    "category": "Lattice",
}

classes = (plt_operator.PLT_OT_SelectedToLattice,
           plt_operator.VIEW3D_PT_edit_petit_lattice_tools)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():


    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
