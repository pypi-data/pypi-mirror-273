from setuptools import setup, find_packages

setup(
    name='seatbelt-sdk',
    version='1.0.0',
    description='SDK for detecting seatbelt violations in images and videos',
    author='Your Name',
    author_email='your@email.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'opencv-python',
        'ultralytics',
        'pymongo'
        # Add other dependencies as needed
    ],
)
