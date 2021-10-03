import subprocess


def generate_graphs():
    subprocess.run(
        ["pyreverse", "../iot_firmware/event", "-d", "graphs", "-p", "event"]
    )


if __name__ == "__main__":
    generate_graphs()
