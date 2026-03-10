from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
EXT = ROOT / 'external' / 'autoemulate'


def main():
    EXT.parent.mkdir(parents=True, exist_ok=True)
    if not EXT.exists():
        subprocess.check_call(['git', 'clone', 'https://github.com/alan-turing-institute/autoemulate', str(EXT)])
    subprocess.check_call(['python', '-m', 'pip', 'install', '-e', str(EXT)])
    print('autoemulate ready', EXT)


if __name__ == '__main__':
    main()
