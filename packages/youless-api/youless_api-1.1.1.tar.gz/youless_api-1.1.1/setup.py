import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='youless_api',
      version='1.1.1',
      description='A bridge for python to the YouLess sensor',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/gjong/youless-python-bridge',
      author='G. Jongerius',
      license='MIT',
      packages=setuptools.find_packages(exclude=("test",)),
      zip_safe=False)
