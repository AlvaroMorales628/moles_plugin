import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.mel as mel
from maya import cmds

from renderman_interface import *


only_active_lights = False

def clear_aovs(mobject):
    if (not check_for_renderman()):
        cmds.confirmDialog(title="Renderman must be the selected renderer to use this plugin.", button=["ok"])
        return

    reset_aovs()
    update_aov_ui()

def basic_aov_setup(mobject):
    if (not check_for_renderman()):
        cmds.confirmDialog(title="Renderman must be the selected renderer to use this plugin.", button=["ok"])
        return

    reset_aovs()
    pxr_lights = get_pxr_lights()
    lt_group_names = get_light_groups(pxr_lights, active_lights_only=only_active_lights)
    create_lpe_aovs(lt_group_names)
    create_basic_aovs(["z", "zfiltered"])

    update_aov_ui()
    
def render_aov_setup(mobject):
    RMAN_DISPLAY = "rmanDefaultDisplay"
    LIGHT_GROUP_DISPLAY = "LPE_LightGroups"
    EXTRA_ATTR_DISPLAY = "Extra_Attr"
    Z_FILTERED_DISPLAY = "Z_Filtered"

    # clear the aovs we need to use to avoid conflicts
    reset_aovs()
    pxr_lights = get_pxr_lights()
    light_groups = get_light_groups(pxr_lights, active_lights_only=only_active_lights)


    createDisplay(LIGHT_GROUP_DISPLAY)
    createDisplay(EXTRA_ATTR_DISPLAY)
    createDisplay(Z_FILTERED_DISPLAY)
    
    create_lpe_aovs(light_groups, dspy_name=LIGHT_GROUP_DISPLAY, advanced=True)
    #extra aovs (not denoised)
    create_basic_aovs(dspy_name=EXTRA_ATTR_DISPLAY, aov_channels=["z", "directSpecular", "indirectSpecular", "emissive", "transmissiveGlassLobe", "dPdtime", "motionFore", "motionBack"])
    create_basic_aovs(dspy_name=Z_FILTERED_DISPLAY, aov_channels=["zfiltered"])

    # turn on denoise for default display
    cmds.evalDeferred(lambda: setupDenoisedDisplay(RMAN_DISPLAY))
    # turn on denoise for light groups
    cmds.evalDeferred(lambda: setupDenoisedDisplay(LIGHT_GROUP_DISPLAY))

    update_aov_ui()

def set_render_settings(mobject):
    general_render_setup()


def coming_soon(mobject):
    cmds.confirmDialog(title='Not yet implemented', button=["ok"])
    return

def switch_light_func(mobject):
    #mobject is a boolean value based off checkbox
    global only_active_lights
    only_active_lights = mobject


# Initialize the script plug-in
def initializePlugin(mobject):
    """Load the plugin in Maya."""
    global custom_menu

    custom_menu = cmds.menu('Moles Plugin', parent=mel.eval("$retvalue = $gMainWindow;"))
    cmds.menuItem(divider=True, dividerLabel='Render Settings')
    cmds.menuItem(label='Set render settings', command=set_render_settings, parent=custom_menu)
    cmds.menuItem(divider=True, dividerLabel='Generate AOVs')
    cmds.menuItem(label='Use only visible lights', checkBox=False, command=switch_light_func, parent=custom_menu)
    cmds.menuItem(label='Create basic AOVs', command=basic_aov_setup, parent=custom_menu)
    cmds.menuItem(label='Create AOVs for render', command=render_aov_setup, parent=custom_menu)
    cmds.menuItem(label='Clear AOVS', command=clear_aovs, parent=custom_menu)

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    """Remove the plugin from Maya."""
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    cmds.deleteUI(custom_menu)

    """
    try:
        for fn in callback_fns:
            OpenMaya.MCommandMessage.removeCallback(fn)
    except RuntimeError as e:
        sys.stderr.write("Failed to unregister callbacks: %s\n" % e)
    """
