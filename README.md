# gitcs
A simple, fast and powerful git code search tool was built by antx, which based on pocx.

## Description
Gitcs is a simple, fast and powerful git code search tool was built by antx, which based on pocx. Gitcs support engine and site list as follows:

- Github
- Gitlab
- Gitee

## Install

```bash
git clone https://github.com/antx-code/gitcs.git
```
## Install Dependencies
```shell
poetry install
```

## Usage
When you use gitcs to collect code related information, you must set config into config.yaml first. The Github module default config 
is not to search content detail for each matched record, if you want to search content detail, you must set parameter `is_detail` to `true` in github module.

### Gitcs Sample:

#### command line sample:

```shell
python3 gitcs.py target
```

#### python3 lib sample:

```python
# Title: xxxxxxx
# Author: antx
# Email: wkaifeng2007@163.com

from gitcs import dia

if __name__ == '__main__':
    dia('target')
```