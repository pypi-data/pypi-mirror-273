from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name='kakao_api_vet1ments',
    description="카카오 로그인 rest api",
    version='0.1.6',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.11.0',
    author="no hong seok",
    author_email="vet1ments@naver.com",
    maintainer="no hong seok",
    maintainer_email="vet1ments@naver.com",
    project_urls={
        "Repository": "https://github.com/vet1ments/kakao_api"
    },
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "httpx>=0.27.0"
    ],
)