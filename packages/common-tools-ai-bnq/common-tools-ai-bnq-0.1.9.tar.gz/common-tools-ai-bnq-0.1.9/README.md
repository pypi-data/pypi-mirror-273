## 打包和上传

使用以下命令来生成和上传分发包：

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

## 类说明

### 1. `NacConnect` 类

用于连接 Nacos 服务，获取配置文件信息。

#### 参数信息

- `server_addresses`：地址
- `namespace`：命名空间
- `username`：用户名
- `password`：密码
- `group`：组合字典，包括 `group_name` 和 `data_ids`
- `conf_type`：配置文件类型，非必需，值为 `json` 或 `yaml`

#### 示例

```python
from bnq_py_core import NacConnect

test_data = {
    'group': {'t-dev': ['project_name_1', 'project_name_2']},
    'username': 'nacos',
    'password': 'nacos',
    'server_addresses': '127.0.0.1:8080',
    'namespace': 't-dev'
}
conf_test = NacConnect(**test_data)
print(conf_test())
```

### 2. `LoggingRecord` 类

用于记录日志信息。

#### 参数信息

- `max_bytes`：日志文件最大大小，默认值 20M
- `backup_count`：日志备份最大数量，默认值为 10
- `log_level`：日志级别，默认值为 `INFO`
- `log_dir`：日志文件路径，默认在根目录下创建 `log` 文件夹

#### 示例

```python
import logging

from bnq_py_core import LoggingRecord

testLog = LoggingRecord(log_level=logging.DEBUG)
for i in range(10):
    print(i, 'i')
    print(testLog, "testLog")
    testLog.debug(i)
    testLog.info("中文测试")
    testLog.error(i)
    testLog.warning(i)
    testLog.exception(i)
```

### 3. `LoggingRecordTimeRotation` 类

用于记录日志信息, 可根据设定时间自动轮转日志文件。

#### 参数信息

- `max_bytes`：日志文件最大大小，默认值 20M
- `backup_count`：日志备份最大数量，默认值为 10
- `log_level`：日志级别，默认值为 `INFO`
- `log_dir`：日志文件路径，默认在根目录下创建 `log` 文件夹

#### 示例

```python
import logging

from bnq_py_core import LoggingRecordTimeRotation

testLog = LoggingRecordTimeRotation(log_level=logging.DEBUG)
for i in range(10):
    print(i, 'i')
    print(testLog, "testLog")
    testLog.debug(i)
    testLog.info("中文测试")
    testLog.error(i)
    testLog.warning(i)
    testLog.exception(i)
```
### 4. `SingletonMeta` 类

用于实现单例模式。

#### 示例

```python
from bnq_py_core import SingletonMeta


class TestClass(metaclass=SingletonMeta):
    def __init__(self):
        pass
```

### 5. `CosConnect` 类

用于连接腾讯云存储平台 COS。

#### 参数信息

- `secret_id`：腾讯云 secret_id
- `secret_key`：腾讯云 secret_key
- `region`：腾讯云存储区域

#### 示例

```python
from bnq_py_core import CosConnect

test_data = {
    'secret_id': 'AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'secret_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'region': 'ap-guangzhou'
}
cos_test = CosConnect(**test_data)

```