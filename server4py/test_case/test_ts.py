from unittest import TestCase
from app.container.ts import ts_pes_packets, ts_pat_packet, ts_pmt_packet
# from container import datas
from app.container import print_ts_packet
from app import Packet, Packet_Type_VIDEO, Packet_Type_AUDIO
import os
import time
from app.codec.h264 import NALU_AUD_PACKET, NaluType, FrameType
from app.data_type_ext import int32, uint64, uint32
import math
from app.codec import h264
from app.container import ts


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
        ts_packets_size, ts_packets = ts_pes_packets(es_buffer, is_video, is_keyframe, 0, 0)

        for i in range(0, len(ts_packets)):
            p = ts_packets[i]
            print("=" * 20)
            print('index', i)
            print_ts_packet(p)

    def test_video_pes_packet(self):
        fs = h264.parse_from_file('v_datas1.txt')

        print("=" * 20)
        print('split elematry stream frame size  %d' % len(fs))
        path = '001.ts'
        # with open(path, 'w') as f:
        #     f.write('')
        ts.write_to_file(path, fs)
