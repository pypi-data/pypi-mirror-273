import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cwslib',
    version='1.0.0',
    author='jiangli',
    author_email='1329084163@qq.com',
    license='MIT License',
    description="Packages related to Consistent Weighted Sampling Algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiangli0618/cwslib",
    packages=setuptools.find_packages(),
    data_files=[('cwslib/cpluspluslib', ['cwslib/cpluspluslib/cws_fingerprints.dll']),('cwslib/cpluspluslib', ['cwslib/cpluspluslib/cws_fingerprints.so'])],
    install_requires=['numpy>=1.15.0', 'scipy>=1.1.0'],

)
