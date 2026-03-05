import os, json, shutil, datetime
import torch


def make_run_dir(output_root):
    run_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out = os.path.join(output_root, run_id)
    os.makedirs(out, exist_ok=True)
    os.makedirs(os.path.join(out, 'frames'), exist_ok=True)
    return out


def save_config_copy(config_path, out_dir):
    shutil.copy2(config_path, os.path.join(out_dir, 'config.yaml'))


def log_line(out_dir, txt):
    with open(os.path.join(out_dir, 'run.log'), 'a') as f:
        f.write(txt + '\n')


def save_snapshot(out_dir, step, payload):
    p = os.path.join(out_dir, f'step_{step:04d}.pt')
    torch.save(payload, p)
