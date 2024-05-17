
import matplotlib.pyplot as plt
import numpy as np



def generate_localisation_mask(spot_size, spot_shape = "square", 
                               buffer=0, bg_size=1, plot=False):

    box_size = spot_size + (bg_size*2) + (buffer*2)
    
    # Create a grid of coordinates
    y, x = np.ogrid[:box_size, :box_size]
    
    # Adjust center based on box size
    if box_size % 2 == 0:
        center = (box_size / 2 - 0.5, box_size / 2 - 0.5)
    else:
        center = (box_size // 2, box_size // 2)
    
    if spot_shape.lower() == "circle":
        # Calculate distance from the center for circular mask
        distance = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
    
        # Central spot mask
        inner_radius = spot_size // 2
        mask = distance <= inner_radius
    
        # Buffer mask
        buffer_outer_radius = inner_radius + buffer
        buffer_mask = (distance > inner_radius) & (distance <= buffer_outer_radius)
    
        # Background mask (outside the buffer zone)
        background_outer_radius = buffer_outer_radius + bg_size
        background_mask = (distance > buffer_outer_radius) & (distance <= background_outer_radius)
        
    elif spot_shape.lower() == "square":
        # Create square mask
        half_size = spot_size // 2
        mask = (abs(x - center[0]) <= half_size) & (abs(y - center[1]) <= half_size)
    
        # Create square background mask (one pixel larger on each side)
        buffer_mask = (abs(x - center[0]) <= half_size + buffer) & (abs(y - center[1]) <= half_size+buffer)
        background_mask = (abs(x - center[0]) <= half_size + buffer + bg_size) & (abs(y - center[1]) <= half_size + buffer+ bg_size)
        background_mask = background_mask & ~buffer_mask
    
    if plot == True:
    
         plt.figure(figsize=(6, 6))
         plt.imshow(mask, cmap='gray', interpolation='none')
         plt.xticks(np.arange(-0.5, box_size, 1), [])
         plt.yticks(np.arange(-0.5, box_size, 1), [])
         plt.grid(color='blue', linestyle='-', linewidth=2)
         plt.title(f"{box_size}x{box_size} Spot Mask")
         plt.show()
    
    
         plt.figure(figsize=(6, 6))
         plt.imshow(buffer_mask, cmap='gray', interpolation='none')
         plt.xticks(np.arange(-0.5, box_size, 1), [])
         plt.yticks(np.arange(-0.5, box_size, 1), [])
         plt.grid(color='blue', linestyle='-', linewidth=2)
         plt.title(f"{box_size}x{box_size} Buffer Mask")
         plt.show()
    
    
         plt.figure(figsize=(6, 6))
         plt.imshow(background_mask, cmap='gray', interpolation='none')
         plt.xticks(np.arange(-0.5, box_size, 1), [])
         plt.yticks(np.arange(-0.5, box_size, 1), [])
         plt.grid(color='blue', linestyle='-', linewidth=2)
         plt.title(f"{box_size}x{box_size} Background Mask")
         plt.show()
    
    return mask,buffer_mask,background_mask
   
    
mask,buffer_mask,background_mask = generate_localisation_mask(spot_size = 3,
                           spot_shape="square",
                           buffer=0,
                           bg_size=0,
                           plot=True)