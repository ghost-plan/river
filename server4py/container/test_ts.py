from unittest import TestCase
from container.ts import pes_packet
from container import datas


class TestTS_all(TestCase):

    def test_audio_pes_packet(self):
        expected_ret = bytes([
            0x47, 0x41, 0x01, 0x31,
            0x81, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff,
            # pes header
            # 0x0, 0x0,  0x1,  0xc0, 0x0, 0x30, 0x80, 0x80, 0x5,  0x21, 0x0,  0x1 ,  0x7, 0xd1
            0x00, 0x00, 0x01, 0xc0, 0x00, 0x30, 0x80, 0x80, 0x05, 0x21, 0x00, 0x01, 0x00, 0x01,
            # pes payload
            0xaf, 0x01, 0x21, 0x19, 0xd3, 0x40, 0x7d, 0x0b, 0x6d, 0x44, 0xae, 0x81, 0x08, 0x00, 0x89, 0xa0, 0x3e,
            0x85, 0xb6, 0x92, 0x57, 0x04, 0x80, 0x00, 0x5b, 0xb7, 0x78, 0x00, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38,
            0x30, 0x00, 0x06, 0x00, 0x38])
        __TS_PACKET_SIZE = 188
        is_video = False
        is_keyframe = False
        es_buffer = bytes([0xaf, 0x01, 0x21, 0x19, 0xd3, 0x40, 0x7d, 0x0b, 0x6d, 0x44, 0xae, 0x81,
                           0x08, 0x00, 0x89, 0xa0, 0x3e, 0x85, 0xb6, 0x92, 0x57, 0x04, 0x80, 0x00, 0x5b, 0xb7,
                           0x78, 0x00, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x30, 0x00, 0x06, 0x00, 0x38,
                           ])
        a, ts_packet = pes_packet(es_buffer, is_video, is_keyframe, 0, 0)
        s = ''
        for i in range(0, __TS_PACKET_SIZE):
            p = ts_packet[i]
            line = (27 if is_video else 22)
            if len(s) == 0:
                s = hex(p)
            elif i == 4 or i == 12:
                s = s + ',\n' + hex(p)
            else:
                s = s + ',' + hex(p)
        print("=" * 20)
        print(a, s)
        for i in range(0, a):
            print(i, hex(ts_packet[i]))
            self.assertEqual(expected_ret[i], ts_packet[i])

    def test_video_pes_packet(self):
        expected_ret = bytes([
            0x47, 0x41, 0x01, 0x31,
            0x81, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff,
            # pes header
            # 0x0, 0x0,  0x1,  0xc0, 0x0, 0x30, 0x80, 0x80, 0x5,  0x21, 0x0,  0x1 ,  0x7, 0xd1
            0x00, 0x00, 0x01, 0xc0, 0x00, 0x30, 0x80, 0x80, 0x05, 0x21, 0x00, 0x01, 0x00, 0x01,
            # pes payload
            0xaf, 0x01, 0x21, 0x19, 0xd3, 0x40, 0x7d, 0x0b, 0x6d, 0x44, 0xae, 0x81, 0x08, 0x00, 0x89, 0xa0, 0x3e,
            0x85, 0xb6, 0x92, 0x57, 0x04, 0x80, 0x00, 0x5b, 0xb7, 0x78, 0x00, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38,
            0x30, 0x00, 0x06, 0x00, 0x38])
        __TS_PACKET_SIZE = 188
        is_video = True
        is_keyframe = True
        a, ts_packet = pes_packet(datas.data0['es'], is_video, is_keyframe, datas.data0['pts'], 1)
        # s = ''
        # for i in range(0, __TS_PACKET_SIZE):
        #     p = ts_packet[i]
        #     if len(s) == 0:
        #         s = hex(p)
        #     elif i == 4 or i == 12:
        #         s = s + ',\n' + hex(p)
        #     else:
        #         s = s + ',' + hex(p)
        # print("=" * 20)
        # print(a, s)
        # for i in range(0, a):
        #     print(i, hex(ts_packet[i]))
        #     self.assertEqual(expected_ret[i], ts_packet[i])
