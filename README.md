# koi(西湖锦鲤)

A third-party (and incomplete) client library for aliyun.

Why reinvent the wheel when there is official SDK? 

- Aliyun's Python SDK is poor maintained.
- It doesn't support Python3.
- It's design is weird, sugar methods are to rescue.

Why not AWS, why the hell do anyone want Aliyun over AWS?

- AWS only has one region in China, which is not as flexible as Aliyun when your business is very sensitive to network location.
- AWS sucks on ICP备案 what is the key prerequisite to all internet services within China.
- AWS China is not the same thing as AWS Global. For example, it lacks spot instances; its pricing is weird, too.

## Get Stared

```py
from koi.ecs import ECSClient

c = ECSClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
c.describe_regions()
```

## What's Next?

There's no docs, read the source for more details, yay!
Read Aliyun docs may also help: https://docs.aliyun.com/#/pub/ecs/open-api/summary
