import subprocess


def generate_graphs():
    for package in ["", "event", "communications"]:
        subprocess.run(
            ["pyreverse", f"../iot_firmware/{package}", "-d", "graphs", "-p", package]
        )


if __name__ == "__main__":
    generate_graphs()
