import relationalai as rai

from relationalai import debugging
from relationalai.clients import config as cfg
from relationalai.std import aggregates

from relationalai.clients.snowflake import Snowflake

# derived from https://relationalai.atlassian.net/browse/RAI-22876
def test_heap_snapshots(engine_config: cfg.Config):
    use_multi_valued = True
    use_value_types = True
    with debugging.span("run", idx=0, use_multi_valued=use_multi_valued, use_value_types=use_value_types):
        model = rai.Model("HeapSnapshotsBenchmark", config=engine_config)
        model._config.set("compiler.use_multi_valued", use_multi_valued)
        model._config.set("compiler.use_value_types", use_value_types)

        sf = Snowflake(model)

        Node = model.Type("Node")
        ArrayEdge = model.Type("ArrayEdge")
        ObjectEdge = model.Type("ObjectEdge")
        Edge = model.Type("Edge")

        ArrayTableEntry = sf.PYREL_HEAP_SNAPSHOTS_BENCHMARK.PUBLIC.EMPTY__ARRAYS
        ObjectTableEntry = sf.PYREL_HEAP_SNAPSHOTS_BENCHMARK.PUBLIC.EMPTY__OBJECTS
        NodeTableEntry = sf.PYREL_HEAP_SNAPSHOTS_BENCHMARK.PUBLIC.EMPTY__NODES
        StringsTableEntry = sf.PYREL_HEAP_SNAPSHOTS_BENCHMARK.PUBLIC.EMPTY__STRINGS

        with model.query(tag="select_5") as select:
            out = select(5)
        print(out.results)

        with model.query(tag="count_strings") as select:
            s = StringsTableEntry()
            out = select(aggregates.count(s))
        print(out.results)

        with model.query(tag="count_string_values") as select:
            s = StringsTableEntry()
            out = select(aggregates.count(s.value))
        print(out.results)

        # Build the nodes using the string table to get string typename values
        with model.rule():
            n = NodeTableEntry()
            name = StringsTableEntry(id = n.type)
            Node.add(id=n.id, typename=name.value)

        # Build the edges using the string table to get string typename values
        with model.rule():
            o = ObjectTableEntry()
            label = StringsTableEntry(id = o.label)
            ObjectEdge.add(from_=o.from_, to=o.to_, label=label.value)
            Edge.add(from_=o.from_, to=o.to_)

        with model.rule():
            a = ArrayTableEntry()
            o = ObjectTableEntry()
            ArrayEdge.add(from_=o.from_, to=o.to_, index=a.index)
            Edge.add(from_=o.from_, to=o.to_)

        with model.query(tag="count_object_edges") as select:
            out = select(aggregates.count(ObjectEdge()))
        print(out.results)
