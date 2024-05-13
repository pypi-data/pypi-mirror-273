from setuptools import setup, find_packages
import setuptools
import subprocess
import os

setup(
    name='image_input_handler',  # Package name
    version='0.2.5',  # Version of your package
    author='Enes Kuzucu',  # Your name

    description='A module to handle different formats of image input',  # Short description
    long_description=open('README.md').read(),  # Long description from a README file
    long_description_content_type='text/markdown',  # Type of the long description
#     url='https://github.com/karaposu/image-input-handler',  # URL to the repository
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'numpy', 'opencv-python', 'Pillow', 'urllib3'  # List of dependencies
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Development status
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # License as you choose
        'Programming Language :: Python :: 3',  # Supported Python versions
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Minimum version requirement of Python
)



# cf_remote_version = (
#     subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
#     .stdout.decode("utf-8")
#     .strip()
# )
#
# if "-" in cf_remote_version:
#     # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
#     # pip has gotten strict with version numbers
#     # so change it to: "1.3.3+22.git.gdf81228"
#     # See: https://peps.python.org/pep-0440/#local-version-segments
#     v,i,s = cf_remote_version.split("-")
#     cf_remote_version = v + "+" + i + ".git." + s
#
# assert "-" not in cf_remote_version
# assert "." in cf_remote_version
#
# assert os.path.isfile("cf_remote/version.py")
# with open("cf_remote/VERSION", "w", encoding="utf-8") as fh:
#     fh.write("%s\n" % cf_remote_version)
#
# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()