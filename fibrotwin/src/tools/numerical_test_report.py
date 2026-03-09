import json
import subprocess
import sys
from pathlib import Path


def main():
    # collect tests
    py = sys.executable
    collect = subprocess.check_output([py, '-m', 'pytest', '--collect-only', '-q'], text=True)
    tests = [ln.strip() for ln in collect.splitlines() if '::' in ln]

    # run tests
    run = subprocess.run([py, '-m', 'pytest', '-q'], capture_output=True, text=True)
    out = run.stdout + '\n' + run.stderr

    passed = None
    m = None
    import re
    m = re.search(r'(\d+) passed', out)
    if m:
        passed = int(m.group(1))

    report = {
        'n_collected': len(tests),
        'n_passed': passed,
        'exit_code': run.returncode,
        'tests': tests,
        'raw_tail': '\n'.join(out.splitlines()[-25:]),
    }

    Path('outputs/numerical_test_report.json').write_text(json.dumps(report, indent=2))

    lines = ['# Numerical Test Report', '', f"Collected: {report['n_collected']}", f"Passed: {report['n_passed']}", f"Exit code: {report['exit_code']}", '']
    lines.append('## Tests')
    for t in tests:
        lines.append(f"- {t}")
    lines.append('')
    lines.append('## pytest tail')
    lines.append('```')
    lines.append(report['raw_tail'])
    lines.append('```')
    Path('outputs/numerical_test_report.md').write_text('\n'.join(lines))

    print(json.dumps({'n_collected': len(tests), 'n_passed': passed, 'exit_code': run.returncode}, indent=2))


if __name__ == '__main__':
    main()
