#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import orm, asyncio
from models import User, Blog, Comment


@asyncio.coroutine
def test(loop):
        yield  from orm.create_pool(loop =loop, user='root', password='test123', db='etcyouhui', charset='utf8')
        u = User(name='Test', email='test@example.com', password='1234567890', image='about:blank')
        yield from u.save()
        yield from orm.destory_pool()

loop = asyncio.get_event_loop()
if __name__=='__main__':
    test(loop)
    loop.run_until_complete(test(loop))
    loop.close()






