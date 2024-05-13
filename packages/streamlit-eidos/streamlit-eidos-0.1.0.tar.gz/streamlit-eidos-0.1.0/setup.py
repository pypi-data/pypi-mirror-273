from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-eidos",
    version="0.1.0",
    author="Oceanum",
    author_email="developers@oceanum.science",
    description="Streamlit component for EIDOS framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["streamlit_eidos"],
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.7",
    keywords=["streamlit", "oceanum", "eidos", "visualisation"],
    install_requires=["streamlit>=1.2", "oceanum"],
    entry_points={},
)
