import tsugu_api
import tsugu_async
import unittest
import os
from PIL import Image
import io


class TestTsugu(unittest.IsolatedAsyncioTestCase):

    async def test_tsugu(self):
        async def show_back_msg(data):
            for i in data:
                if isinstance(i, str):
                    print(f"[文字信息]\n{i}")
                elif isinstance(i, bytes):
                    print(f"[图片信息]")
                    img = Image.open(io.BytesIO(i))
                    img.show()
                    print(f"[图像大小: {len(i) / 1024:.2f}KB]")

        # tsugu.database('./user_data.db')
        # tsugu_async.config.reload_from_json('./config.json')

        msg1 = await tsugu_async.handler('查试炼 -m', '1528593481', 'red', '666808414')
        await show_back_msg(msg1)

        # msg2 = await tsugu_async.handler('ycm', '1528593481', 'red', '666808414')
        # await show_back_msg(msg2)

        # msg3 = await tsugu_async.handler('12324 测q1试', '1528593481', 'red', '666808414')
        # await show_back_msg(msg3)

        # print(tsugu_api.get_user_data('red', '1528593481'))


if __name__ == '__main__':
    unittest.main()
