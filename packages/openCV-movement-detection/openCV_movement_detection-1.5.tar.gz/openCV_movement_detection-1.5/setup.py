from setuptools import setup, find_packages

setup(
    name='openCV_movement_detection',
    version='1.5',
    author='Lenson',
    description='A Python library for movement detection with OpenCV.',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'imageio',
    ]
)
