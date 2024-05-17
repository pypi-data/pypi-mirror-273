from setuptools import setup

setup(
    name="camera-ui-python-types",
    version="0.1.37",
    description="camera.ui python types",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seydx/camera.ui",
    author="seydx",
    author_email="dev@seydx.com",
    maintainer="seydx",
    maintainer_email="dev@seydx.com",
    packages=["camera_ui_python_types"],
    license="MIT",
    python_requires=">=3.9",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "typing_extensions",
        "rx",
        "numpy",
        'Pillow; sys_platform != "linux" or platform_machine != "x86_64"',
        'pillow-simd; sys_platform == "linux" and platform_machine == "x86_64"',
    ],
)
