"""
ArmatureConstraintSync

このスクリプトは、Blender内で2つのアーマチュア間で「Copy Transforms」コンストレイントを同期させるために使用します。
ソースアーマチュアのボーンのローカル変形を、ターゲットアーマチュアの同名ボーンにコピーします。

使用方法:
1. ソースアーマチュアを最初に選択します。
2. 次に、ターゲットアーマチュアを選択します。
3. このスクリプトを実行します。

スクリプトは、ターゲットアーマチュアに存在するソースアーマチュアの同名ボーンにのみ「Copy Transforms」コンストレイントを適用します。
コンストレイントはローカル空間で適用され、ソースのローカル変形をターゲットに反映させます。

"""

import bpy

# シーンから選択されているオブジェクトのリストを取得
selected_objects = bpy.context.selected_objects

# 2つのアーマチュアが選択されていることを確認
if len(selected_objects) != 2 or any(obj.type != 'ARMATURE' for obj in selected_objects):
    raise Exception("2つのアーマチュアを選択してください。")

# ソースアーマチュアとターゲットアーマチュアを識別
source_armature = selected_objects[0]
target_armature = selected_objects[1]

# ソースアーマチュアのボーン名のセットを作成
source_bone_names = set(bone.name for bone in source_armature.data.bones)

# ターゲットアーマチュアのポーズモードに切り替え
bpy.context.view_layer.objects.active = target_armature
bpy.ops.object.mode_set(mode='POSE')

# ターゲットアーマチュアの各ボーンにコンストレイントを追加（ソースに同名のボーンが存在する場合のみ）
for bone in target_armature.pose.bones:
    if bone.name in source_bone_names:
        # コンストレイントを追加
        constraint = bone.constraints.new('COPY_TRANSFORMS')
        # ソースアーマチュアと同じ名前のボーンを設定
        constraint.target = source_armature
        constraint.subtarget = bone.name
        # コンストレイントをローカル空間で適用
        constraint.target_space = 'LOCAL'
        constraint.owner_space = 'LOCAL'

# 元のモードに戻る（必要に応じて）
bpy.ops.object.mode_set(mode='OBJECT')
