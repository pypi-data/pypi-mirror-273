import os
import rx784

PORT = os.environ['PORT']


def test_smoke():
    device = rx784.Device()
    assert device.open(PORT)                             == rx784.Status.SUCCESS
    assert device.key_down(rx784.VirtualKeyCode.OS_LEFT) == rx784.Status.SUCCESS
    assert device.key_up(rx784.VirtualKeyCode.OS_LEFT)   == rx784.Status.SUCCESS
