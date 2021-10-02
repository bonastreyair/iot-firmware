import subprocess


def main():
    subprocess.run(["pyreverse", "../iot_firmware", "-d", "graphs"])
    subprocess.run(
        ["pyreverse", "../iot_firmware/event", "-d", "graphs", "-p", "event"]
    )


if __name__ == "__main__":
    main()
