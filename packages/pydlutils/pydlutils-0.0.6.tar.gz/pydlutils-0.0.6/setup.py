from setuptools import setup, find_packages

VERSION = "0.0.6"
DESCRIPTION = "Utility library for deep learning"


def main():
    INSTALL_REQUIRES = []
    DEPENDENCY_LINKS = []

    with open("./requirements.txt", "r") as file:
        for line in file.readlines():
            line = line.strip()
            if (not line) or line.startswith("#"):
                continue
            if line.startswith("git+"):
                DEPENDENCY_LINKS.append(line)
                INSTALL_REQUIRES.append(line.split("#egg=")[1])
            else:
                INSTALL_REQUIRES.append(line)

        with open("./README.md", encoding="utf-8") as f:
            LONG_DESCRIPTION = f.read()
    excludes = ["output", "artifacts"]

    setup(
        name="pydlutils",
        version=VERSION,
        author="zebincai",
        author_email="1028798080@qq.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        packages=find_packages(exclude=excludes),
        url="https://github.com/zebincai/pydlutils",
        download_url="https://github.com/zebincai/pydlutils/tags",
        install_requires=INSTALL_REQUIRES,  # add any additional packages that
        dependency_links=DEPENDENCY_LINKS,
        include_package_data=True,
        keywords=["python", "compute vision", "deep learning", "LLM"],
        license="Apache",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "Topic :: Software Development",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
        ],
    )


if __name__ == "__main__":
    main()
