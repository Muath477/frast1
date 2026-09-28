from app.intelligence.baseline import Baseline


def test_normal_z_small():
    b = Baseline(warmup=20)
    for _ in range(50):
        b.learn("e", "m", 10.0, anomalous=False)
    mean, z = b.score("e", "m", 10.5)
    assert abs(mean - 10) < 0.5
    assert abs(z) < 3


def test_spike_z_large():
    b = Baseline(warmup=20)
    for _ in range(50):
        b.learn("e", "m", 10.0, anomalous=False)
    _, z = b.score("e", "m", 90.0)
    assert z > 6


def test_anomalous_does_not_shift_mean():
    b = Baseline(warmup=20)
    for _ in range(50):
        b.learn("e", "m", 10.0, anomalous=False)
    mean_before, _ = b.score("e", "m", 10.0)
    for _ in range(30):
        b.learn("e", "m", 90.0, anomalous=True)
    mean_after, _ = b.score("e", "m", 10.0)
    assert abs(mean_after - mean_before) < 0.01
    assert abs(mean_after - 10) < 0.5
