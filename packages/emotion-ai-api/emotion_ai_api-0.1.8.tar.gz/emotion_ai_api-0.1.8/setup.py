from setuptools import setup, find_packages

setup(
    name='emotion_ai_api',
    version='0.1.8',
    author='Wes Lagarde',
    author_email='weslagarde@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',  # Assuming requests is a dependency; add others as needed
    ],
    description='A Python client for interfacing with Emotion AI API services.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://api.emotion-ai.io',  # Optional: your project's repo
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
