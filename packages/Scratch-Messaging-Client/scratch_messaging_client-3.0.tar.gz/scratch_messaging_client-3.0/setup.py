from setuptools import setup, find_packages # type: ignore

setup(
  name='Scratch-Messaging-Client',
  version='3.0',
  packages=find_packages(),
  install_requires=['scratchattach'
  ],
  
  entry_points={
    "console_scripts": [
      "SMC = SMC:SMC",
    ],
  },


)
