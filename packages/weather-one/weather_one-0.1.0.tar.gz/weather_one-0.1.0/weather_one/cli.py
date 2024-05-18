import requests
import click

@click.command()
@click.argument("metric", required=True)
@click.option("--latitude", "-lat", default=40.71, type=float, required=False, help="latitude (in degrees)")
@click.option("--longitude", "-lon", default=-74.01, type=float, required=False, help="longitude (in degrees)")
def cli(metric: str, latitude: float, longitude: float) -> None:
    r = requests.get('https://api.open-meteo.com/v1/forecast?latitude=' + str(latitude) + '&longitude=' + str(longitude) + '&current_weather=true')
    if r.status_code == 200:
        if metric in r.json()["current_weather"]:
            print(r.json()['current_weather'][metric])
        else:
            print("Metric not supported!")
    else:
        print("Open-Meteo is down!")

if __name__ == "__main__":
    cli()