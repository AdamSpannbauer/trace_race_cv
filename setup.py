from setuptools import setup, find_packages

version = {}
with open("trace_race/version.py") as f:
    exec(f.read(), version)

setup(
    name='trace_race',
    version=version['__version__'],
    description='Play the Mario Party mini-game, "Trace Race", using object tracking.',
    author='Adam Spannbauer',
    author_email='spannbaueradam@gmail.com',
    url='https://github.com/AdamSpannbauer/trace_race_cv',
    license='MIT',
    packages=find_packages(),
    package_data={
        '': ['*.png', '*.jpg']
    },
    install_requires=[
        'numpy',
        'imutils',
    ],
    extras_require={
        'cv2': ['opencv-contrib-python >= 3.4.0'],
        'flask': ['flask']
    },
    keywords=['video stabilization', 'game', 'image processing', 'computer vision'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ]
)
