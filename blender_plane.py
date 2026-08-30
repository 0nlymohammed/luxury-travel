"""Headless Blender: stylized gold airliner, 3/4 aerial view, transparent PNG.
Run: blender --background --factory-startup --python blender_plane.py"""
import bpy, math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plane_render.png')

# clean scene
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

scene = bpy.context.scene

# ---- gold material ----
mat = bpy.data.materials.new('Gold')
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get('Principled BSDF')
bsdf.inputs['Base Color'].default_value = (0.694, 0.573, 0.400, 1)
bsdf.inputs['Metallic'].default_value = 0.95
bsdf.inputs['Roughness'].default_value = 0.32

def use_gold(obj):
    obj.data.materials.clear()
    obj.data.materials.append(mat)

def mesh_from(verts, faces, name, thickness=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    if thickness:
        m = ob.modifiers.new('sol', 'SOLIDIFY')
        m.thickness = thickness
        m.offset = 0
    use_gold(ob)
    return ob

parts = []

# ---- fuselage: cylinder along X + nose sphere + tail cone (nose = +X) ----
bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=7.6, rotation=(0, math.pi/2, 0), location=(0, 0, 0))
fus = bpy.context.object; use_gold(fus); parts.append(fus)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55, location=(3.8, 0, 0), segments=24, ring_count=16)
nose = bpy.context.object; nose.scale = (1.7, 1.0, 1.0); use_gold(nose); parts.append(nose)
bpy.ops.mesh.primitive_cone_add(radius1=0.55, radius2=0.07, depth=2.6, rotation=(0, -math.pi/2, 0), location=(-5.0, 0, 0.12))
tail = bpy.context.object; tail.rotation_euler[1] += math.radians(-4); use_gold(tail); parts.append(tail)

# ---- wings (swept, low-mounted) ----
w = mesh_from(
    [(0.9, 0.55, 0), (-1.7, 4.9, 0.35), (-2.5, 4.9, 0.35), (-1.5, 0.55, 0),
     (0.9, -0.55, 0), (-1.7, -4.9, 0.35), (-2.5, -4.9, 0.35), (-1.5, -0.55, 0)],
    [(0, 1, 2, 3), (4, 7, 6, 5)], 'Wings', thickness=0.16)
w.location = (0.3, 0, -0.18)
parts.append(w)

# ---- tailplane ----
tp = mesh_from(
    [(0.35, 0.2, 0), (-0.75, 1.9, 0.12), (-1.15, 1.9, 0.12), (-0.75, 0.2, 0),
     (0.35, -0.2, 0), (-0.75, -0.2, 0), (-1.15, -1.9, 0.12), (-0.75, -1.9, 0.12)],
    [(0, 1, 2, 3), (4, 5, 6, 7)], 'Tailplane', thickness=0.12)
tp.location = (-4.7, 0, 0.25)
parts.append(tp)

# ---- vertical fin ----
fin = mesh_from(
    [(0.5, 0, 0), (-0.9, 0, 1.75), (-1.55, 0, 1.75), (-0.7, 0, 0)],
    [(0, 1, 2, 3)], 'Fin', thickness=0.13)
fin.location = (-4.45, 0, 0.4)
parts.append(fin)

# ---- engines under wings ----
for sy in (1, -1):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.34, depth=1.6, rotation=(0, math.pi/2, 0), location=(0.55, 1.95 * sy, -0.62))
    e = bpy.context.object; use_gold(e); parts.append(e)

# ---- rig: gentle bank ----
rig = bpy.data.objects.new('rig', None)
bpy.context.collection.objects.link(rig)
for p in parts:
    p.parent = rig
rig.rotation_euler = (math.radians(16), 0, 0)

# ---- lights ----
def area(loc, energy, size, color=(1, 1, 1)):
    bpy.ops.object.light_add(type='AREA', location=loc)
    L = bpy.context.object
    L.data.energy = energy; L.data.size = size; L.data.color = color
    c = L.constraints.new('TRACK_TO'); c.target = rig
    return L
area((5, -5, 9), 1400, 7, (1.0, 0.88, 0.68))
area((-7, -3, 5), 420, 9, (0.95, 0.97, 1.0))
area((-1, 7, 7), 800, 5, (1.0, 0.92, 0.75))

# ---- camera: 3/4 aerial, nose to screen-right ----
bpy.ops.object.camera_add(location=(3.0, -15.5, 13.5))
cam = bpy.context.object
cam.data.lens = 46
c = cam.constraints.new('TRACK_TO'); c.target = rig
scene.camera = cam

# ---- render settings ----
scene.render.engine = 'CYCLES'
scene.cycles.samples = 96
try:
    scene.cycles.use_denoising = True
except Exception:
    pass
scene.render.film_transparent = True
scene.render.resolution_x = 1600
scene.render.resolution_y = 1100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.filepath = OUT

bpy.ops.render.render(write_still=True)
print('RENDERED ->', OUT)
