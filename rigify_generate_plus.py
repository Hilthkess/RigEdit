bl_info = {
    "name": "Rigify Generate and Edit",
    "blender": (4, 1, 0),
    "category": "Rigging",
}

import bpy

class GenerateRigifyAdvanced(bpy.types.Operator):
    """Generates the rig based on the armature set in the Metarig field with the defined settings"""
    bl_idname = "object.generate_rigify_advanced"
    bl_label = "Generate Rigify Rig"

    def execute(self, context):
        metarig = context.scene.metarig_obj
        generated = context.scene.genrig_obj
        checkbox_DEF = context.scene.DEF_checkbox
        checkbox_MCH = context.scene.MCH_checkbox
        checkbox_ORG = context.scene.ORG_checkbox
        checkbox_overwrite = context.scene.overwrite_widgets
        dropdown_bone_displ = context.scene.bone_display_dropdown
        
        if metarig is None:
            self.report({'WARNING'}, "Please set the Metarig")
            return {'CANCELLED'}

        # Insert your custom code here
        self.generate_plus(metarig, generated, checkbox_DEF, checkbox_MCH, checkbox_ORG, dropdown_bone_displ,checkbox_overwrite)
        return {'FINISHED'}

    def generate_plus(self, metarig, generated, checkbox_DEF, checkbox_MCH, checkbox_ORG, dropdown_bone_displ,checkbox_overwrite):
        if checkbox_overwrite==True:
            bpy.context.object.data.rigify_force_widget_update = True
        else:
            bpy.context.object.data.rigify_force_widget_update = False    
        if (
        metarig.hide_viewport == True):
            metarig.hide_viewport = False
        bpy.context.view_layer.objects.active = metarig
        bpy.ops.pose.rigify_generate()
        bpy.context.object.data.collections_all["DEF"].is_visible = checkbox_DEF
        bpy.context.object.data.collections_all["ORG"].is_visible = checkbox_ORG
        bpy.context.object.data.collections_all["MCH"].is_visible = checkbox_MCH
        bpy.context.object.data.display_type = dropdown_bone_displ
        metarig.hide_viewport = True
        


class EditMetarig(bpy.types.Operator):
    """Edit the Metarig set in the Metarig field above."""
    bl_idname = "object.edit_metarig"
    bl_label = "Edit Metarig"

    def execute(self, context):
        metarig = context.scene.metarig_obj
        generated = context.scene.genrig_obj
        
        if metarig is None:
            self.report({'WARNING'}, "Please set the Metarig")
            return {'CANCELLED'}

        # Insert your custom code here
        self.edit_metarig(metarig, generated)
        return {'FINISHED'}

    def edit_metarig(self, metarig, generated):
        metarig.hide_viewport = False
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = metarig
        metarig.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')

    

class GenerateEditRigify(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Generate and Edit Rigify rig"
    bl_idname = "OBJECT_PT_two_objects"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'
    
    
    def draw(self, context):
        layout = self.layout
        
        # Create fields to select objects
        layout.prop(context.scene, "metarig_obj")
        #layout.prop(context.scene, "genrig_obj")
        
        layout.separator()
        box = layout.box()
        box.label(text="Generation Setting:")
        # Create dropdown menu
        box.prop(context.scene, "bone_display_dropdown", text="Bone Display")
        
        # Create checkboxes for DEF, MCH, ORG
        row = box.row()
        row.prop(context.scene, "DEF_checkbox", text="DEF")
        row.prop(context.scene, "MCH_checkbox", text="MCH")
        row.prop(context.scene, "ORG_checkbox", text="ORG")
        
        #Create checkbox for Overwrite Widgets
        row = box.row()
        row.prop(context.scene, "overwrite_widgets", text="Overwrite Widgets")

        row1 = box.row()
        row1.operator("object.generate_rigify_advanced")
        row1.scale_y = 1.5
        
        
        # Create button to execute action
        box = layout.box()
        box.scale_y = 1.5
        row = box.row()
        row.operator("object.edit_metarig")
        
        


def register():
    bpy.utils.register_class(GenerateRigifyAdvanced)
    bpy.utils.register_class(EditMetarig)
    bpy.utils.register_class(GenerateEditRigify)
    bpy.types.Scene.metarig_obj = bpy.props.PointerProperty(
        name="Metarig",
        type=bpy.types.Object,
        description="Set your Metarig here"
    )
    bpy.types.Scene.genrig_obj = bpy.props.PointerProperty(
        name="Generated",
        type=bpy.types.Object,
        description="Set your Generated rig here"
    )
    bpy.types.Scene.DEF_checkbox = bpy.props.BoolProperty(
        name="DEF Checkbox",
        description="Show DEF bones after Generation",
        default=False
    )
    bpy.types.Scene.MCH_checkbox = bpy.props.BoolProperty(
        name="MCH Checkbox",
        description="Show MCH bones after Generation",
        default=False
    )
    bpy.types.Scene.ORG_checkbox = bpy.props.BoolProperty(
        name="ORG Checkbox",
        description="Show ORG bones after Generation",
        default=False
    )
    bpy.types.Scene.overwrite_widgets = bpy.props.BoolProperty(
        name="Overwrite Widgets",
        description="Show ORG bones after Generation",
        default=False
    )
    bpy.types.Scene.bone_display_dropdown = bpy.props.EnumProperty(
        name="Bone Display",
        description="Bone Display mode after Generation",
        items=[
            ('OCTAHEDRAL', "Octahedral", ""),
            ('BBONE', "B-Bone", ""),
            ('STICK', "Stick", ""),
            ('ENVELOPE', "Envelope", ""),
            ('WIRE', "Wire", "")
        ],
        default='BBONE'
    )


def unregister():
    bpy.utils.unregister_class(GenerateRigifyAdvanced)
    bpy.utils.unregister_class(EditMetarig)
    bpy.utils.unregister_class(GenerateEditRigify)
    del bpy.types.Scene.metarig_obj
    del bpy.types.Scene.genrig_obj
    del bpy.types.Scene.DEF_checkbox
    del bpy.types.Scene.MCH_checkbox
    del bpy.types.Scene.ORG_checkbox
    del bpy.types.Scene.bone_display_dropdown

if __name__ == "__main__":
    register()
