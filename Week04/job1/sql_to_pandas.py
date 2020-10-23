import pandas as pd
import numpy as np


def create_data():
    table_data = pd.DataFrame({
        "id": pd.Series((x + 1 for x in range(100)), dtype="int32"),
        "age": pd.Series(np.random.randint(18, 40, 100, dtype="int32")),
    })
    return table_data


def create_table1():
    table_table1 = pd.DataFrame({
        "id": pd.Series(np.random.randint(1, 30, 100, dtype="int32")),
        "order_id": pd.Series(np.random.randint(10010, 10086, 100, dtype="int32")),
    })
    return table_table1


def create_table2():
    table_table2 = pd.DataFrame({
        "id": pd.Series(np.random.randint(20, 50, 100, dtype="int32")),
        "order_id": pd.Series(np.random.randint(10010, 10096, 100, dtype="int32")),
    })
    return table_table2


data = create_data()
table1 = create_table1()
table2 = create_table2()

# SELECT * FROM data;
print(data.to_numpy())

# SELECT * FROM data LIMIT 10;
print(data.head(10))

# SELECT id FROM data;
print(data["id"])

# SELECT COUNT(id) FROM data;
print(data["id"].count())

# SELECT * FROM data WHERE id<1000 AND age>30;
print(data[(data["id"] < 1000) & (data["age"] > 30)])
# 或者map进行筛选
print(data[(data["id"].map(lambda x: x < 1000)) & data["age"].map(lambda x: x > 30)])

# SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
print(table1.groupby(by=["id"]).agg({"order_id": [("order_id_count", "nunique")]}))

# SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
print(pd.merge(table1, table2, on="id", how="inner"))

# SELECT * FROM table1 UNION SELECT * FROM table2;
print(pd.concat([table1, table2], axis=0, ignore_index=True).drop_duplicates().reset_index())

# DELETE FROM table1 WHERE id=10;
print(table1.drop(table1[table1["id"]==10].index).reset_index())

# ALTER TABLE table1 DROP COLUMN column_name  (column_name=id);
print(table1.drop("id", axis=1))
