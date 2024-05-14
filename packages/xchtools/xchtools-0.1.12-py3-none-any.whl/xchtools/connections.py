# %%
import os
import pymysql
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import logging
import traceback
import pymysqlpool

pymysqlpool.logger.setLevel("DEBUG")


class XCHConnections:
    """

    init params:
        settings_dir: the directory to settings.toml/.env/.secret.toml
        project_name: optional.

    methods:
        sql2li(sql): return the result of sql in list of list format
        sql2df(sql): return theresult of sql in dataframe format


    """

    def __init__(self, settings_dir, project_name="XCHTOOLS"):
        self.project_name = project_name
        self.init_config(
            settings_dir=settings_dir, project_name=project_name
        )  # make self.settings available
        # self.conn, self.cursor = self._renew_connect_mysql()
        self.pool = self._create_pool()

    def init_config(self, settings_dir, project_name="XCHTOOLS"):
        # Usage: input settings file path， return the settings dictionary.
        import os
        from dynaconf import Dynaconf

        settings = Dynaconf(
            env=os.environ.get(f"ENV_FOR_{project_name}") or "development",
            envvar_prefix="XCHTOOLS",
            settings_files=[
                os.path.join(settings_dir, "settings.toml"),
                os.path.join(settings_dir, ".secrets.toml"),
            ],
            environments=True,
            load_dotenv=True,
            dotenv_path=os.path.join(settings_dir, ".env"),
        )
        self.settings = settings

    def _create_pool(self):
        if not self.settings.get("db"):
            raise ValueError(
                "settings is emmpty. please specify them in `settings.toml`"
            )
        cdp_params = self.settings.get("db").to_dict()
        return pymysqlpool.ConnectionPool(name="poo", **cdp_params)

    def get_pool_info(self):
        return f"avail/total conns:  {self.pool.available_num}/{self.pool.total_num}"

    def _execute_fetch(self, sql):
        con = self.pool.get_connection()
        cur = con.cursor()
        try:
            data = cur.execute(sql)
            data = cur.fetchall()
            return data
        finally:
            cur.close()
            con.close()

    def _execute_fetchmany(self, sql, limit=1):
        con = self.pool.get_connection()
        cur = con.cursor()
        try:
            data = cur.execute(sql)
            data = cur.fetchmany(limit)
            return data
        finally:
            cur.close()
            con.close()

    def _execute_fetch_with_head(self, sql):
        con = self.pool.get_connection()
        cur = con.cursor()
        cur.execute(sql)
        head = [a[0] for a in cur.description]
        data = cur.fetchall()
        if not data:
            return pd.DataFrame(columns=head)
        df = pd.DataFrame(data)
        df.columns = head
        cur.close()
        con.close()
        return df

    def sql2li(self, sql, limit=1000):
        if limit > 0:
            data = self._execute_fetchmany(sql, limit)
        else:
            data = self._execute_fetch(sql)
        return data

    def sql2df(self, sql) -> pd.DataFrame:
        data = self._execute_fetch_with_head(sql)
        return data

    def create_tables(self, sql_folder, database):
        conn, cursor = self._renew_connect_mysql()
        conn.select_db(database)
        p = Path(sql_folder)
        sqlfiles = list(p.rglob("*.sql"))
        for sqlfile in tqdm(sqlfiles):
            try:
                with open(sqlfile, "r", encoding="utf8") as f:
                    sql_list = f.read().split(";")[:-1]
                    for sql in sql_list:
                        sql = sql.strip() + ";"
                        cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"Load {sqlfile} failed.  {e}")
        cursor.close()
        conn.close()


# %%
if __name__ == "__main__":
    xc = XCHConnections(os.path.dirname(os.path.abspath(__file__)))
    config = xc.settings
    print(config.db)
    # %%
    xc.sql2df("show databases")
    # xc.sql2li_limit("show databases", 3)

    # %%
    for i in tqdm(range(12)):
        try:
            xc.sql2li("show tables in information_schema")
            xc.sql2li("show databases")
            xc.sql2df("show columns in fundresearch.fund_awards ")
            xc.sql2li("show ads")  # wrong sql
        except:
            pass
    # %%
    # xc.sql2li("show tables in fundresearch")
    # xc.sql2li("select * from fundresearch.fund_information")
    xc.sql2li("select * from information_schema.TABLES")
    # %%
    # 批量建表
    path = r"C:\Users\o0oii\Downloads\fundresearch_fundresearch_20231115205701\fundresearch\TABLE"
    xc.create_tables(path, "fundresearch")

    # %%
    xc.sql2df("show columns in fundresearch.fund_awards ")

    # %%
    xc.sql2df("show columns in fundresearch.fund_awards ")  # ["Field"].tolist()

    # %%
    # 测试性能
    import timeit

    sql = "show databases"
    print(timeit.timeit(lambda: xc.sql2li(sql), number=1000))

    # %%

    # %%
    # 测试链接关闭的情况
    import time

    # sql = "show columns in fund_qaqa.fund_awards"
    sql = "show databases"

    print(xc.sql2li(sql))
    time.sleep(0.5)

    xc.conn.close()
    print(xc.sql2li(sql))
    time.sleep(0.5)

    xc.cur.close()
    print(xc.sql2li(sql))
    time.sleep(0.5)

    xc.cur.close()
    xc.conn.close()
    print(xc.sql2li(sql))

    # %%
    sql = "select '1','2' where False"
    xc.sql2df(sql)

# %%
