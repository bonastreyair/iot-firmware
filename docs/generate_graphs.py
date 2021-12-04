import os
import subprocess

DIRECTORY = "graphs"
PACKAGES = ["", "event", "communications"]


def generate_graphs():
    os.makedirs(DIRECTORY, exist_ok=True)
    for package in PACKAGES:
        subprocess.run(
            ["pyreverse", f"../iot_firmware/{package}", "-d", DIRECTORY, "-p", package]
        )


if __name__ == "__main__":
    generate_graphs()
