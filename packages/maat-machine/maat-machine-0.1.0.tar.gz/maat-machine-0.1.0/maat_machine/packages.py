import sys
import subprocess

def install_packages(packages):
    for package in ['pip'] + packages:
        print('============================================================')
        print(f"✔️ Installing '{package}'...")
        proc = subprocess.Popen([sys.executable, '-m', 'pip', 'install', '--upgrade', package], stdout=subprocess.PIPE)
        output = proc.stdout.read().decode('utf-8')
        print(output)
        print('============================================================')
