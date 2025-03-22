import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

rho= 0.002377 # slug/ft^3
U = 80.38058  # ft/s
alpha_induced = 1 # degrees (induced angle)

# --------------------------------------------Set-Up----------------------------------------
# Image Upload
def extract_image_points(image_path, threshold=240):
    # Extracts non-white points from an image
    # threshold is an integer. Pixel values greater than 240 are considered white
    
    # Load Image
    image = Image.open(image_path)
    image = image.rotate(270, expand=True) #matplotlib has the orgin start at the top_left instead the conventional bottom-left for an image. Therefore, the image needs to be rotated 90 degrees counterclockwise

    # Convert image to RGB if it's not in RGB
    image = image.convert("RGB")

    image_array = np.array(image)
    
    #Check that the image is in RGB (3 channels)
    if image_array.ndim == 3 and image_array.shape[2] == 3:
        non_white_pixels = np.all(image_array < threshold, axis =-1)
    else:
        raise ValueError("The image must be in RGB format")
    
    # Coordinate Setting
    rows, cols =np.where(non_white_pixels)

    if len(rows) == 0 or len(cols) == 0:
        print("Error! Image uploaded needs to be an enclosed shape.")
        raise ValueError("Image uploaded needs to be an enclosed shape.")
    else:
        print("X Coordinates:", rows)
        print("Y Coordinates:", cols)
        print("X length:", len(rows))
        print("Y length:", len(cols))
        print("Y Coordinate Max:", np.max(cols))

    return rows, cols

# --------Trapezoidal Summation Method-------- #
def trapezoid_rule(x_array,y_array):
    
    x_data_samples = np.array(x_array)
    y_data_samples = np.array(y_array)

    area= 0
    for i in range(len(x_data_samples)-1):
        incremental_width = x_data_samples[i+1] - x_data_samples[i]
        incremental_height = (y_data_samples[i] + y_data_samples[i+1])/2
        area+= incremental_width*incremental_height
    return area
    
def gamma(image_path, threshold=240, point_color="blue", point_size=5):
    rows, cols = extract_image_points(image_path, threshold)

    Gamma = trapezoid_rule(rows, cols)
    lift=round(rho*U*Gamma, 2)
    drag=round(rho*U*Gamma*alpha_induced, 2)

    print("Gamma:", Gamma)
    print(f"Wing Span: {rows[-1]-rows[0]} ft")
    print(f"Lift: {lift} lb-ft")
    print(f"Drag: {drag} lb-ft")

    # Plot Coordinates
    plt.scatter(rows, cols, c=point_color, s= point_size, alpha=0.5, label="Non-white points")
    plt.xlabel("Circulation Distribution")
    plt.legend([f"Lift: {lift} lb-ft"], loc ="upper right")
    plt.show()

#-----------------------------------------------------------------------------------------

gamma("Capture4.jpg", threshold=240, point_color='blue', point_size=2)

