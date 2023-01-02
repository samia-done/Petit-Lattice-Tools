# Copyright (c) 2022 Samia
import bpy
import bmesh
import mathutils


class PLT_OT_SelectedToLattice(bpy.types.Operator):
    bl_idname = "lattice.pat_selected_to_lattice"
    bl_label = "Create Lattice From Selected"
    bl_description = (
        "Creates a Lattice object using the dimensions of the selected vertices"
    )
    bl_options = {"REGISTER", "UNDO"}

    def __init__(self):
        pass

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj and obj.type == "MESH" and obj.mode == "EDIT" or "OBJECT":
            return True
        return False

    def invoke(self, context, event):
        return self.execute(context)

    def execute(self, context):
        # モディファイアの名前
        modifier_name = "CreateLatticeFromSelectedVertices"

        # 現在のモードを取得
        current_mode = bpy.context.mode

        # 編集モードの場合
        if current_mode == "EDIT_MESH":
            # 編集モードでの選択結果を反映させるために一度オブジェクトモードにする
            bpy.ops.object.mode_set(mode="OBJECT")

            # 選択されているオブジェクトを取得
            obj = bpy.context.active_object

            # 選択されている頂点を取得
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            selected_verts = [obj.matrix_world @ v.co for v in bm.verts if v.select]

            if selected_verts:
                # オブジェクトにラティスモディファイアが設定されているかどうかを確認
                if modifier_name in obj.modifiers:
                    # ラティスモディファイアを取得
                    mod = obj.modifiers[modifier_name]
                else:
                    # ラティスモディファイアを追加
                    mod = obj.modifiers.new(modifier_name, "LATTICE")

                # 頂点グループを作成する
                if obj.vertex_groups.get(modifier_name):
                    obj.vertex_groups.remove(obj.vertex_groups[modifier_name])
                    vertex_group = obj.vertex_groups.new(name=modifier_name)
                else:
                    vertex_group = obj.vertex_groups.new(name=modifier_name)

                # 選択した頂点を頂点グループに追加する
                for vertex in obj.data.vertices:
                    if vertex.select:
                        vertex_group.add([vertex.index], 1.0, "ADD")

                # 選択された頂点のみを囲むバウンディングボックスのサイズを計算
                x_min = min(v.x for v in selected_verts)
                x_max = max(v.x for v in selected_verts)
                y_min = min(v.y for v in selected_verts)
                y_max = max(v.y for v in selected_verts)
                z_min = min(v.z for v in selected_verts)
                z_max = max(v.z for v in selected_verts)

                # バウンディングボックスの中点座標
                bb_center = mathutils.Vector(
                    ((x_min + x_max) / 2, (y_min + y_max) / 2, (z_min + z_max) / 2)
                )

                # ローカル座標からワールド座標への変換
                # world_location = obj.matrix_world @ bb_center
                # world_scale = obj.scale
                # world_rotation = obj.rotation_euler

                # ラティスオブジェクトのサイズ
                size = mathutils.Vector((x_max - x_min, y_max - y_min, z_max - z_min))

                # ラティスオブジェクトを作成
                bpy.ops.object.add(type="LATTICE", enter_editmode=False)
                obj = bpy.context.active_object

                # ラティスオブジェクトの位置を設定
                obj.location = bb_center

                off_set = 0.02
                # ラティスオブジェクトのサイズを設定
                obj.dimensions = size

                # obj.location = obj.matrix_world @ bb_center
                # obj.scale = (obj.scale.x * world_scale.x, obj.scale.y * world_scale.y, obj.scale.z * world_scale.z)
                # obj.rotation_euler = world_rotation

                # ラティスモディファイアにオブジェクトを設定
                mod.object = obj

                # ラティスモディファイアに頂点グループを設定
                mod.vertex_group = vertex_group.name

            # Bmeshを破棄
            bm.free()
        return {"FINISHED"}


class VIEW3D_PT_edit_petit_lattice_tools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"
    # bl_context = "mesh_edit"
    bl_label = "Petit Lattice Tools"
    # bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout: bpy.types.UILayout = self.layout
        layout.operator_context = "INVOKE_DEFAULT"
        op: PLT_OT_SelectedToLattice = layout.operator(  # noqa
            PLT_OT_SelectedToLattice.bl_idname,
            text=PLT_OT_SelectedToLattice.bl_label,
        )  # noqa
