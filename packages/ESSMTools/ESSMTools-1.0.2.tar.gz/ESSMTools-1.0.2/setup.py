from setuptools import setup, find_packages

setup(
    name = 'ESSMTools',
    version = '1.0.2',
    description = "Ecosystem Service Scoring and Management tools",
    url = 'https://github.com/MG-Choi/ESSM',
    author = 'Moongi Choi, Jang-Hwan Jo',
    author_email = 'mongil030233@gmail.com',
    packages = find_packages(),
    package_data = {'ESSMTools': ['sampleData/ES_scoring/Mireuksan_sample.cpg', 'sampleData/ES_scoring/Mireuksan_sample.dbf', 'sampleData/ES_scoring/Mireuksan_sample.prj',
                             'sampleData/ES_scoring/Mireuksan_sample.sbn', 'sampleData/ES_scoring/Mireuksan_sample.sbx', 'sampleData/ES_scoring/Mireuksan_sample.shp',
                             'sampleData/ES_scoring/Mireuksan_sample.shp.xml', 'sampleData/ES_scoring/Mireuksan_sample.shx']},
    include_package_data = True,
    install_requires = ['tqdm',
                        'numpy',
                        'pandas',
                        'geopandas>=0.14.0']
)







'''
note: How to make library
- 모두 seqC -> py로 저장.

- cmd (administrator) -> cd repository
- python setup.py sdist bdist_wheel

- 이후 upload를 위해 https://pypi.org/manage/account/token/ 여기서 token을 받아야함. 그리고 밑에 처럼 토큰을 입력.
- 예로 토큰이 pypi-asdadsdas-adwdas 라면
- twine upload dist/* -u __token__ -p pypi-asdadsdas-adwdas
  아니면 twine upload dist/* 하고 token 입력
- 업데이트시에는 setup.py -> 0.02로 하고 다시 위 과정 반복

twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDJiNmQ5OTRhLTFiZDQtNDIxNS04NjM0LTRmOTQ5NjQzMDUyNwACKlszLCIyYjI3OWNjMi1lYjE1LTQ3YTgtYTA3YS0zZjM5ZGIwOWMxZDEiXQAABiBDqinSY-9FQjkdFk1zeN1ELZCvDbz3OSeyfMQaR-gg3w

library test는 cmd에서 한다.

- pip uninstall 
- pip install sequentPSS


* 주의할 점:
random이나 os와 같이 깔려있는 library의 경우 위에 install_requires에 쓰지 않는다. py안에 바로 import로 쓰면 된다.

'''


#repository: C:\Users\MoongiChoi\Desktop\MG\양식, 코드 등\Python\Library\indoorCont

#참고:https://lsjsj92.tistory.com/592
#https://developer-theo.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-GitHub-Repository-%EC%83%9D%EC%84%B1%EB%B6%80%ED%84%B0-PyPI-Package-%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80

#위에서 버전 문제 발생: !pip install --upgrade requests
