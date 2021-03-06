from plenum.test.test_node import ensureElectionsDone

nodeCount = 7


def test_select_primary_after_removed_backup(txnPoolNodeSet,
                                             looper,
                                             sdk_pool_handle,
                                             sdk_wallet_client):
    """
    Check correct order of primaries on backup replicas
    """

    node = txnPoolNodeSet[0]
    start_replicas_count = node.replicas.num_replicas
    instance_id = start_replicas_count - 1
    node.replicas.remove_replica(instance_id)
    for node in txnPoolNodeSet:
        node.view_changer.on_master_degradation()
    ensureElectionsDone(looper=looper, nodes=txnPoolNodeSet)
    for n in txnPoolNodeSet:
        assert n.requiredNumberOfInstances == n.replicas.num_replicas
        for inst_id in range(n.requiredNumberOfInstances):
            assert n.replicas[inst_id].primaryName == \
                   txnPoolNodeSet[inst_id + 1].name + ":" + str(inst_id)
