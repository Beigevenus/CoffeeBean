from distutils.core import setup
from distutils.command.install_data import install_data


class PostInstall(install_data):
    def run(self):
        install_data.run(self)

        # DB code goes here


setup(name="CoffeeBean",
      author="Zoe Skye",
      url="https://github.com/Beigevenus/CoffeeBean",
      packages=["discord~=2.1.0", "python-dotenv~=1.0.0"],
      cmdclass={"install_data": PostInstall},
      )
