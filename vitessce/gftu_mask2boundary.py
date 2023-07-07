# Your existing libraries
import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()
import cv2
import numpy as np
import json
import os

# Additional libraries for GeoJSON format
from shapely.geometry import mapping, Polygon

save_boundary_img = False

# Root directory containing the folders
ROOT_DIR = r'C:\Users\bunny\Desktop\test'  # replace this with your root directory

# List of directories
directories = [os.path.join(ROOT_DIR, str(i)) for i in range(1, 6)]

for directory in directories:
    # List all png files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            filepath = os.path.join(directory, filename)

            # Load the image
            img = cv2.imread(filepath, 0)

            # Threshold the image: this will create a binary image from source image
            _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

            # Find contours: This will give you the boundaries of the white object.
            # Note: This will alter the source image
            contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if save_boundary_img:
                # Create an empty image to store the contours
                boundary_img = np.zeros_like(img)

                # Draw contours on the empty image. Argument "-1" means drawing all contours
                cv2.drawContours(boundary_img, contours, -1, (255), 1)

                # Save the boundary image to PNG
                boundary_filepath = os.path.join(directory, filename.split('.')[0] + '_boundary.png')
                cv2.imwrite(boundary_filepath, boundary_img)

            # For GeoJSON, we'll create a Feature for each contour
            geojson_features = []
            for cnt in contours:
                if len(cnt) >= 4:
                    polygon = Polygon(shell=[tuple(pt[0]) for pt in cnt])
                    feature = {
                        "type": "Feature",
                        "id": "PathAnnotationObject",
                        "geometry": mapping(polygon)
                    }
                    geojson_features.append(feature)

            # Save to GeoJSON file
            json_filepath = os.path.join(directory, filename.split('.')[0] + '.json')
            with open(json_filepath, 'w') as f:
                json.dump(geojson_features, f)

            print(f"Boundary for {filename} has been saved to {json_filepath}")
