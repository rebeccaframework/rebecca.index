from setuptools import setup, find_packages

requires = [
    "zope.index",
    "igo-python",
]

tests_require = [
    "pytest",
    "webtest",
    "pyramid",
    "pyramid_zodbconn",
    "pyramid_tm",
    "repoze.catalog",
    "pytest-cov",
]

setup(name="rebecca.index",
      namespace_packages=["rebecca"],
      packages=find_packages("src"),
      package_dir={"": "src"},
      install_requires=requires,
      tests_require=tests_require,
      extras_require={
          "testing": tests_require,
      },
)
