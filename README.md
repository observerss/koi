# koi(西湖锦鲤)

A third-party (and incomplete) client library for aliyun.

Why? Because aliyun's python sdk is poor maintained and don't support python3.
Why not AWS? Because AWS only has one region in China, which is not as flexible as Aliyun when your business is very sensitive to low pings.

## Get Stared

```py
from koi.ecs import ECSClient

c = ECSClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET)

```

## What's Next?


