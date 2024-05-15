from xz import open as xzopen

with xzopen(r"C:\Users\Dani\repos_git\shexer\test\t_files\compression\t_graph_1.ttl.xz") as in_stream:
    for a_line in in_stream:
        print(a_line)