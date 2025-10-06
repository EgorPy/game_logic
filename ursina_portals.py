from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

random.seed(0)
Entity.default_shader = lit_with_shadows_shader

# Ground entity
ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4, 4))

# Player setup
editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=16, collider='box')
player.mouse_sensitivity = [110, 110]

# Disable default jumping and gravity
player.jumping = False
player.gravity = False
player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))

# Jumping and gravity variables
jumping = False
jump_force = 12  # Height of the jump
gravity = 30  # How strong gravity is
velocity_y = 0  # Vertical velocity
ground_level = 1  # Define the ground level for the player

# Create two portals with solid color textures
portal_1 = Entity(model='plane', color=color.blue, scale=2, collider='box', position=(5, 1, 5))
portal_2 = Entity(model='plane', color=color.orange, scale=2, collider='box', position=(-5, 1, 5))

# Flag to check teleportation state
player.has_teleported = False

def teleport_to_portal():
    global player

    # When player enters portal 1, teleport to portal 2
    if player.intersects(portal_1) and not player.has_teleported:
        player.position = portal_2.position + Vec3(0, 1, 0)  # Teleport to portal 2's location
        player.has_teleported = True  # Flag to prevent teleport loop
        player.rotation = portal_2.rotation  # Rotate the player to face the correct way

    # When player enters portal 2, teleport to portal 1
    elif player.intersects(portal_2) and not player.has_teleported:
        player.position = portal_1.position + Vec3(0, 1, 0)  # Teleport to portal 1's location
        player.has_teleported = True  # Flag to prevent teleport loop
        player.rotation = portal_1.rotation  # Rotate the player to face the correct way

    # Reset teleport flag when player exits portal
    if not player.intersects(portal_1) and not player.intersects(portal_2):
        player.has_teleported = False

def update():
    global velocity_y, jumping

    # Check if player is on the ground
    if player.y <= ground_level:
        velocity_y = 0  # Reset vertical velocity when on the ground
        player.y = ground_level  # Ensure player is not below the ground level
        if not jumping and held_keys['space']:  # Trigger jump
            jumping = True
            velocity_y = jump_force  # Set upward velocity for jump

    # Apply gravity when the player is in the air
    if player.y > ground_level:
        velocity_y -= gravity * time.dt  # Apply downward force due to gravity

    # Update player position with vertical velocity
    player.y += velocity_y * time.dt

    # Prevent falling below the ground level
    if player.y < ground_level:
        player.y = ground_level
        jumping = False  # Player is back on the ground, no longer jumping

    # Teleport player if they enter a portal
    teleport_to_portal()

def pause_input(key):
    if key == 'tab':  # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)

# Light source
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))

# Skybox
Sky()

# Run the app
app.run()
