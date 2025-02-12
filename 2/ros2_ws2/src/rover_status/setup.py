from setuptools import find_packages, setup

package_name = 'rover_status'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sai',
    maintainer_email='no@no.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['rover_health=rover_status.health_stat_pub:main',
                            'rover_battery=rover_status.rover_status:main',
                            'rover_status = status_subscriber:main'
                            
        ],
    },
)
