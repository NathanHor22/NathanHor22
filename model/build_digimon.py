"""Render an original Digimon enclosure concept for Nathan Hor's profile.

Run: blender --background --factory-startup --python build_digimon.py -- preview
Run without 'preview' to render the complete 72-frame turntable.
This is a visual design study, not measured or fabrication-ready CAD.
"""
from pathlib import Path
import bpy
import math
import sys
from mathutils import Vector

HERE = Path(__file__).resolve().parent
OUTPUTS = HERE.parent
WORK = OUTPUTS.parent / 'work'
FRAMES = WORK / 'digimon-frames'
FRAMES.mkdir(parents=True, exist_ok=True)

# This script runs in a separate background Blender process. It never opens or
# changes the user's interactive Blender document.
scene = bpy.data.scenes.new('Nathan Hor - Digimon concept')
bpy.context.window.scene = scene
scene['description'] = 'Original enclosure concept for the ESP32-S3 Digimon companion. Not measured CAD or footage of working hardware.'
scene['reference'] = 'NathanHor22/digimon: mint face, three physical buttons, 240x240 display.'
scene.render.engine = 'BLENDER_EEVEE'
if hasattr(scene, 'eevee') and hasattr(scene.eevee, 'taa_render_samples'):
    scene.eevee.taa_render_samples = 24
scene.render.resolution_x = 720
scene.render.resolution_y = 650
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = True
scene.render.fps = 12
scene.frame_start = 1
scene.frame_end = 72
scene.render.filepath = str(FRAMES / 'frame_')
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.view_settings.exposure = 0
scene.world = bpy.data.worlds.new('Studio atmosphere')
scene.world.use_nodes = True
scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value = (.15, .18, .22, 1)
scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value = .65

def srgb(hexcode):
    rgb = [int(hexcode[i:i+2], 16) / 255 for i in (0,2,4)]
    return tuple(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb) + (1,)

def material(name, color, rough=.4, metallic=0, emission=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = srgb(color)
    mat.use_nodes = True
    node = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    node.inputs['Base Color'].default_value = srgb(color)
    node.inputs['Roughness'].default_value = rough
    node.inputs['Metallic'].default_value = metallic
    if emission:
        node.inputs['Emission Color'].default_value = srgb(color)
        node.inputs['Emission Strength'].default_value = emission
    return mat

ivory = material('Ceramic ivory shell', 'EAE8DC', .3)
ink = material('Graphite rubber', '18252D', .42)
black = material('Recess shadows', '071015', .75)
mint = material('Mint display', '88D9B6', .55, emission=.8)
face = material('Dark green display pixels', '123E30', .6)
coral = material('Coral accent', 'FF574B', .32)
acid = material('Selected yellow', 'EAFF4B', .38)
steel = material('Hardware steel', 'A6B4B7', .25, .7)
muted = material('Backplate printing', 'B9CBC9', .65)

rig = bpy.data.objects.new('Turntable - complete device', None)
scene.collection.objects.link(rig)

def finish(obj, mat, parent=True):
    obj.data.materials.append(mat)
    if parent:
        obj.parent = rig
    return obj

def box(name, loc, dims, mat, bevel=.06):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new('Soft machined edge', 'BEVEL')
        mod.width = bevel
        mod.segments = 5
        mod = obj.modifiers.new('Weighted corner normals', 'WEIGHTED_NORMAL')
    for p in obj.data.polygons:
        p.use_smooth = True
    return finish(obj, mat)

def cylinder(name, loc, radius, depth, mat, rotation=(math.pi/2,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth, location=loc, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    bevel = obj.modifiers.new('Rounded edge', 'BEVEL')
    bevel.width = .018
    bevel.segments = 3
    obj.modifiers.new('Weighted normals', 'WEIGHTED_NORMAL')
    for p in obj.data.polygons:
        p.use_smooth = True
    return finish(obj, mat)

font_path = Path('C:/Windows/Fonts/bahnschrift.ttf')
font = bpy.data.fonts.load(str(font_path)) if font_path.exists() else None

def text(name, value, loc, size, mat, back=False):
    curve = bpy.data.curves.new(name, 'FONT')
    curve.body = value
    curve.size = size
    curve.align_x = 'CENTER'
    curve.align_y = 'CENTER'
    curve.extrude = .0005
    if font:
        curve.font = font
    obj = bpy.data.objects.new(name, curve)
    scene.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (math.pi/2, 0, math.pi if back else 0)
    return finish(obj, mat)

box('Main ivory shell', (0,0,0), (2.64,.78,3.35), ivory, .22)
box('Perimeter gasket', (0,.20,0), (2.65,.10,3.30), ink, .18)
box('Graphite rear cover', (0,.34,0), (2.50,.26,3.16), ink, .16)
box('Raised display bezel', (0,-.403,.28), (2.34,.17,2.34), ink, .14)
box('Square mint LCD', (0,-.495,.28), (2.09,.025,2.09), mint, .055)

eyes = []
for x in (-.41,.41):
    eye = cylinder('Face eye', (x,-.514,.48), .067,.012,face)
    eyes.append(eye)
box('Idle straight mouth', (0,-.515,-.02), (.49,.016,.026), face, .008)
cylinder('Small status pixel', (.83,-.514,1.10), .022,.012,face)

for x in (-.70,.70):
    box('Side button recess', (x,-.399,-1.17), (.49,.04,.35), ink,.10)
    box('Side button', (x,-.433,-1.17), (.40,.085,.25), ivory,.075)
    text('Volume marking', '+' if x > 0 else '-', (x,-.482,-1.17),.16,ink)
cylinder('Centre button surround', (0,-.425,-1.17), .30,.085,ink)
cylinder('Centre action button', (0,-.481,-1.17), .23,.08,acid)
cylinder('Centre action mark', (0,-.528,-1.17), .032,.008,ink)
text('Front wordmark', 'DIGIMON', (0,-.399,-.98), .115,ink)
cylinder('Microphone aperture', (-.96,-.393,-1.47), .027,.013,black)
text('Serial front', '01', (.97,-.393,-1.47), .10,ink)

for z in (.65,.81,.97,1.13):
    box('Rear speaker slot', (0,.477,z), (1.38,.017,.067),black,.03)
text('Back device wordmark', 'DIGIMON', (0,.48,.13), .24,muted,True)
text('Back designer', 'NATHAN HOR', (0,.48,-.14), .105,muted,True)
text('Concept engraving', 'ENCLOSURE CONCEPT / 01', (0,.48,-.37), .075,muted,True)
box('Rear accent stripe', (0,.478,-.83), (.7,.014,.055),coral,.02)
for x in (-1.0,1.0):
    for z in (-1.31,1.31):
        cylinder('Rear fastener', (x,.478,z),.047,.015,steel)
        box('Fastener slot', (x,.489,z), (.051,.008,.009),ink,.001)

box('USB-C side surround', (1.318,-.03,-.87), (.03,.42,.18),steel,.06)
box('USB-C port', (1.337,-.03,-.87), (.015,.32,.105),black,.04)
box('USB-C tongue', (1.348,-.03,-.87), (.008,.22,.025),steel,.005)
box('Small side switch', (-1.323,0,-.66), (.07,.27,.14),coral,.04)

# A distinctive loop supplies a useful silhouette as the case turns.
bpy.ops.mesh.primitive_torus_add(major_segments=48, minor_segments=16, location=(.77,0,1.78), rotation=(math.pi/2,0,0), major_radius=.23, minor_radius=.07)
loop = bpy.context.object
loop.name = 'Coral carry loop'
for p in loop.data.polygons:
    p.use_smooth = True
finish(loop, coral)

# One closed turn. Frame 73 matches frame 1 and is intentionally omitted.
rig.rotation_euler = (0,0,math.radians(-14))
rig.keyframe_insert(data_path='rotation_euler',frame=1)
rig.rotation_euler.z += 2*math.pi
rig.keyframe_insert(data_path='rotation_euler',frame=73)
action = rig.animation_data.action
for layer in action.layers:
    for strip in layer.strips:
        for bag in strip.channelbags:
            for curve in bag.fcurves:
                for key in curve.keyframe_points:
                    key.interpolation = 'LINEAR'

# A single blink: decorative idle animation, not evidence of a live voice loop.
for eye in eyes:
    for frame,scale in ((1,1),(3,1),(4,.17),(5,.17),(6,1),(73,1)):
        eye.scale.y = scale
        eye.keyframe_insert(data_path='scale',frame=frame)

def area(name, loc, energy, size, color):
    data = bpy.data.lights.new(name, 'AREA')
    data.energy = energy
    data.shape = 'DISK'
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name,data)
    scene.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (Vector((0,0,.1))-obj.location).to_track_quat('-Z','Y').to_euler()

area('Large soft key', (-4,-6,7), 650,5,(1,.95,.85))
area('Cool fill', (5,-3,2), 430,4,(.78,.94,1))
area('Mint edge', (1,4,5), 850,3,(.69,1,.86))
camera_data = bpy.data.cameras.new('Orthographic character portrait')
camera = bpy.data.objects.new('Orthographic character portrait',camera_data)
scene.collection.objects.link(camera)
camera.location = (4,-10,3.7)
camera.rotation_euler = (Vector((0,0,.12))-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type = 'ORTHO'
camera_data.ortho_scale = 5.5
scene.camera = camera
scene.frame_set(1)
scene.render.filepath = '//renders/frame_'
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(HERE / 'digimon-concept.blend'))
if 'preview' in sys.argv:
    scene.render.filepath = str(WORK / 'digimon-model-preview.png')
    bpy.ops.render.render(write_still=True)
else:
    scene.render.filepath = str(FRAMES / 'frame_')
    bpy.ops.render.render(animation=True)
print('DIGIMON_RENDER_COMPLETE')
