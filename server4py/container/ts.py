'''
    [MPEG-TS 格式解析](https://blog.csdn.net/Kayson12345/article/details/81266587)
    [MPEG2-TS基础](https://blog.csdn.net/rootusers/article/details/42772657)
    [MPEG-TS基础2](https://blog.csdn.net/rootusers/article/details/42970859)

[MPEG transport stream](https://en.wikipedia.org/wiki/MPEG_transport_stream)
[Program-specific information(https://en.wikipedia.org/wiki/Program-specific_information)
[Packetized elementary stream](https://en.wikipedia.org/wiki/Packetized_elementary_stream#:~:text=PES%20packet%20header,-Name&text=Specifies%20the%20number%20of%20bytes,Optional%20PES%20header)
[HLS协议及TS封装](https://www.jianshu.com/p/d6311f03b81f)

PAT packet                       PMT  packet              PES packet
program_number=5            
program_map_PID=10   ---->  TS header pid=10
                            stream_type=0x0f audio
                            elementary_PID=20  ---->  TS header pid=20
                            stream_type=0x1b video
                            elementary_PID=22 ---->   TS header pid=22

program_number=6
program_map_PID=11  ---->  TS header pid=11
                            ....

program_number=7    
program_map_PID=12  ---->  ...
'''

from util.data_type import uint32, byte

__crcTable = [
    0x00000000, 0x04c11db7, 0x09823b6e, 0x0d4326d9,
    0x130476dc, 0x17c56b6b, 0x1a864db2, 0x1e475005,
    0x2608edb8, 0x22c9f00f, 0x2f8ad6d6, 0x2b4bcb61,
    0x350c9b64, 0x31cd86d3, 0x3c8ea00a, 0x384fbdbd,
    0x4c11db70, 0x48d0c6c7, 0x4593e01e, 0x4152fda9,
    0x5f15adac, 0x5bd4b01b, 0x569796c2, 0x52568b75,
    0x6a1936c8, 0x6ed82b7f, 0x639b0da6, 0x675a1011,
    0x791d4014, 0x7ddc5da3, 0x709f7b7a, 0x745e66cd,
    0x9823b6e0, 0x9ce2ab57, 0x91a18d8e, 0x95609039,
    0x8b27c03c, 0x8fe6dd8b, 0x82a5fb52, 0x8664e6e5,
    0xbe2b5b58, 0xbaea46ef, 0xb7a96036, 0xb3687d81,
    0xad2f2d84, 0xa9ee3033, 0xa4ad16ea, 0xa06c0b5d,
    0xd4326d90, 0xd0f37027, 0xddb056fe, 0xd9714b49,
    0xc7361b4c, 0xc3f706fb, 0xceb42022, 0xca753d95,
    0xf23a8028, 0xf6fb9d9f, 0xfbb8bb46, 0xff79a6f1,
    0xe13ef6f4, 0xe5ffeb43, 0xe8bccd9a, 0xec7dd02d,
    0x34867077, 0x30476dc0, 0x3d044b19, 0x39c556ae,
    0x278206ab, 0x23431b1c, 0x2e003dc5, 0x2ac12072,
    0x128e9dcf, 0x164f8078, 0x1b0ca6a1, 0x1fcdbb16,
    0x018aeb13, 0x054bf6a4, 0x0808d07d, 0x0cc9cdca,
    0x7897ab07, 0x7c56b6b0, 0x71159069, 0x75d48dde,
    0x6b93dddb, 0x6f52c06c, 0x6211e6b5, 0x66d0fb02,
    0x5e9f46bf, 0x5a5e5b08, 0x571d7dd1, 0x53dc6066,
    0x4d9b3063, 0x495a2dd4, 0x44190b0d, 0x40d816ba,
    0xaca5c697, 0xa864db20, 0xa527fdf9, 0xa1e6e04e,
    0xbfa1b04b, 0xbb60adfc, 0xb6238b25, 0xb2e29692,
    0x8aad2b2f, 0x8e6c3698, 0x832f1041, 0x87ee0df6,
    0x99a95df3, 0x9d684044, 0x902b669d, 0x94ea7b2a,
    0xe0b41de7, 0xe4750050, 0xe9362689, 0xedf73b3e,
    0xf3b06b3b, 0xf771768c, 0xfa325055, 0xfef34de2,
    0xc6bcf05f, 0xc27dede8, 0xcf3ecb31, 0xcbffd686,
    0xd5b88683, 0xd1799b34, 0xdc3abded, 0xd8fba05a,
    0x690ce0ee, 0x6dcdfd59, 0x608edb80, 0x644fc637,
    0x7a089632, 0x7ec98b85, 0x738aad5c, 0x774bb0eb,
    0x4f040d56, 0x4bc510e1, 0x46863638, 0x42472b8f,
    0x5c007b8a, 0x58c1663d, 0x558240e4, 0x51435d53,
    0x251d3b9e, 0x21dc2629, 0x2c9f00f0, 0x285e1d47,
    0x36194d42, 0x32d850f5, 0x3f9b762c, 0x3b5a6b9b,
    0x0315d626, 0x07d4cb91, 0x0a97ed48, 0x0e56f0ff,
    0x1011a0fa, 0x14d0bd4d, 0x19939b94, 0x1d528623,
    0xf12f560e, 0xf5ee4bb9, 0xf8ad6d60, 0xfc6c70d7,
    0xe22b20d2, 0xe6ea3d65, 0xeba91bbc, 0xef68060b,
    0xd727bbb6, 0xd3e6a601, 0xdea580d8, 0xda649d6f,
    0xc423cd6a, 0xc0e2d0dd, 0xcda1f604, 0xc960ebb3,
    0xbd3e8d7e, 0xb9ff90c9, 0xb4bcb610, 0xb07daba7,
    0xae3afba2, 0xaafbe615, 0xa7b8c0cc, 0xa379dd7b,
    0x9b3660c6, 0x9ff77d71, 0x92b45ba8, 0x9675461f,
    0x8832161a, 0x8cf30bad, 0x81b02d74, 0x857130c3,
    0x5d8a9099, 0x594b8d2e, 0x5408abf7, 0x50c9b640,
    0x4e8ee645, 0x4a4ffbf2, 0x470cdd2b, 0x43cdc09c,
    0x7b827d21, 0x7f436096, 0x7200464f, 0x76c15bf8,
    0x68860bfd, 0x6c47164a, 0x61043093, 0x65c52d24,
    0x119b4be9, 0x155a565e, 0x18197087, 0x1cd86d30,
    0x029f3d35, 0x065e2082, 0x0b1d065b, 0x0fdc1bec,
    0x3793a651, 0x3352bbe6, 0x3e119d3f, 0x3ad08088,
    0x2497d08d, 0x2056cd3a, 0x2d15ebe3, 0x29d4f654,
    0xc5a92679, 0xc1683bce, 0xcc2b1d17, 0xc8ea00a0,
    0xd6ad50a5, 0xd26c4d12, 0xdf2f6bcb, 0xdbee767c,
    0xe3a1cbc1, 0xe760d676, 0xea23f0af, 0xeee2ed18,
    0xf0a5bd1d, 0xf464a0aa, 0xf9278673, 0xfde69bc4,
    0x89b8fd09, 0x8d79e0be, 0x803ac667, 0x84fbdbd0,
    0x9abc8bd5, 0x9e7d9662, 0x933eb0bb, 0x97ffad0c,
    0xafb010b1, 0xab710d06, 0xa6322bdf, 0xa2f33668,
    0xbcb4666d, 0xb8757bda, 0xb5365d03, 0xb1f740b4
]


def __genCrc32(value):
    crc32 = uint32(0xffffffff)
    for i in range(0, len(value)):
        j = ((crc32 >> 24) ^ uint32(value[i])) & 0xFF
        crc32 = uint32(uint32(crc32 << 8) ^ __crcTable[j])
        # print(i,crc32)
    return crc32


__TS_PACKET_SIZE = 188
__TS_PACKET_HEADER_SIZE = 4
__TS_PACKET_PAYLOAD_SIZE = 184
__H264_DEFAULT_HZ = 90
__patCc = 0
__pmtCc = 0
__videoCc = 0
__audioCc = 0
__VIDEO_PID = 0x100
__AUDIO_PID = 0x101
__PAT_PID = 0x000
__VIDEO_SID = 0xe0
__AUDIO_SID = 0xc0


def copy(src: bytes, dest: bytearray, offset: int = 0):
    src_size = len(src)
    dest_size = len(dest)
    if src_size > dest_size:
        raise BaseException("dest size must be greater than src size")
    for i in range(0, src_size):
        if offset + i >= dest_size:
            break
        dest[offset + i] = src[i]


def pmt_packet(has_video: bool) -> bytes:
    '''

    :param has_video:
    :return:
    '''
    ts_header = bytearray([0x47,
                           # 0x50,0x01:transport_error_indicator=0 payload_unit_start_indicator=1
                           # transport_priority=1(高优先级) pid=4097
                           0x50, 0x01,
                           # 0x10:transport_scrambling_control==00(未加密) adaptation_field_control=01(无自适应域)
                           # continuity_counter=0000
                           0x10,
                           # payload_unit_start_indicator=1 会添加一个0x00表示负载起始
                           0x00])
    global __pmtCc
    if __pmtCc > 0xf:
        __pmtCc = 0
    ts_header[3] |= __pmtCc & 0x0f
    __pmtCc = __pmtCc + 1
    pmt_header = bytearray([0x02,
                            # 0xb0，0xff：section_syntax_indicator=1(固定) zero=0(固定) reserved=11(固定)
                            # section_length=11111111(255)
                            0xb0, 0xff,
                            # 0x00,0x01:program_number=1 频道号码，表示当前的PMT关联到的频道，取值0x0001
                            0x00, 0x01,
                            0xc1, 0x00, 0x00,
                            # 0xe1，0x00：reserved=111(固定) PCR_PID=256(10进制) PCR(节目参考时钟)所在TS分组的PID，指定为视频PID
                            0xe1, 0x00,
                            # 0xf0,0x00:reserved=1111(固定) program_info_length=0 节目描述信息，指定为0x000表示没有
                            0xf0, 0x00])
    if not has_video:
        pmt_header[9] = 0x01  # PCR_PID 0xe1,0x01
        prog_info = bytearray([0x0f, 0xe1, 0x01, 0xf0, 0x00])
    else:
        prog_info = bytearray([
            # h264 or h265 *
            # 0x1b:stream_type:h264
            # 0xe1, 0x00： reserved=111(固定） elementary_PID=256
            0x1b, 0xe1, 0x00, 0xf0, 0x00,
            # mp3 or aac
            # 0x0f:stream_type:aac
            # 0xe1, 0x01： elementary_PID = 257
            0x0f, 0xe1, 0x01, 0xf0, 0x00,
        ])
    pmt_header[2] = len(prog_info) + 9 + 4  # section_length：表示从下一个字段开始到CRC32(含)之间有用的字节数

    pmt = bytearray([0xff for i in range(0, __TS_PACKET_SIZE)])
    ts_header_size = len(ts_header)
    pmt_header_size = len(pmt_header)
    prog_info_size = len(prog_info)

    copy(ts_header, pmt)
    copy(pmt_header, pmt, ts_header_size)
    copy(prog_info, pmt, ts_header_size + pmt_header_size)

    crc32Value = __genCrc32(pmt[ts_header_size:ts_header_size + pmt_header_size + prog_info_size])
    for i in range(0, 4):
        bytes_size = 8 * (3 - i)
        ret = byte(crc32Value >> bytes_size)
        pmt[i + ts_header_size + pmt_header_size + prog_info_size] = ret
    # print('patCc:', __patCc, len(pmt))
    return pmt


def pat_packet() -> bytes:
    ts_header = bytearray([0x47,
                           # 0x40,0x00:transport_error_indicator=0 payload_unit_start_indicator=1
                           # transport_priority=0 pid=0(PAT表的PID值固定为0)
                           0x40, 0x00,
                           # 0x10:transport_scrambling_control==00(未加密) adaptation_field_control=01(无自适应域)
                           # continuity_counter=0000
                           0x10,
                           # payload_unit_start_indicator=1 会添加一个0x00表示负载起始
                           0x00])

    pat_header = bytearray([0x00,
                            # 0xb0，0x0d：section_syntax_indicator=1(固定) zero=0(固定) reserved=11(固定)
                            # section_length=1101(13)
                            0xb0, 0x0d,
                            # 0x00, 0x01 ：transport_stream_id 传输流ID，固定为0x0001
                            0x00, 0x01,
                            0xc1, 0x00, 0x00,
                            # 0x00,0x01:program_number=1 节目号为0x0000时表示这是NIT，节目号为0x0001时,表示这是PMT
                            0x00, 0x01,
                            # 0xf0,0x01:reserved=111(固定) PID =4097(10进制) 节目号对应内容的PID值
                            0xf0, 0x01])
    global __patCc
    if __patCc > 0xf:
        __patCc = 0
    ts_header[3] |= __patCc & 0x0f
    __patCc = __patCc + 1

    pat = bytearray([0xff for i in range(0, __TS_PACKET_SIZE)])
    ts_header_size = len(ts_header)
    pat_header_size = len(pat_header)
    copy(ts_header, pat)
    copy(pat_header, pat, ts_header_size)
    # for i in range(0, ts_header_size):
    #     pat[i] = ts_header[i]
    # for i in range(0, pat_header_size):
    #     pat[ts_header_size + i] = pat_header[i]
    crc32Value = __genCrc32(pat_header)
    for i in range(0, 4):
        bytes_size = 8 * (3 - i)
        ret = byte(crc32Value >> bytes_size)
        pat[i + pat_header_size + ts_header_size] = ret
    # print('patCc:', __patCc, len(pat))
    return pat


def adaptaionbuf_init(src, occupy_bytes, remainBytes):
    src[occupy_bytes] = remainBytes - 1
    if remainBytes > 1:
        src[1 + occupy_bytes] = 0x00  # payload_unit_start_indicator=1 会添加一个0x00表示负载起始
        for i in range(2 + occupy_bytes, len(src)):
            src[i] = 0xff


def write_pts_or_dts(buffer, value, flag):
    start = len(buffer)
    if value > 0x1ffffffff:
        value -= 0x1ffffffff
    n = uint32(flag << 4) | ((uint32(value >> 30) & 0x07) << 1) | 1
    buffer.insert(start, byte(n))
    n = ((uint32(value >> 15) & 0x7fff) << 1) | 1
    buffer.insert(start + 1, byte(n >> 8))
    buffer.insert(start + 2, byte(n))
    n = (uint32(value & 0x7fff) << 1) | 1
    buffer.insert(start + 3, byte(n >> 8))
    buffer.insert(start + 4, byte(n))


def gen_pes_header(payload_size: int, is_video, pts, dts):
    pes_header = bytearray([0x00, 0x00, 0x01])
    pes_header.insert(3, __AUDIO_SID if not is_video else __VIDEO_SID)
    pts_size = 5  # pts 5 bytes
    dts_size = 5
    remain_header_size = pts_size
    flag = 0x80  # 0x80表示只含有pt
    if is_video and pts != dts:
        flag |= 0x40  # 取值0xc0表示含有pts和dts
        remain_header_size = pts_size + dts_size

    remain_packet_size = payload_size + remain_header_size + 3
    if remain_packet_size > 0xffff:
        remain_packet_size = 0
    pes_header.insert(4, byte(remain_packet_size >> 8))
    pes_header.insert(5, byte(remain_packet_size))
    pes_header.insert(6, 0x80)
    pes_header.insert(7, flag)
    pes_header.insert(8, remain_header_size)
    # pts and dts
    write_pts_or_dts(pes_header, pts, flag >> 6)
    if is_video and pts != dts:
        write_pts_or_dts(pes_header, dts, 1)
    return len(pes_header), pes_header


def pes_packet(buffer: bytes, is_video, is_keyframe, pts, dts) -> (int, bytes):
    def __print_ts_packet(ts_packet):
        s = ''
        adaptation_field_control = 0x01
        adaptation_field_length = 0
        payload_unit_start_indicator = 0
        for jj in range(0, __TS_PACKET_SIZE):
            p = ts_packet[jj]
            if jj == 1:
                payload_unit_start_indicator = p >> 6 & 0b01
                print("payload_unit_start_indicator", bin(payload_unit_start_indicator))
            elif jj == 3:
                adaptation_field_control = (p >> 4) & 0b0011
                print('adaptation_field_control', bin(adaptation_field_control))
            if jj == 4 and adaptation_field_control & 0b10 == 0b10:
                adaptation_field_length = p
                print('adaptation_field_length', adaptation_field_length)

            if len(s) == 0:
                s = hex(p)
            elif jj == 4:
                s = s + ',\n' + hex(p)
            elif adaptation_field_control & 0b10 == 0b10 and adaptation_field_length + 4 == jj:
                s = s + ',\n' + hex(p)
            elif payload_unit_start_indicator == 1 and jj == adaptation_field_length + 5:
                s = s + ',\n\u001B[31mpes header:\u001B[0m' + hex(p)
            elif payload_unit_start_indicator == 1 and jj == adaptation_field_length + 5 + 19:
                s = s + ',\n\u001B[31mpes payload:\u001B[0m' + hex(p)
            else:
                s = s + ',' + hex(p)

        print(s)


    is_first_packet = True
    pes_payload_size = len(buffer)  # es size == pes_payload_size
    pes_header_size, pes_header = gen_pes_header(pes_payload_size, is_video, pts, dts)
    pes_packet_size = pes_header_size + pes_payload_size
    print('pes_packet_size', pes_packet_size)
    i = 0
    # data_block_size = 0
    # for loop split one pes(one frame) into ts blocks
    while i < pes_payload_size:
        ts_packet = bytearray([0xff for i in range(0, __TS_PACKET_SIZE)])
        print("=" * 20)
        print('index', i)
        pid = __AUDIO_PID
        if is_video:
            pid = __VIDEO_PID
        # ts header
        ts_packet[0] = 0x47  # sync byte
        ts_packet[1] = byte(pid >> 8)  # pid high 5 bits
        if is_first_packet:
            # unit start indicator 负载单元起始标示符，一个完整的数据包开始时标记为1
            ts_packet[1] = 0x40 | ts_packet[1]
        ts_packet[2] = byte(pid)  # pid low 8 bits
        global __videoCc, __audioCc
        if is_video:
            __videoCc = __videoCc + 1
            if __videoCc > 0xf:
                __videoCc = 0
            ts_packet[3] = 0x10 | __videoCc & 0x0f
        else:
            __audioCc = __audioCc + 1
            if __audioCc > 0xf:
                __audioCc = 0
            ts_packet[3] = 0x10 | __audioCc & 0x0f
        ts_packet_index = 4
        adaptation_field_size = 0

        # adaptation_field
        if is_first_packet and is_video and is_keyframe:
            # first packet,关键帧需要加pcr
            ts_packet[3] |= 0x20  # adaptation_field_control:‘10’为仅含自适应域，无有效负载
            ts_packet[4] = 7
            ts_packet[5] = 0x50
            pcr = dts
            ts_packet[6] = byte(pcr >> 25)
            ts_packet[7] = byte((pcr >> 17) & 0xff)
            ts_packet[8] = byte((pcr >> 9) & 0xff)
            ts_packet[9] = byte((pcr >> 1) & 0xff)
            ts_packet[10] = byte(((pcr & 0x1) << 7) | 0x7e)
            ts_packet[11] = 0x00  # payload_unit_start_indicator=1 会添加一个0x00表示负载起始
            ts_packet_index = 12
            adaptation_field_size = 8

        should_fill_0xff_size = __TS_PACKET_SIZE - (ts_packet_index + pes_packet_size)
        # fill 0xff
        if should_fill_0xff_size > 0:
            ts_packet[3] |= 0x20  # adaptation_field_control:‘10’为仅含自适应域，无有效负载
            # adaptation field
            ts_packet[ts_packet_index] = byte(should_fill_0xff_size - 1)
            if should_fill_0xff_size != 1:
                ts_packet[ts_packet_index + 1] = 0x00
            ts_packet_index += should_fill_0xff_size
        print("ts size:%d\tadaptation_field_size:%d\tfill 0xff size:%d\tpes_header_size:%d " % (__TS_PACKET_HEADER_SIZE,
                                                                                                adaptation_field_size,
                                                                                                should_fill_0xff_size,
                                                                                                pes_header_size))
        print('continuity_counter %d pid 0x%x' % (ts_packet[3] & 0x0f,
                                                  ((ts_packet[1] & 0b00011111) << 8) | ts_packet[2]
                                                  ))
        # pes header 放在第一个包中
        if is_first_packet and ts_packet_index < __TS_PACKET_SIZE and pes_header_size > 0:
            copy(pes_header, ts_packet, ts_packet_index)
            ts_packet_index += pes_header_size
            pes_packet_size -= pes_header_size
        print("ts_packet_index", ts_packet_index)
        if ts_packet_index < __TS_PACKET_SIZE:
            data_block_size = __TS_PACKET_SIZE - ts_packet_index
            copy(buffer[i:i + data_block_size], ts_packet, ts_packet_index)
            pes_packet_size -= data_block_size
            i += data_block_size

        __print_ts_packet(ts_packet)
        is_first_packet = False

    return len(ts_packet), ts_packet


if __name__ == "__main__":
    patHeader = bytearray([0x00, 0xb0, 0x0d, 0x00, 0x01, 0xc1, 0x00, 0x00, 0x00, 0x01, 0xf0, 0x01])
    # print(genCrc32(patHeader))

    # for i in range(0, 4):
    #     ps = pat()
    #     s = ''
    #     for i in range(0, __TS_PACKET_SIZE):
    #         p = ps[i]
    #         if len(s) == 0:
    #             s = hex(p)
    #         elif i == 5 or i == 17 or i == 21:
    #             s = s + ',\n' + hex(p)
    #         else:
    #             s = s + ',' + hex(p)
    #
    #     print(s)
    # has_video = True
    # for i in range(0, 10):
    #     ps = pmt_packet(has_video)
    #     s = ''
    #     for i in range(0, __TS_PACKET_SIZE):
    #         p = ps[i]
    #         line = (27 if has_video else 22)
    #         if len(s) == 0:
    #             s = hex(p)
    #         elif i == 5 or i == 17 or i == line or i == (line + 4):
    #             s = s + ',\n' + hex(p)
    #         else:
    #             s = s + ',' + hex(p)
    #
    #     print(s)
    pass