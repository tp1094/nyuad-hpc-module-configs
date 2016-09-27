import os
import unittest
import subprocess

#Don't rebuild the env
environment_1 = '''
name: env-1
dependencies:
  - perl-threaded
channels:
  - bioconda
'''

environment_2 = '''
name: env-1
rebuild: 1
dependencies:
  - perl-threaded
channels:
  - bioconda
'''


def run(command):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    stdout, stderr = process.communicate()
    status = process.returncode
    return (stdout, stderr, status)

def create_env(content, filename='environment.yml'):
    with open(filename, 'w') as fenv:
        fenv.write(content)

def remove_env_file(filename='environment.yml'):
    os.remove(filename)

class IntegrationTest(unittest.TestCase):
    def assertStatusOk(self, status):
        self.assertEqual(status, 0)

    def assertStatusNotOk(self, status):
        self.assertNotEqual(0, status)

    def test_rebuild(self):
        create_env(environment_2)
        o, e, s = run('gencore_app build_envs --environments environment.yml')
        self.assertStatusOk(s)
        o, e, s = run('gencore_app build_docs --environments environment.yml')
        self.assertStatusOk(s)
        o, e, s = run('gencore_app build_man --environments environment.yml')
        self.assertStatusOk(s)
        o, e, s = run('gencore_app upload_envs --environments environment.yml')

    def test_no_rebuild(self):
        create_env(environment_1)
        o, e, s = run('gencore_app build_envs --environments environment.yml')
        self.assertStatusOk(s)
        o, e, s = run('gencore_app build_docs --environments environment.yml')
        self.assertStatusOk(s)
        o, e, s = run('gencore_app build_man --environments environment.yml')
        self.assertStatusOk(s)
        o, e, s = run('gencore_app upload_envs --environments environment.yml')


    def tearDown(self):
        run('rm -f environment.yml')

if __name__ == '__main__':
    unittest.main()
