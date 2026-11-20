"""PES2UG24AM014: statement coverage of the unchanged assigned module."""
import pytest
from cloud_storage_tier import process_storage_tenants as bill
from cloud_storage_tier import monitor_replication_latency as monitor


def tenant(tier='hot', buckets=None, vault=False):
    return {'account_active': True, 'tier': tier,
            'buckets': [] if buckets is None else buckets,
            'has_backup_vault': vault}


def test_invalid_tenant_container():
    with pytest.raises(ValueError, match='Invalid tenants'):
        bill(None, 10)


def test_inactive_tenant_is_skipped():
    assert bill([{'account_active': False}], 10) == {
        'total_billed': 0.0, 'status': 'ZERO_USAGE'}


@pytest.mark.parametrize('tier,expected', [('hot', 2.5), ('cool', 1.5),
                                          ('archive', 0.5)])
def test_each_storage_tier(tier, expected):
    assert bill([tenant(tier, [{'size_gb': 100}])], 10) == {
        'total_billed': expected, 'status': 'BILLED'}


def test_volume_discount_egress_and_support_fee():
    # 600 * .025 * .9 + (150 - 100) * .08 + 10 = 27.5
    assert bill([tenant(buckets=[{'size_gb': 600, 'egress_gb': 150}],
                        vault=True)], 10) == {
        'total_billed': 27.5, 'status': 'BILLED'}


def test_corrupted_hot_bucket_still_pays_egress():
    # This documents the starter's policy: no storage, but billed egress.
    assert bill([tenant(buckets=[{'size_gb': 100, 'corrupted': True,
                                 'egress_gb': 150}])], 10) == {
        'total_billed': 4.0, 'status': 'BILLED'}


def test_corrupted_archive_resets_charge_and_breaks():
    buckets = [{'size_gb': 100}, {'size_gb': 200, 'corrupted': True},
               {'size_gb': 10000, 'egress_gb': 10000}]
    assert bill([tenant('archive', buckets)], 10) == {
        'total_billed': 0.0, 'status': 'ZERO_USAGE'}


def test_invalid_sizes_and_unknown_tier_trigger_audit():
    tenants = [tenant(buckets=[{'size_gb': 0}] * 4), tenant('unknown')]
    assert bill(tenants, 10) == {
        'total_billed': 0.0, 'status': 'AUDIT_FLAGGED'}


def test_latency_without_data():
    assert monitor([]) == 'NO_DATA'


def test_latency_reset_then_alert():
    assert monitor([[201, 200, 201, 202]]) == 'SYNC_LAG_ALERT'


def test_latency_fully_synced():
    assert monitor([[10, 100], [], [200]]) == 'SYNCED'
