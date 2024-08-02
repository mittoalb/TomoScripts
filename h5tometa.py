import click
import h5py
import numpy as np
import os

def print_attrs_and_datasets(name, obj, output_file):
    # Print attributes of the object
    for key, value in obj.attrs.items():
        try:
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            output_file.write(f"{name}: {key} -> {value}\n")
        except Exception as e:
            output_file.write(f"Error processing attribute {key} in {name}: {e}\n")

    # Print datasets
    if isinstance(obj, h5py.Dataset):
        try:
            data = np.array(obj)
            output_file.write(f"{name} dataset values: {data}\n")
        except Exception as e:
            output_file.write(f"Error processing dataset {name}: {e}\n")

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def process_hdf5(file_path):
    output_path = os.path.splitext(file_path)[0] + ".txt"
    with open(output_path, 'w', encoding='utf-8') as output_file:
        with h5py.File(file_path, 'r') as f:
            f.visititems(lambda name, obj: print_attrs_and_datasets(name, obj, output_file))

    print(f"Output saved to {output_path}")

if __name__ == '__main__':
    process_hdf5()
