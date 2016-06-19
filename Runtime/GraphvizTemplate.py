__author__ = 'Tihamer Levendovszky'

template = """
digraph G {
subgraph cluster0 {
node [style=filled,color=white];
style=filled;
color=lightgrey;
@NODELIST@;
label = "Nodes";
}
subgraph cluster1 {
node [style=filled];
@COMPONENTLIST@;
label = "Components";
color=blue
}
@CONNECTIONLIST@;

}"""