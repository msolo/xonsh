#!/usr/bin/env python3
import subprocess
import os
import argparse

program_description = '''Build and run Xonsh in a fresh, controlled
    environment using docker '''

parser = argparse.ArgumentParser(description=program_description)

parser.add_argument('--clean', action='store_true')
parser.add_argument('--build', action='store_true')
parser.add_argument('--test', action='store_true')

parser.add_argument('--debug-shell', action='store_true')
parser.add_argument('--shell', action='store_true')

parser.add_argument('--python', '-p', default='3.9', metavar='python_version')

args, extra_args = parser.parse_known_args()

if args.clean:
  subprocess.call(['docker', 'rmi',  'xonsh'])

if args.build:
  # docker_script = '''
  # from python:{python_version}
  # RUN mkdir -p /xonsh-base/requirements
  # ENV DEBIAN_FRONTEND=noninteractive
  # ADD ./requirements/ /xonsh-base/requirements
  # RUN apt-get update && apt-get install -y bash-completion man
  # RUN pip install --upgrade pip && pip install -r /xonsh-base/requirements/tests.txt
  # '''.format(
  #     python_version=args.python,
  # )
  docker_script = '''
  from python:{python_version}
  ENV DEBIAN_FRONTEND=noninteractive
  RUN apt-get update && apt-get install -y bash-completion man
  '''.format(
      python_version=args.python,
  )

  print('Building and running Xonsh')
  print('Using python ', args.python)

  with open('./Dockerfile', 'w+') as f:
      f.write(docker_script)

  subprocess.call(['docker', 'build', '-t', 'xonsh', '.'])
  os.remove('./Dockerfile')


# Create an ephemeral container that mounts the git source in /xonsh
run_args = ['docker', 'run', '-ti', '-v', os.getcwd() + ':/xonsh', '--name', 'xonsh-dev', '--rm', '-w', '/xonsh', 'xonsh']
# for e in args.env:
#   run_args += ['-e', e]

if args.build:
  subprocess.call(run_args + ['./xonsh-venvctl.py', '--build'])


if args.test:
  test_cmd = ['./xonsh-venvctl.py', '--test'] + extra_args
  subprocess.call(run_args + test_cmd)

if args.debug_shell:
  # Run a debug shell using trusty bash
  shell_cmd = ['/bin/bash'] + extra_args
  subprocess.call(run_args + shell_cmd)

if args.shell:
  # Run a xonsh
  shell_cmd = ['./.venv/bin/xonsh'] + extra_args
  subprocess.call(run_args + shell_cmd)
