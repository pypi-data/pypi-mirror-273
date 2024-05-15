from setuptools import setup, find_packages
import os

def find_image_files(directory):
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                image_files.append(os.path.relpath(os.path.join(root, file), directory))
    return image_files

setup(
    name='pythfinder',
    version='0.0.3.5',
    license='MIT',
    author='Contraș Adrian',
    author_email='omegacoresincai@gmail.com',
    description='Motion Planning library designed for FLL teams',
    packages=find_packages(),
    keywords=[
        'motion-planning',
        'mobile-robots',
        'robotics',
        'first-lego-league',
        'first-robotics',
        'fll'
    ],
    install_requires=[''],
    package_data={'pythfinder': find_image_files('Images')}
    
)
