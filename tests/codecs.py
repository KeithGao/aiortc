from unittest import TestCase

from aiortc import AudioFrame, VideoFrame
from aiortc.codecs import depayload, get_decoder, get_encoder

AUDIO_PTIME = 0.020


class CodecTestCase(TestCase):
    def roundtrip_audio(self, codec, output_channels, output_sample_rate):
        """
        Round-trip an AudioFrame through encoder then decoder.
        """
        encoder = get_encoder(codec)
        decoder = get_decoder(codec)

        # encode
        frame = AudioFrame(
            channels=1,
            data=b'\x00\x00' * 160,
            sample_rate=8000)
        self.assertEqual(len(frame.data), 320)
        data = encoder.encode(frame)

        # decode
        frames = decoder.decode(data)
        self.assertEqual(len(frames), 1)
        self.assertEqual(len(frames[0].data),
                         output_sample_rate * AUDIO_PTIME * output_channels * 2)
        self.assertEqual(frames[0].channels, output_channels)
        self.assertEqual(frames[0].sample_rate, output_sample_rate)
        self.assertEqual(frames[0].sample_width, 2)

    def roundtrip_video(self, codec, width, height):
        """
        Round-trip a VideoFrame through encoder then decoder.
        """
        encoder = get_encoder(codec)
        decoder = get_decoder(codec)

        # encode
        frame = VideoFrame(width=width, height=height)
        packages = encoder.encode(frame)

        # depacketize
        data = b''
        for package in packages:
            data += depayload(codec, package)

        # decode
        frames = decoder.decode(data)
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].width, width)
        self.assertEqual(frames[0].height, height)
