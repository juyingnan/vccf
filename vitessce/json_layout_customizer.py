import json
import os


def process_file(json_file_path, spatial_width=10.0, max_width=12.0):
    print(f"Processing: {json_file_path}")
    # Load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Update the "spatial" component
    for component in data['layout']:
        if component['component'] == 'spatial' and component['w'] < spatial_width:
            print(f"\tUpdating 'spatial' component 'width' from {component['w']} to {spatial_width}")
            component['w'] = spatial_width

    # Update other components based on the new width of the "spatial" component
    for component in data['layout']:
        if component['component'] != 'spatial' and component['x'] == 6:
            print(f"\tUpdating '{component['component']}' component 'x' from {component['x']} to {spatial_width}")
            print(f"\tUpdating '{component['component']}' component 'width' from {component['w']} to 2")
            component['x'] = spatial_width
            component['w'] = max_width - spatial_width

    # Save the updated JSON back to the file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=2)


# Root path
root_path = r'C:\Users\bunny\Desktop\vignette_VCCF'

# Walk through the root directory and its subdirectories
for subdir, _, files in os.walk(root_path):
    for file_name in files:
        # Look for vitessce.json files
        if file_name == 'vitessce.json':
            full_file_path = os.path.join(subdir, file_name)
            process_file(full_file_path)
