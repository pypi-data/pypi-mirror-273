from setuptools import setup, find_packages

setup(
    name='ps_game_21',  # 包名
    version='0.0.1',  # 版本
    description='简单的21点扑克牌游戏',  # 描述
    author='Ps',  # 作者
    packages=find_packages(),  # 自动发现并包含项目中的所有Python包和子包
    python_requires='>=3.11.4',  # 指定Python版本要求
)
