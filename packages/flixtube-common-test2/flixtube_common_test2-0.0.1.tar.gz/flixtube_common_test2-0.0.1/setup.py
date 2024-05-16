import setuptools

setuptools.setup(
  name = "flixtube_common_test2",
  version="0.0.1",
  author="me",
  description="Common code for the FlixTube application",
  install_requires=[
    'motor==3.4.0'
  ],
  package_dir = {"": "src"},
  packages = setuptools.find_packages(where="src"),
  python_requires = ">=3.6"
)