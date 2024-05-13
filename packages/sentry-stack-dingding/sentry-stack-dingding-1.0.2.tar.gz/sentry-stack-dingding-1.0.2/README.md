# Sentry-DingDing

Fork `https://github.com/FeSeason/sentry-10-dingding.git`

* feature-1:
Fix  `Sentry 10 or the same error`

[sentry-dingding issues](https://github.com/anshengme/sentry-dingding/issues/22)

```
'Event' object has no attribute 'id' 
```

* feature-2:
add stack preview in dingding

## 安装
* requirement.txt 方式:
```
    sentry-stack-dingding
```

* sentry/enhance-image.sh 方式
```sh
    # 在sentry/enhance-image.sh 添加 pip install sentry-stack-dingding
    # 然后 sudo ./install.sh
```

* docker-compose 方式：直接改成这个插件包就好了

如果帮你解决了问题，麻烦给个小星星.

## 构建
```sh
python3 setup.py sdist bdist_wheel
twine upload --repository testpypi dist/*
twine upload --repository pypi dist/*
```

