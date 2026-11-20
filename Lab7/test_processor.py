"""PES2UG24AM014: property-based fuzzing and replayable regression cases."""
import math
import re
import pytest
from hypothesis import given, settings, strategies as st
from processor import (parse_storage_quota, compute_compression_ratio,
                       lookup_bandwidth_tier_rate)

# Deterministic generated cases; no user-profile database writes required.
settings.register_profile('lab', max_examples=300, derandomize=True,
                          database=None, deadline=None)
settings.load_profile('lab')
inputs = st.one_of(st.text(max_size=350), st.none(), st.integers(),
                   st.floats(allow_nan=True, allow_infinity=True),
                   st.binary(max_size=30), st.lists(st.integers(), max_size=5),
                   st.dictionaries(st.text(max_size=5), st.integers(), max_size=3))


@given(inputs)
def test_parse_storage_quota_no_crash(value):
    try:
        result = parse_storage_quota(value)
    except Exception as exc:
        pytest.fail(f'quota crashed for {value!r}: {type(exc).__name__}: {exc}')
    valid = (isinstance(value, str) and len(value) <= 256
             and re.fullmatch(r'[0-9]+(?:MB|GB|TB)', value.strip().upper()))
    if valid:
        cleaned = value.strip().upper()
        expected = int(cleaned[:-2]) * {'MB': .001, 'GB': 1, 'TB': 1000}[cleaned[-2:]]
        assert result == f'Quota: {expected:.2f} GB'
    else:
        assert result is None


@given(inputs)
def test_compute_compression_ratio_safe(value):
    try:
        result = compute_compression_ratio(value)
    except Exception as exc:
        pytest.fail(f'ratio crashed for {value!r}: {type(exc).__name__}: {exc}')
    assert result is None or (isinstance(result, (int, float))
                              and math.isfinite(result) and result >= 0)


@given(inputs)
def test_lookup_bandwidth_tier_rate_safe(value):
    try:
        result = lookup_bandwidth_tier_rate(value)
    except Exception as exc:
        pytest.fail(f'tier crashed for {value!r}: {type(exc).__name__}: {exc}')
    aliases = {'HOT': .08, 'HOT_TIER': .08, 'COL': .05, 'COOL': .05,
               'COLD': .05, 'COOL_TIER': .05, 'COLD_TIER': .05,
               'ARC': .02, 'ARCHIVE': .02, 'ARCHIVE_TIER': .02}
    expected = (aliases.get(value.strip().upper())
                if isinstance(value, str) and len(value) <= 256 else None)
    assert result == expected


@given(st.integers(min_value=0, max_value=10**12),
       st.sampled_from(['MB', 'GB', 'TB']), st.booleans())
def test_valid_quota_conversion(amount, unit, lower):
    text = f'{amount}{unit}'
    text = '  ' + (text.lower() if lower else text) + '  '
    expected = amount * {'MB': .001, 'GB': 1, 'TB': 1000}[unit]
    assert parse_storage_quota(text) == f'Quota: {expected:.2f} GB'


@given(st.integers(min_value=0, max_value=10**12),
       st.integers(min_value=1, max_value=10**12))
def test_valid_ratio_math(raw, compressed):
    assert compute_compression_ratio(f'{raw}:{compressed}') == round(raw / compressed, 2)


@given(st.integers(min_value=0, max_value=10**12))
def test_zero_denominator_rejected(raw):
    assert compute_compression_ratio(f'{raw}:0') is None


@pytest.mark.parametrize('value', ['', None, '1XB', '-1GB', '1.5GB',
                                  '١GB', '9' * 300 + 'TB', b'2GB', True])
def test_quota_regressions(value):
    assert parse_storage_quota(value) is None


@pytest.mark.parametrize('value,expected', [('500MB', 'Quota: 0.50 GB'),
    ('20GB', 'Quota: 20.00 GB'), ('2TB', 'Quota: 2000.00 GB'),
    ('0MB', 'Quota: 0.00 GB'), (' 2tb ', 'Quota: 2000.00 GB')])
def test_quota_examples(value, expected):
    assert parse_storage_quota(value) == expected


@pytest.mark.parametrize('value', ['', None, ':', '1:0', '0:0', '1:-1', '-1:2',
    '1:2:3', 'nan:1', '1:nan', 'inf:1', '1:inf', '1e309:1',
    '1e308:1e-308', '1:1e-9999', '1:' + '0' * 300, [], True])
def test_ratio_regressions(value):
    assert compute_compression_ratio(value) is None


@pytest.mark.parametrize('value,expected', [('0:1', 0), ('1024:256', 4),
    ('1:3', .33), (' 12 : 4 ', 3), ('1e3:2e2', 5)])
def test_ratio_examples(value, expected):
    assert compute_compression_ratio(value) == expected


@pytest.mark.parametrize('value', ['', None, 'H', 'UNKNOWN', 'HOTDOG',
                                  'COLLISION', 'ARCHAIC', 'HOT' * 100, 4])
def test_tier_regressions(value):
    assert lookup_bandwidth_tier_rate(value) is None


@pytest.mark.parametrize('value,expected', [('HOT_TIER', .08), (' hot ', .08),
    ('COOL', .05), ('COLD', .05), ('ARCHIVE', .02), ('arc', .02)])
def test_tier_examples(value, expected):
    assert lookup_bandwidth_tier_rate(value) == expected
