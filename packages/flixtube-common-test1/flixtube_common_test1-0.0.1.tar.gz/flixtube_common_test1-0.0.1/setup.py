import setuptools

setuptools.setup(
  name = "flixtube_common_test1",
  version="0.0.1",
  author="me",
  description="Common code for the FlixTube application",
  packages=["cosmosdb"],
  install_requires=[
    'motor==3.4.0'
  ],
)