#!/usr/bin/env python3
import subprocess
import os
import argparse

program_description = '''Build and run Xonsh tests in a fresh, controlled
    environment using venv '''

parser = argparse.ArgumentParser(description=program_description)

parser.add_argument('--clean', action='store_true')
parser.add_argument('--build', action='store_true')
parser.add_argument('--test', action='store_true')

# Use extra args to pass-through to py.test
args, extra_args = parser.parse_known_args()

if args.clean:
  subprocess.call(['git', 'clean',  '-f', '-d'])

if args.build:
  subprocess.call(['python3', '-m', 'venv', '.venv'])
  subprocess.call(['./.venv/bin/pip', 'install', '--upgrade', 'pip'])
  # use tests here, development.txt doesn't seem be necessary and in fact fails on OS X
  # due to py-inotify
  subprocess.call(['./.venv/bin/pip', 'install', '-r', './requirements/tests.txt'])
  subprocess.call(['./.venv/bin/pip', 'install', '-e', '.'])

if args.test:
  run_args = ['./.venv/bin/py.test'] + extra_args
  env = os.environ.copy()
  env['PATH'] = './.venv/bin:' + env['PATH']
  subprocess.call(run_args, env=env)
