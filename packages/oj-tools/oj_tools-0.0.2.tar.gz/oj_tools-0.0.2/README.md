# oj-tools

[QingdaoU/OnlineJudge](https://github.com/QingdaoU/OnlineJudge) 를 위한 테스트케이스 생성기입니다.

```python
from oj import TestCase
from oj import makezip


# TestCase for A+B

test_cases = [
    TestCase(
        id="1",
        input="2 3",
        output="5",
    ),
    TestCase(
        id="2",
        input="99 100",
        output="199",
    ),
]




```
