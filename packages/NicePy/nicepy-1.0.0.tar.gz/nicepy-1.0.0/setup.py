import setuptools

setuptools.setup(
  name = "NicePy",
  version = "1.0.00",
  author = "Jim Weiler",
  description = "An API library for NICE CXOne",
  packages=["NicePy"],
  install_requires = [
    'requests',
    'requests-oauthlib',
    'oauthlib',
    'python-dateutil',
    'pydub',
    'joblib',
    'tzlocal',
    'debugpy'
  ]
)