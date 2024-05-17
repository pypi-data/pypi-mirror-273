import calling_rate

import typer

curator = typer.Typer(help="Tools to clean calling rates data")


@curator.command()
def write_recording_coordinates(shp_path: str, output_path: str):
    recording_coordinates_df = calling_rate.get_recording_coordinates(shp_path)
    recording_coordinates_df.to_csv(output_path, index=False)


@curator.command()
def write_recording_data(shp_path: str, output_path: str):
    recording_data_df = calling_rate.get_recording_data(shp_path)
    recording_data_df.to_csv(output_path, index=False)


@curator.command()
def version():
    version = calling_rate.__version__
    print(version)
