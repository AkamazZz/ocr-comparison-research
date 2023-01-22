df = pd.DataFrame(dict(
    group = ["A", "B", "C", "D", "E"],
    value = [14, 12, 8, 10, 16]))

fig = px.bar(df, x = 'group', y = 'value')

fig.show()