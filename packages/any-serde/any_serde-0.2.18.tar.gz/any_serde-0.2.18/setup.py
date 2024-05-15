from setuptools import find_packages, setup

setup(
    name="any_serde",
    version="0.2.18",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={
        "": ["*py.typed"],
    },
    data_files=[
        (
            "any_serde/typescript",
            [
                "any_serde/typescript/bool_typedef.ts.jinja2",
                "any_serde/typescript/dataclass_typedef.ts.jinja2",
                "any_serde/typescript/float_typedef.ts.jinja2",
                "any_serde/typescript/int_typedef.ts.jinja2",
                "any_serde/typescript/list_typedef.ts.jinja2",
                "any_serde/typescript/literal_typedef.ts.jinja2",
                "any_serde/typescript/none_typedef.ts.jinja2",
                "any_serde/typescript/nonetype_typedef.ts.jinja2",
                "any_serde/typescript/string_typedef.ts.jinja2",
                "any_serde/typescript/union_typedef.ts.jinja2",
            ],
        ),
    ],
)
