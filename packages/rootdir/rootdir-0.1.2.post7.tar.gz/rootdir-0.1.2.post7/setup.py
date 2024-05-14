import setuptools

setuptools.setup(
    name = 'rootdir',
    version = '0.1.2-7',
    description = 'get python root directory easily',
    author = 'meansoup',
    author_email = 'alsrnr1210@gmail.com',
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    url = 'https://github.com/meansoup/rootdir',
    include_package_data = True,
    packages=setuptools.find_packages(),
)