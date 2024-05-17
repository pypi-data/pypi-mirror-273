import argparse
import subprocess
import os
import configparser

CONFIG_FILE = os.path.expanduser("~/.badger_config")


def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        exit(result.returncode)


def build(skip_tests):
    command = "mvn package"
    if skip_tests:
        command += " -DskipTests=true"
    print(f"Running command: {command}")
    run_command(command)


def run(run_script):
    if not os.path.exists(run_script):
        print(f"Run script not found: {run_script}")
        exit(1)
    print(f"Running command: {run_script}")
    run_command(run_script)


def get_badger_directory():
    if not os.path.exists(CONFIG_FILE):
        return None

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.get('settings', 'badger_directory', fallback=None)


def set_badger_directory(directory):
    config = configparser.ConfigParser()
    config['settings'] = {'badger_directory': directory}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def main():
    parser = argparse.ArgumentParser(description="Badger Commerce CLI")
    parser.add_argument("build", nargs="?", help="Run the build command", default=None)
    parser.add_argument("options", nargs="*", help="Options for the build command", default=[])

    args = parser.parse_args()

    badger_directory = get_badger_directory()
    if not badger_directory:
        badger_directory = input("Enter the Badger installation directory: ").strip()
        set_badger_directory(badger_directory)

    run_script = os.path.join(badger_directory, "dev-scripts/devEnv.sh web")

    if args.build == "build":
        if "test" in args.options:
            build(skip_tests=False)
        else:
            build(skip_tests=True)

        if "run" in args.options:
            run(run_script)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
