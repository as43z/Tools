from setuptools import setup

setup(
    name="cv_management_create",
    version="1",
    py_modules=["cv_management_create"],
    entry_points={
        "console_scripts": ["cv-management-create = cv_management_create:main"]
    }
)
