from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
          name="geotaichi",
          version="0.1.0",
          author="Shi-YiHao",
          author_email="syh-1999@outlook.com",
          description="A Taichi-powered high-performance numerical simulator for multiscale geophysical problems",
          long_description=long_description,
          long_description_content_type="text/markdown",
          url="https://github.com/Yihao-Shi/GeoTaichi",
          packages=find_packages(exclude=('geotaichi', 'src', 'example')),
          include_package_data=True,
          python_requires='>=3.8,<=3.11',
          install_requires=[
                               'taichi==1.6.0',
                               'numpy==1.23.5',
                               'psutil',
                               'pynvml',
                               'scipy==1.10.1',
                               'trimesh==3.20.1',
                               'shapely==1.8.0',
                               'rtree'
                           ],
          classifiers=[
                          'Programming Language :: Python :: 3.8',
                          'Programming Language :: Python :: 3.9',
                          'Programming Language :: Python :: 3.10',
                          'License :: OSI Approved :: GNU Affero General Public License v3',
                          'Development Status :: 3 - Alpha'
                      ]
    )
