"""PES2UG24AM014: independent branch suite with inherited line cases."""
import pytest
# Reuse the line-stage scenarios and extend them with decision boundaries.
from CodeCoverageTest_PES2UG24AM014_application import *  # noqa: F403
from cloud_storage_tier import process_storage_tenants as bill
from cloud_storage_tier import monitor_replication_latency as monitor


def test_negative_fee_with_valid_list():
    with pytest.raises(ValueError):
        bill([], -0.01)


def test_empty_tenants_zero_fee():
    assert bill([], 0) == {'total_billed': 0.0, 'status': 'ZERO_USAGE'}


@pytest.mark.parametrize('size,expected', [(500, 12.5), (501, 11.27)])
def test_discount_boundary(size, expected):
    assert bill([tenant(buckets=[{'size_gb': size}])], 0)['total_billed'] == expected


@pytest.mark.parametrize('egress,expected', [(100, 2.5), (101, 2.58)])
def test_egress_boundary(egress, expected):
    assert bill([tenant(buckets=[{'size_gb': 100, 'egress_gb': egress}])], 0)['total_billed'] == expected


def test_four_flags_do_not_trigger_audit():
    assert bill([tenant(buckets=[{'size_gb': -1}] * 4)], 0) == {
        'total_billed': 0.0, 'status': 'ZERO_USAGE'}


def test_audit_status_preserves_other_tenant_charges():
    assert bill([tenant(buckets=[{}] * 5),
                 tenant('cool', [{'size_gb': 100}])], 0) == {
        'total_billed': 1.5, 'status': 'AUDIT_FLAGGED'}


def test_missing_fields_use_defaults():
    assert bill([{}, {'account_active': True, 'buckets': [{'size_gb': 100}]}], 0) == {
        'total_billed': 2.5, 'status': 'BILLED'}


def test_archive_break_preserves_support_fee():
    assert bill([tenant('archive', [{'size_gb': 5, 'corrupted': True}], True)], 10) == {
        'total_billed': 10.0, 'status': 'BILLED'}


@pytest.mark.parametrize('matrix,expected', [
    (None, 'NO_DATA'), ([[]], 'SYNCED'), ([[201]], 'SYNCED'),
    ([[201], [201]], 'SYNCED'), ([[201, 200, 201]], 'SYNCED'),
    ([[200, 201, 201], []], 'SYNC_LAG_ALERT'),
    ([[], [201, 201]], 'SYNC_LAG_ALERT'),
])
def test_latency_branch_boundaries(matrix, expected):
    assert monitor(matrix) == expected
