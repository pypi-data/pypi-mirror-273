from setuptools import find_packages, setup
with open('README.md', 'r', encoding='utf-8') as fileso:
    readme = fileso.read()

install = ["tqdm>=4.64.1",
           "tenacity>=8.2.2",
           "requests>=2.27.1",
           "pycryptodome>=3.20.0,<4.0.0"]

setup(name='megaxdl',
      version='0.0.1',
      python_requires='~=3.10',
      packages=find_packages(),
      long_description=readme,
      install_requires=install,
      include_package_data=True,
      long_description_content_type='text/markdown')
