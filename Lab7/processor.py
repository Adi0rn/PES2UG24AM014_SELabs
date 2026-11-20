"""Cloud storage input validation. SRN: PES2UG24AM014.

Valid inputs retain the assigned API. Invalid or non-finite inputs return None;
the CLI reports the validation failure and continues to the next operation.
"""
import math
import re

MAX_INPUT_LENGTH = 256
QUOTA_PATTERN = re.compile(r'([0-9]+)(MB|GB|TB)', re.ASCII)
TIER_RATES = {
    'HOT': 0.08, 'HOT_TIER': 0.08,
    'COL': 0.05, 'COOL': 0.05, 'COLD': 0.05,
    'COOL_TIER': 0.05, 'COLD_TIER': 0.05,
    'ARC': 0.02, 'ARCHIVE': 0.02, 'ARCHIVE_TIER': 0.02,
}


def _clean_text(value):
    """Bound work before stripping or parsing untrusted input."""
    if not isinstance(value, str) or len(value) > MAX_INPUT_LENGTH:
        return None
    return value.strip().upper()


def parse_storage_quota(quota_str):
    """Convert non-negative integer MB/GB/TB quotas to a formatted GB string."""
    cleaned = _clean_text(quota_str)
    if cleaned is None:
        return None
    match = QUOTA_PATTERN.fullmatch(cleaned)
    if match is None:
        return None
    value, unit = match.groups()
    # A 256-character bound keeps this conversion below float overflow.
    gb_total = int(value) * {'MB': 0.001, 'GB': 1.0, 'TB': 1000.0}[unit]
    return f'Quota: {gb_total:.2f} GB'


def compute_compression_ratio(size_metric_str):
    """Return finite raw/compressed ratio, requiring raw >= 0 and compressed > 0."""
    cleaned = _clean_text(size_metric_str)
    if cleaned is None or cleaned.count(':') != 1:
        return None
    raw_str, comp_str = cleaned.split(':')
    try:
        raw_bytes, comp_bytes = float(raw_str), float(comp_str)
    except ValueError:
        return None
    if (not math.isfinite(raw_bytes) or not math.isfinite(comp_bytes)
            or raw_bytes < 0 or comp_bytes <= 0):
        return None
    ratio = raw_bytes / comp_bytes
    if not math.isfinite(ratio):
        return None
    return round(ratio, 2)


def lookup_bandwidth_tier_rate(tier_descriptor):
    """Look up documented names/aliases; reject misleading prefix matches."""
    cleaned = _clean_text(tier_descriptor)
    if cleaned is None:
        return None
    return TIER_RATES.get(cleaned)


def main():
    """Run all three demonstrations without crashing on malformed input."""
    prompts = (
        ('parse_storage_quota', 'Enter quota (e.g. 500MB, 10GB, 2TB): ',
         parse_storage_quota, ''),
        ('compute_compression_ratio',
         'Enter raw:compressed bytes (e.g. 1024:256): ',
         compute_compression_ratio, 'Compression Ratio: '),
        ('lookup_bandwidth_tier_rate',
         'Enter tier descriptor (e.g. HOT_TIER, COLD, ARCHIVE): ',
         lookup_bandwidth_tier_rate, 'Rate per GB: $ '),
    )
    for name, prompt, operation, prefix in prompts:
        print(f'==== Running {name} ====')
        try:
            value = input(prompt)
        except EOFError:
            print('Input unavailable.')
            return
        result = operation(value)
        print('Invalid input.' if result is None else f'{prefix}{result}')


if __name__ == '__main__':
    main()
