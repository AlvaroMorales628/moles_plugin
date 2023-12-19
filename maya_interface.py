from maya import cmds


def generate_maya_playblast():

    """ Capture current state prior to altering settings """
    current_panel = cmds.playblast(activeEditor=True)

    selected_objects = cmds.ls(sl=True,long=True)


    """ Get current window options. This will be unformatted"""
    options = cmds.modelEditor(current_panel, q=True, sts=True)

    user_settings = {}
    for option in options.splitlines():
        trimmed_option = option.strip()
        
        key_val = trimmed_option.split(" ")
        
        # We don't want all the options 
        if (len(key_val) != 2):
            continue;
        
        # We don't want all the options    
        if (key_val[0][0] == "-"):
            if (key_val[1] == "1" or key_val[1] == "0"):
                # Type cast when we can
                user_settings[key_val[0][1:]] = int(key_val[1])
            else:
                user_settings[key_val[0][1:]] = key_val[1]
        


    """ Set desired playblast settings """
    cmds.select([], replace=True)
    # Image plane options?
    cmds.modelEditor(current_panel, controllers=0, nurbsCurves=0, nurbsSurfaces=0, controlVertices=0,
                    hulls=0, polymeshes=1, subdivSurfaces=0, planes=0,  lights=1, cameras=0,
                    joints=0, ikHandles=0, deformers=0, dynamics=1, particleInstancers=0, fluids=1, 
                    hairSystems=0, follicles=0, nCloths=0, nParticles=0, nRigids=0, dynamicConstraints=0,
                    locators=0, dimensions=0, pivots=0, handles=0, textures=1, strokes=0, motionTrails=1,
                    pluginShapes=0, clipGhosts=0, greasePencils=1, manipulators=0, grid=0, hud=0, hos=0,
                    edit=True)
                    
    cmds.playblast(height=540, width=960)

    """ Restore to prior state """
    cmds.select(selected_objects, replace=True)
    cmds.modelEditor(current_panel, controllers=user_settings["controllers"], nurbsCurves=user_settings["nurbsCurves"], nurbsSurfaces=user_settings["nurbsSurfaces"], controlVertices=user_settings["controlVertices"],
                    hulls=user_settings["hulls"], polymeshes=user_settings["polymeshes"], subdivSurfaces=user_settings["subdivSurfaces"], planes=user_settings["planes"],  lights=user_settings["lights"], cameras=user_settings["cameras"],
                    joints=user_settings["joints"], ikHandles=user_settings["ikHandles"], deformers=user_settings["deformers"], dynamics=user_settings["dynamics"], particleInstancers=user_settings["particleInstancers"], fluids=user_settings["fluids"], 
                    hairSystems=user_settings["hairSystems"], follicles=user_settings["follicles"], nCloths=user_settings["nCloths"], nParticles=user_settings["nParticles"], nRigids=user_settings["nRigids"], dynamicConstraints=user_settings["dynamicConstraints"],
                    locators=user_settings["locators"], dimensions=user_settings["dimensions"], pivots=user_settings["pivots"], handles=user_settings["handles"], textures=user_settings["textures"], strokes=user_settings["strokes"], motionTrails=user_settings["motionTrails"],
                    pluginShapes=user_settings["pluginShapes"], clipGhosts=user_settings["clipGhosts"], greasePencils=user_settings["greasePencils"], manipulators=user_settings["manipulators"], grid=user_settings["grid"], hud=user_settings["headsUpDisplay"], hos=user_settings["holdOuts"],
                    edit=True)
