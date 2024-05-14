from scfile.consts import McsaModel
from scfile.file.data import ModelData
from scfile.file.encoder import FileEncoder
from scfile.utils.model import Mesh, Vertex


class Ms3dAsciiEncoder(FileEncoder[ModelData]):
    FLOAT_FORMAT = ".6f"

    def serialize(self):
        self.model = self.data.model
        self.meshes = self.data.model.meshes
        self.skeleton = self.model.skeleton
        self.flags = self.data.model.flags

        self.model.ensure_unique_names()

        self._add_header()
        self._add_meshes()
        self._add_materials()
        self._add_skeleton()
        self._add_stats()

    def _add_header(self):
        self.b.writes(
            "\n".join(
                [
                    "// MilkShape 3D ASCII",
                    "",
                    "Frames: 30",
                    "Frame: 1",
                    f"Meshes: {len(self.meshes)}",
                ]
            )
        )
        self.b.writes("\n")

    def _add_meshes(self):
        for index, mesh in enumerate(self.meshes):
            self.b.writes(f'"{mesh.name}" 0 {index}\n')
            self._add_vertices(mesh)
            self._add_normals(mesh)
            self._add_polygons(mesh)
        self.b.writes("\n")

    def _get_bone_id(self, v: Vertex) -> int:
        bone_id = McsaModel.ROOT_BONE_ID
        weight = 0
        for key, value in v.bone.ids.items():
            if v.bone.weights[key] > weight:
                bone_id = value
                weight = v.bone.weights[key]
        return bone_id

    def _add_vertices(self, mesh: Mesh):
        f = self.FLOAT_FORMAT

        self.b.writes(f"{len(mesh.vertices)}\n")
        self.b.writes(
            "\n".join(
                [
                    f"0 {v.position.x:{f}} {v.position.y:{f}} {v.position.z:{f}} {v.texture.u:{f}} {v.texture.v:{f}} {self._get_bone_id(v)}"
                    for v in mesh.vertices
                ]
            )
        )
        self.b.writes("\n")

    def _add_normals(self, mesh: Mesh):
        f = self.FLOAT_FORMAT

        self.b.writes(f"{len(mesh.vertices)}\n")
        self.b.writes(
            "\n".join(
                [f"{v.normals.x:{f}} {v.normals.y:{f}} {v.normals.z:{f}}" for v in mesh.vertices]
            )
        )
        self.b.writes("\n")

    def _add_polygons(self, mesh: Mesh):
        self.b.writes(f"{len(mesh.polygons)}\n")

        for p in mesh.polygons:
            self.b.writes(f"0 {p.a} {p.b} {p.c} {p.a} {p.b} {p.c} 1\n")

    def _add_materials(self):
        self.b.writes(f"Materials: {len(self.model.meshes)}\n")

        for index, mesh in enumerate(self.model.meshes):
            blank_name = f"material_{index}"
            self.b.writes(
                "\n".join(
                    [
                        f'"{mesh.material or blank_name}"',
                        "0.200000 0.200000 0.200000 1.000000",
                        "0.800000 0.800000 0.800000 1.000000",
                        "0.000000 0.000000 0.000000 1.000000",
                        "0.000000 0.000000 0.000000 1.000000",
                        "0.000000",
                        "1.000000",
                        '""',
                        '""',
                    ]
                )
            )
            self.b.writes("\n")
        self.b.writes("\n")

    def _add_skeleton(self):
        f = self.FLOAT_FORMAT

        if not self.flags.skeleton:
            self.b.writes("Bones: 0\n")
            return

        self.b.writes(f"Bones: {len(self.skeleton.bones)}\n")

        for b in self.skeleton.bones:
            self.b.writes(f'"{b.name}"\n')

            if b.parent_id < 0:
                self.b.writes('""\n')
            else:
                parent_name = self.skeleton.bones[b.parent_id].name
                self.b.writes(f'"{parent_name}"\n')

            self.b.writes(
                f"0 {b.position.x:{f}} {b.position.y:{f}} {b.position.z:{f}} {b.rotation.x:{f}} {b.rotation.y:{f}} {b.rotation.z:{f}}\n"
            )
            self.b.writes("0\n")
            self.b.writes("0\n")

    def _add_stats(self):
        self.b.writes(
            "\n".join(
                [
                    "GroupComments: 0",
                    "MaterialComments: 0",
                    "BoneComments: 0",
                    "ModelComment: 0",
                ]
            )
        )
