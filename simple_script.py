import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Load the image
image = cv2.imread('path_to_image/syria_map.png')

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Create masks for different regions based on pixel intensity
# Adjust the thresholds as needed to isolate different regions
mask_gov = cv2.inRange(gray_image, 0, 100)      # Government (dark)
mask_rebels = cv2.inRange(gray_image, 51, 100) # Rebels (medium dark)
mask_kurds = cv2.inRange(gray_image, 101, 150) # Kurds (medium)
mask_al_nusra = cv2.inRange(gray_image, 151, 200) # Al-Nusra (medium light)
mask_isis = cv2.inRange(gray_image, 201, 255)  # ISIS (light)
mask_assad = cv2.inRange(gray_image, 50, 100)  # Assad (distinct shade)

# Create pattern images
def create_pattern(size, pattern_type):
    pattern = Image.new('L', (size, size), 255)
    draw = ImageDraw.Draw(pattern)
    if pattern_type == 'xxx':
        for i in range(0, size, 7):
            draw.line((i, 0, i, size), fill=0, width=1)
            draw.line((0, i, size, i), fill=0, width=1)
    elif pattern_type == '+++':
        for i in range(0, size, 7):
            draw.line((i, 0, i, size), fill=0, width=1)
            draw.line((0, i, size, i), fill=0, width=1)
            draw.line((i, 0, i + size, size), fill=0, width=1)
            draw.line((0, i, size, i + size), fill=0, width=1)
    elif pattern_type == '...':
        for i in range(0, size, 7):
            draw.line((i, 0, i, size), fill=0, width=1)
            draw.line((0, i, size, i), fill=0, width=1)
            draw.line((i, 0, i + size, size), fill=0, width=1)
            draw.line((0, i, size, i + size), fill=0, width=1)
    return np.array(pattern)

pattern_assad = create_pattern(50, '...')

# Create an output image with distinct shades of gray
output_image = np.zeros_like(gray_image)

# Apply different shades of gray to the masks
output_image[mask_gov > 0] = 0    # Dark gray for Government
# output_image[mask_rebels > 0] = 100  # Medium dark gray for Rebels
output_image[mask_kurds > 0] = 50  # Medium gray for Kurds
# output_image[mask_al_nusra > 0] = 200  # Medium light gray for Al-Nusra
output_image[mask_isis > 0] = 255  # Light gray for ISIS

# Apply pattern to Assad-controlled regions
def apply_pattern(mask, pattern):
    pattern_height, pattern_width = pattern.shape
    for i in range(0, mask.shape[0], pattern_height):
        for j in range(0, mask.shape[1], pattern_width):
            region = mask[i:i+pattern_height, j:j+pattern_width]
            pattern_region = pattern[:region.shape[0], :region.shape[1]]
            output_image[i:i+pattern_height, j:j+pattern_width][region > 0] = pattern_region[region > 0]

apply_pattern(mask_assad, pattern_assad)

# Display the original and converted images
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('Black and White Image with Multiple Shades of Gray and Patterns')
plt.imshow(output_image, cmap='gray')
plt.axis('off')

plt.show()

# Save the black and white image with multiple shades of gray and patterns
cv2.imwrite('syria_map_black_and_white_multiple_shades_patterns.png', output_image)
