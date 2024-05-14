# `relationalai.std.graphs.Compute.avg_clustering_coefficient()`

```python
relationalai.std.graphs.Compute.avg_clustering_coefficient(node: Producer) -> Expression
```

An [Expression](docs/api_reference/python/Expression.md) object that produces
the average of all local clustering coefficents of nodes in the graph.
Only undirected graphs are supported.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | No |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Parameters

None.

## Returns

An [Expression](docs/api_reference/python/Expression.md) object that produces `float` values.

## Example

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with Person and Friendship types.
model = rai.Model("socialNetwork")
Person = model.Type("Person")
Friendship = model.Type("Friendship")

# Add some people and friendships to the model.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    charlie = Person.add(name="Charlie")
    diana = Person.add(name="Diana")
    Friendship.add(person1=alice, person2=bob)
    Friendship.add(person1=alice, person2=charlie)
    Friendship.add(person1=alice, person2=diana)
    Friendship.add(person1=bob, person2=charlie)
    
# Create an undirected graph with nodes from the Person type and edges from the Friendship type.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
with model.rule():
    friendship = Friendship()
    graph.Edge.add(friendship.person1, friendship.person2)

# Compute the average clustering coefficient of the graph.
with model.query() as select:
    clustering_coeff = graph.compute.avg_clustering_coefficient()
    response = select(alias(clustering_coeff, "clustering_coefficient"))

print(response.results)
# Output:
#    clustering_coefficient
# 0                0.583333
```

## See Also

[`local_clustering_coefficient()`](./local_lustering_coefficient.md)
