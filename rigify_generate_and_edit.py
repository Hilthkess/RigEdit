import bpy

class PosePosition(bpy.types.Operator):
    """Generates the rig based on the armature set in the Metarig field with the defined settings"""
    bl_idname = "object.pose_position"
    bl_label = "Pose Position"

    def execute(self, context):
        generated = context.scene.genrig_obj
        generated.data.pose_position = 'POSE'
        return {'FINISHED'}

class Skin(bpy.types.Operator):
    """Generates the rig based on the armature set in the Metarig field with the defined settings"""
    bl_idname = "object.skin"
    bl_label = "Skin"

    def execute(self, context):
        skin = context.scene.skin_obj
        skin.hide_viewport = False
        skin.hide_set(False)
        skin.hide_select = False
        skin.select_set(True)
        generated = context.scene.genrig_obj
        generated.select_set(True)
        generated.hide_viewport = False
        generated.hide_set(False)
        bpy.context.view_layer.objects.active = generated
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.wm.voxel_heat_diffuse()
        return {'FINISHED'}

class RestPosition(bpy.types.Operator):
    """Generates the rig based on the armature set in the Metarig field with the defined settings"""
    bl_idname = "object.rest_position"
    bl_label = "Rest Position"

    def execute(self, context):
        generated = context.scene.genrig_obj
        generated.data.pose_position = 'REST'
        return {'FINISHED'}

class GenerateRigifyAdvanced(bpy.types.Operator):
    """Generates the rig based on the armature set in the Metarig field with the defined settings"""
    bl_idname = "object.generate_rigify_advanced"
    bl_label = "Generate Rig"

    def execute(self, context):
        metarig = context.scene.metarig_obj
        generated = context.scene.genrig_obj
        checkbox_overwrite = context.scene.overwrite_widgets
        dropdown_bone_displ = context.scene.bone_display_dropdown

        if metarig is None:
            self.report({'WARNING'}, "Please set the Metarig")
            return {'CANCELLED'}

        # Insert your custom code here
        self.generate_plus(metarig, generated, dropdown_bone_displ,checkbox_overwrite)
        return {'FINISHED'}

    def generate_plus(self, metarig, generated, dropdown_bone_displ,checkbox_overwrite):
        bpy.context.view_layer.objects.active = metarig
        if checkbox_overwrite==True:
            bpy.context.object.data.rigify_force_widget_update = True
        else:
            bpy.context.object.data.rigify_force_widget_update = False
        metarig.hide_viewport = False
        metarig.hide_set(False)
        bpy.context.view_layer.objects.active = metarig
        bpy.ops.pose.rigify_generate()
        bpy.context.view_layer.objects.active = generated
        bpy.context.object.data.display_type = dropdown_bone_displ
        metarig.hide_viewport = True
        generated.select_set(True)
        bpy.context.view_layer.objects.active = generated
        bpy.ops.object.mode_set(mode='POSE')

class PoseRigifyAdvanced(bpy.types.Operator):
    """Generates the rig based on the armature set in the Metarig field with the defined settings"""
    bl_idname = "object.pose_rigify_advanced"
    bl_label = "Pose Rig"

    def execute(self, context):
        metarig = context.scene.metarig_obj
        generated = context.scene.genrig_obj
        checkbox_overwrite = context.scene.overwrite_widgets
        dropdown_bone_displ = context.scene.bone_display_dropdown

        if metarig is None:
            self.report({'WARNING'}, "Please set the Metarig")
            return {'CANCELLED'}

        # Insert your custom code here
        self.generate_plus(metarig, generated, dropdown_bone_displ,checkbox_overwrite)
        return {'FINISHED'}

    def generate_plus(self, metarig, generated, dropdown_bone_displ,checkbox_overwrite):
        metarig.hide_viewport = True
        generated.hide_viewport = False
        generated.hide_set(False)
        generated.select_set(True)
        bpy.context.view_layer.objects.active = generated
        bpy.ops.object.mode_set(mode='POSE')

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
        metarig.select_set(True)
        metarig.hide_viewport = False
        metarig.hide_set(False)
        if(metarig.hide_get()):
            self.report({'WARNING'}, "Metarig is hidden?")
        
        generated.hide_viewport = True
        bpy.context.view_layer.objects.active = metarig
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = metarig
        bpy.ops.object.mode_set(mode='EDIT')

class PoseMetarig(bpy.types.Operator):
    """Edit the Metarig set in the Metarig field above."""
    bl_idname = "object.pose_metarig"
    bl_label = "Pose Metarig"

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
        metarig.hide_set(False)
        generated.hide_viewport = True
        bpy.context.view_layer.objects.active = metarig
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = metarig
        metarig.select_set(True)
        bpy.ops.object.mode_set(mode='POSE')

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
        layout.prop(context.scene, "genrig_obj")
        layout.prop(context.scene, "skin_obj")

        layout.separator()
        box = layout.box()
        box.label(text="Generation Setting:")
        # Create dropdown menu
        box.prop(context.scene, "bone_display_dropdown", text="Bone Display")

        #Create checkbox for Overwrite Widgets
        row = box.row()
        row.prop(context.scene, "overwrite_widgets", text="Overwrite Widgets")

        row = box.row()
        row.operator("object.pose_position")
        row.operator("object.rest_position")

        row = box.row()
        row.operator("object.generate_rigify_advanced")
        row.operator("object.skin")
        row.operator("object.pose_rigify_advanced")

        # Create button to execute action
        box = layout.box()
        row = box.row()
        row.operator("object.edit_metarig")
        row.operator("object.pose_metarig")

def register():
    print("rigify_generate_and_edit.register()")
    bpy.utils.register_class(GenerateRigifyAdvanced)
    bpy.utils.register_class(Skin)
    bpy.utils.register_class(PosePosition)
    bpy.utils.register_class(RestPosition)
    bpy.utils.register_class(PoseRigifyAdvanced)
    bpy.utils.register_class(EditMetarig)
    bpy.utils.register_class(PoseMetarig)
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
    bpy.types.Scene.skin_obj = bpy.props.PointerProperty(
        name="Skin",
        type=bpy.types.Object,
        description="Set your object to be skinned here"
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
    print("rigify_generate_and_edit.register()")
    bpy.utils.unregister_class(GenerateRigifyAdvanced)
    bpy.utils.unregister_class(Skin)
    bpy.utils.unregister_class(PosePosition)
    bpy.utils.unregister_class(RestPosition)
    bpy.utils.unregister_class(PoseRigifyAdvanced)
    bpy.utils.unregister_class(EditMetarig)
    bpy.utils.unregister_class(PoseMetarig)
    bpy.utils.unregister_class(GenerateEditRigify)
    del bpy.types.Scene.metarig_obj
    del bpy.types.Scene.genrig_obj
    del bpy.types.Scene.skin_obj
    del bpy.types.Scene.bone_display_dropdown
