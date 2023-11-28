import subprocess
import helpers.config as config


if __name__ == "__main__":
    for node, content in config.Nodes.items():
        args = 'start python node.py ' + node
        print(args)
        subprocess.run(args, shell=True)

    subprocess.run('start python client.py', shell=True)
