import yaml

def add_networks_section(filename):
    # Load the YAML file
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)

    # Define the network configuration
    network_config = {
        'name': 'default',
        'type': 'manual',
        'subnets': [
            {
                'range': '10.244.0.0/22',
                'gateway': '10.244.0.1',
                'static': ['10.244.0.34 - 10.244.0.50'],
                'cloud_properties': {'name': 'random'}
            }
        ]
    }

    # Add the networks section to the top level if it doesn't exist
    if 'networks' not in data:
        data['networks'] = [network_config]

    # Ensure each instance group has a networks section
    for instance_group in data.get('instance_groups', []):
        if 'networks' not in instance_group:
            instance_group['networks'] = [{'name': 'default'}]
        elif not any(net['name'] == 'default' for net in instance_group['networks']):
            instance_group['networks'].append({'name': 'default'})

    # Write the updated YAML back to the file
    with open(filename, 'w') as file:
        yaml.safe_dump(data, file, default_flow_style=False)

# Specify the path to your cf-deployment.yml file
filename = 'cf-deployment.yml'
add_networks_section(filename)
print(f"Updated {filename} with the correct network configurations.")
