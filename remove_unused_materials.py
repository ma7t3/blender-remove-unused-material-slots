bl_info = {
    "name": "Remove Unused Material Slots",
    "blender": (3, 0, 0),
    "category": "Object",
    "description": "Removes unused material slots from the selected object",
}

import bpy

class OBJECT_OT_RemoveUnusedMaterials(bpy.types.Operator):
    """Removes unused material slots from the selected object"""
    bl_idname = "object.remove_unused_material_slots"
    bl_label = "Remove Unused Material Slots"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "The selected object is not a mesh!")
            return {'CANCELLED'}
        
        removed_slots = 0

        for i in range(len(obj.material_slots) - 1, -1, -1):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')

            bpy.ops.object.mode_set(mode='EDIT')
            obj.active_material_index = i
            bpy.ops.object.material_slot_select()
            bpy.ops.object.mode_set(mode='OBJECT')

            if not any(f.select for f in obj.data.polygons):
                obj.active_material_index = i
                bpy.ops.object.material_slot_remove()
                removed_slots += 1

        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, f"{removed_slots} unused material slots removed.")
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_RemoveUnusedMaterials.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_RemoveUnusedMaterials)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_RemoveUnusedMaterials)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

