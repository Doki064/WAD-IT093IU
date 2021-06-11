"""
Example:
    >>> from wms.gui._management import Management
    >>> management = Management()
    >>> management.show_search() # Show search section
    >>> management.show_add() # Show add section
    >>> management.show_remove() # Show remove section
"""

import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st


class Management:

    def __init__(self, connection):
        self.connection = connection
        self.current_option = ""
        self.tables = [
            table[0] for table in self.connection.cursor().execute(
                "SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        ]
        try:
            self.tables.remove("ImportDetail")
            self.tables.remove("TransactionDetail")
        except AttributeError as e:
            print(e)
        except ValueError:
            pass
        self.customer_columns = customer.columns_names(self.connection)
        self.shop_columns = shop.columns_names(self.connection)
        self.category_columns = item_category.columns_names(self.connection)
        self.item_columns = item.columns_names(self.connection)
        self.imports_columns = imports.columns_names(self.connection)
        self.transactions_columns = transactions.columns_names(self.connection)

    def show_search(self):
        with st.beta_container():
            self.current_option = st.selectbox("Select table to search: ", self.tables)
            col1, col2 = st.beta_columns(2)

            if self.current_option == "Customer":
                with col1:
                    st.info("""
                        Input name to search for customer in the database.
                        If there is no input, all entries be shown.\n
                        *Limit to 1000 rows.*
                    """)
                    choice = st.radio("Search by id/name: ", options=['id', 'name'])

                    if choice == "id":
                        customer_id = st.number_input(
                            "Input customer id: ",
                            step=1,
                            value=0,
                            min_value=0,
                            max_value=customer.max_id(self.connection) or 0)
                    elif choice == "name":
                        customer_name = st.text_input(
                            "Input customer name (* to search all): ", value="")

                    columns = st.multiselect("Select columns to show: ",
                                             self.customer_columns)

                if not columns:
                    columns = self.customer_columns

                if choice == "id":
                    data = customer.search_by_id(self.connection, customer_id, columns)
                elif choice == "name":
                    data = customer.search_by_name(self.connection, customer_name,
                                                   columns)

                df = pd.DataFrame.from_records(data, columns=columns)[:1000]

                with col2:
                    with st.beta_expander("Show customer with selected column(s)",
                                          expanded=True):
                        st.dataframe(df)

            elif self.current_option == "ItemCategory":
                with col1:
                    st.info("""
                        Input name to search for category in the database.
                        If there is no input, all entries be shown.\n
                        *Limit to 1000 rows.*
                    """)
                    choice = st.radio("Search by id/name: ", options=['id', 'name'])

                    if choice == "id":
                        category_id = st.number_input(
                            "Input category id: ",
                            step=1,
                            value=0,
                            min_value=0,
                            max_value=item_category.max_id(self.connection) or 0)
                    elif choice == "name":
                        category_name = st.text_input(
                            "Input category name (* to search all): ", value="")

                    columns = st.multiselect("Select columns to search: ",
                                             self.category_columns)

                if not columns:
                    columns = self.category_columns

                if choice == "id":
                    data = item_category.search_by_id(self.connection, category_id,
                                                      columns)
                elif choice == "name":
                    data = item_category.search_by_name(self.connection, category_name,
                                                        columns)

                df = pd.DataFrame.from_records(data, columns=columns)[:1000]

                with col2:
                    with st.beta_expander("Show category with selected column(s)",
                                          expanded=True):
                        st.dataframe(df)

            elif self.current_option == "Buyer":
                pass

            elif self.current_option == "Shop":
                with col1:
                    st.info("""
                        Input name to search for shop in the database.
                        If there is no input, all entries be shown.\n
                        *Limit to 1000 rows.*
                    """)
                    choice = st.radio("Search by id/name: ", options=['id', 'name'])

                    if choice == "id":
                        shop_id = st.number_input("Input shop id: ",
                                                  step=1,
                                                  value=0,
                                                  min_value=0,
                                                  max_value=shop.max_id(self.connection)
                                                  or 0)
                    elif choice == "name":
                        shop_name = st.text_input("Input shop name (* to search all): ",
                                                  value="")

                    columns = st.multiselect("Select columns to show: ",
                                             self.shop_columns)

                if not columns:
                    columns = self.shop_columns

                if choice == "id":
                    data = shop.search_by_id(self.connection, shop_id, columns)
                elif choice == "name":
                    data = shop.search_by_name(self.connection, shop_name, columns)

                df = pd.DataFrame.from_records(data, columns=columns)[:1000]

                with col2:
                    with st.beta_expander("Show shop with selected column(s)",
                                          expanded=True):
                        st.dataframe(df)

            elif self.current_option == "Imports":
                with col1:
                    st.info("""
                        Input name to search for import record in the database.
                        If there is no input, all entries be shown.\n
                        *Limit to 1000 rows.*
                    """)
                    choice = st.radio("Search by id/date/shop: ",
                                      options=['id', 'date', 'shop', 'get all records'])

                    if choice == "id":
                        import_id = st.number_input(
                            "Input import id: ",
                            step=1,
                            value=0,
                            min_value=0,
                            max_value=imports.max_id(self.connection) or 0)
                    elif choice == "date":
                        import_date = datetime.fromordinal(
                            st.date_input(
                                "Input date: ",
                                min_value=imports.get_min_max_date(self.connection)[0],
                                max_value=imports.get_min_max_date(self.connection)[1],
                                value=imports.get_min_max_date(self.connection)[0],
                            ).toordinal()).strftime('%Y-%m-%d')
                    elif choice == "shop":
                        try:
                            shop_id = st.selectbox(
                                "Input shop id: ",
                                options=[i for i in range(shop.max_id(self.connection))]
                                or [0])
                        except TypeError:
                            shop_id = None
                            st.warning("There is no shop in the database yet!")

                    columns = st.multiselect("Select columns to show: ",
                                             self.imports_columns)

                if not columns:
                    columns = self.imports_columns

                if choice == "id":
                    data = imports.search_by_id(self.connection, import_id, columns)
                elif choice == "date":
                    data = imports.search_by_date(self.connection, import_date, columns)
                elif choice == "shop":
                    data = imports.search_by_shop_id(self.connection, shop_id, columns)
                elif choice == "get all records":
                    data = imports.search_all(self.connection, columns)

                df = pd.DataFrame.from_records(data, columns=columns)[:1000]

                with col2:
                    with st.beta_expander("Show import with selected column(s)",
                                          expanded=True):
                        st.dataframe(df)

                    with st.beta_expander("Search for import details"):
                        try:
                            selected_id = int(
                                st.selectbox("Choose which import record to search: ",
                                             options=df["importID"].unique().tolist()))
                        except TypeError:
                            selected_id = None

                        data = import_detail.search_by_import_id(
                            self.connection, selected_id)
                        st.dataframe(
                            pd.DataFrame.from_records(data,
                                                      columns=import_detail.columns_names(
                                                          self.connection)))

            elif self.current_option == "Transactions":
                with col1:
                    st.info("""
                        Input name to search for transaction record in the database.
                        If there is no input, all entries be shown.\n
                        *Limit to 1000 rows.*
                    """)
                    choice = st.radio("Search by id/date/status/customer/shop: ",
                                      options=[
                                          'id', 'date', 'status', 'customer', 'shop',
                                          'get all records'
                                      ])

                    if choice == "id":
                        transaction_id = st.number_input(
                            "Input transaction id: ",
                            step=1,
                            value=0,
                            min_value=0,
                            max_value=transactions.max_id(self.connection) or 0)
                    elif choice == "date":
                        transaction_date = datetime.fromordinal(
                            st.date_input(
                                "Input date: ",
                                min_value=transactions.get_min_max_date(
                                    self.connection)[0],
                                max_value=transactions.get_min_max_date(
                                    self.connection)[1],
                                value=transactions.get_min_max_date(self.connection)[0],
                            ).toordinal()).strftime('%Y-%m-%d')
                    elif choice == "status":
                        transaction_status = st.radio("Transaction status: ",
                                                      options=['Pending',
                                                               'Completed']).upper()
                    elif choice == "customer":
                        customer_id = st.number_input(
                            "Input customer id: ",
                            step=1,
                            value=0,
                            min_value=0,
                            max_value=customer.max_id(self.connection) or 0)
                    elif choice == "shop":
                        try:
                            shop_id = st.selectbox(
                                "Input shop id: ",
                                options=[i for i in range(shop.max_id(self.connection))]
                                or [0])
                        except TypeError:
                            shop_id = None
                            st.warning("There is no shop in the database yet!")

                    columns = st.multiselect("Select columns to show: ",
                                             self.transactions_columns)

                if not columns:
                    columns = self.transactions_columns

                if choice == "id":
                    data = transactions.search_by_id(self.connection, transaction_id,
                                                     columns)
                elif choice == "date":
                    data = transactions.search_by_date(self.connection, transaction_date,
                                                       columns)
                elif choice == "status":
                    data = transactions.search_by_status(self.connection,
                                                         transaction_status, columns)
                elif choice == "customer":
                    data = transactions.search_by_customer_id(self.connection,
                                                              customer_id, columns)
                elif choice == "shop":
                    data = transactions.search_by_shop_id(self.connection, shop_id,
                                                          columns)
                elif choice == "get all records":
                    data = transactions.search_all(self.connection, columns)

                df = pd.DataFrame.from_records(data, columns=columns)[:1000]

                with col2:
                    with st.beta_expander("Show transaction with selected column(s)",
                                          expanded=True):
                        st.dataframe(df)

                    with st.beta_expander("Search for transaction details"):
                        try:
                            selected_id = int(
                                st.selectbox(
                                    "Choose which transaction record to search: ",
                                    options=df["transactionID"].unique().tolist()))
                        except TypeError:
                            selected_id = None

                        data = transaction_detail.search_by_transaction_id(
                            self.connection, selected_id)
                        st.dataframe(
                            pd.DataFrame.from_records(
                                data,
                                columns=transaction_detail.columns_names(
                                    self.connection)))

            elif self.current_option == "Item":
                with col1:
                    st.info("""
                        Input name to search for item in the database.
                        If there is no input, all entries be shown.\n
                        *Limit to 1000 rows.*
                    """)
                    choice = st.radio("Search by id/name/category/shop: ",
                                      options=['id', 'name', 'category', 'shop'])

                    if choice == "id":
                        item_id = st.number_input("Input item id: ",
                                                  step=1,
                                                  value=0,
                                                  min_value=0,
                                                  max_value=item.max_id(self.connection)
                                                  or 0)
                    elif choice == "name":
                        item_name = st.text_input("Input item name (* to search all): ",
                                                  value="")
                    elif choice == "category":
                        category_id = st.number_input(
                            "Input category id: ",
                            step=1,
                            value=0,
                            min_value=0,
                            max_value=item_category.max_id(self.connection) or 0)
                    elif choice == "shop":
                        shop_id = st.number_input("Input shop id: ",
                                                  step=1,
                                                  value=0,
                                                  min_value=0,
                                                  max_value=shop.max_id(self.connection)
                                                  or 0)

                    columns = st.multiselect("Select columns to show: ",
                                             self.item_columns)

                if not columns:
                    columns = self.item_columns

                if choice == "id":
                    data = item.search_by_id(self.connection, item_id, columns)
                elif choice == "name":
                    data = item.search_by_name(self.connection, item_name, columns)
                elif choice == "category":
                    data = item.search_by_category_id(self.connection, category_id,
                                                      columns)
                elif choice == "shop":
                    data = item.search_by_shop_id(self.connection, shop_id, columns)

                df = pd.DataFrame.from_records(data, columns=columns)[:1000]

                with col2:
                    with st.beta_expander("Show item with selected column(s)",
                                          expanded=True):
                        st.dataframe(df)

    def show_add(self):
        with st.beta_container():
            self.current_option = st.selectbox("Select table to add: ", self.tables)

            if self.current_option == "Customer":
                customer_name = st.text_input("Input customer name: ", value="")

                _last_customer_id = customer.max_id(self.connection) or -1
                customer_id = _last_customer_id + 1

                if st.button("Add customer"):
                    check = customer.insert(self.connection, customer_id, customer_name)

                    with st.spinner("Adding customer..."):
                        if check is None:
                            st.exception("Error when adding customer!")
                            st.stop()
                        else:
                            st.success("Customer was added successfully!")
                            data = customer.search_by_id(self.connection, customer_id)
                            st.dataframe(
                                pd.DataFrame.from_records(data,
                                                          columns=self.customer_columns))

            elif self.current_option == "ItemCategory":
                category_name = st.text_input("Input category name: ", value="")

                _last_category_id = item_category.max_id(self.connection) or -1
                category_id = _last_category_id + 1

                if st.button("Add item category"):
                    check = item_category.insert(self.connection, category_id,
                                                 category_name)

                    with st.spinner("Adding item category..."):
                        if check is None:
                            st.exception("Error when adding category!")
                            st.stop()
                        else:
                            st.success("Item category was added successfully!")
                            data = item_category.search_by_id(self.connection,
                                                              category_id)
                            st.dataframe(
                                pd.DataFrame.from_records(data,
                                                          columns=self.category_columns))

            elif self.current_option == "Buyer":
                pass

            elif self.current_option == "Shop":
                shop_name = st.text_input("Input shop name: ", value="")

                _last_shop_id = shop.max_id(self.connection) or -1
                shop_id = _last_shop_id + 1

                if st.button("Add shop"):
                    check = shop.insert(self.connection, shop_id, shop_name)

                    with st.spinner("Adding shop..."):
                        if check is None:
                            st.exception("Error when adding shop!")
                            st.stop()
                        else:
                            st.success("shop was added successfully!")
                            data = shop.search_by_id(self.connection, shop_id)
                            st.dataframe(
                                pd.DataFrame.from_records(data,
                                                          columns=self.shop_columns))

            elif self.current_option == "Imports":
                st.warning("Not yet implemented.")
                st.stop()

            elif self.current_option == "Transactions":
                st.warning("Not yet implemented.")
                st.stop()

            elif self.current_option == "Item":
                item_name = st.text_input("Input item name: ", value="")

                _last_item_id = item.max_id(self.connection) or -1
                item_id = _last_item_id + 1

                quantity = st.number_input("Input item quantity: ",
                                           step=1,
                                           value=0,
                                           min_value=0)

                categories = {}
                for category in item_category.search_all(self.connection):
                    categories[category[0]] = category[1]
                category_name = st.selectbox("Input item category: ",
                                             list(categories.values()))
                category_id = None
                for key, value in categories.items():
                    if value == category_name:
                        category_id = key
                st.write(f"Category ID currently: {category_id}")

                shops = {}
                for shop in shop.search_all(self.connection):
                    shops[shop[0]] = shop[1]
                shop_name = st.selectbox("Input shop name: ", list(shops.values()))
                shop_id = None
                for key, value in shops.items():
                    if value == shop_name:
                        shop_id = key

                st.write(f"Shop ID currently: {shop_id}")

                if st.button("Add item"):
                    check = item.insert(self.connection, item_id, item_name, quantity,
                                        category_id, shop_id)

                    with st.spinner("Adding item..."):
                        if check is None:
                            st.exception("Error when adding item!")
                            st.stop()
                        else:
                            st.success("shop was added successfully!")
                            data = item.search_by_id(self.connection, item_id)
                            st.dataframe(
                                pd.DataFrame.from_records(data,
                                                          columns=self.item_columns))

    def show_remove(self):
        tables_for_remove = self.tables.copy()
        try:
            tables_for_remove.remove("Imports")
            tables_for_remove.remove("Transactions")
        except ValueError:
            pass

        with st.beta_container():
            self.current_option = st.selectbox("Select table to remove: ",
                                               tables_for_remove)

            if self.current_option == "Customer":
                st.info("""
                    Input id or name to search for customer to remove from the database.
                    If there is no input, all entries be shown.
                """)
                choice = st.radio("Search by id/name: ", options=['id', 'name'])

                if choice == "id":
                    customer_id = st.number_input(
                        "Input customer id: ",
                        step=1,
                        value=0,
                        min_value=0,
                        max_value=customer.max_id(self.connection) or 0)
                    data = customer.search_by_id(self.connection, customer_id)
                elif choice == "name":
                    customer_name = st.text_input("Input customer name: ", value="")
                    data = customer.search_by_name(self.connection, customer_name)

                df = pd.DataFrame.from_records(data, columns=self.customer_columns)[:1000]

                with st.beta_expander("Show all customers"):
                    st.dataframe(df)

                with st.beta_expander("Remove customer(s)", expanded=True):
                    if choice == "id":
                        data = customer.search_by_id(self.connection, customer_id)
                    elif choice == "name":
                        selected_ids = st.multiselect("Select customer id(s): ",
                                                      df["customerID"])
                        data = customer.search_by_name(self.connection, customer_name)

                    if len(df["customerID"]) == 1:
                        selected_ids = df["customerID"].values

                    try:
                        df = pd.concat([
                            pd.DataFrame.from_records(
                                data,
                                columns=self.customer_columns).loc[df["customerID"] == i]
                            for i in selected_ids
                        ],
                                       ignore_index=True)
                    except ValueError:
                        pass
                    st.dataframe(df)

                    if st.button("Remove customer"):
                        for Cid in selected_ids:
                            if transactions.search_by_customer_id(
                                    self.connection, int(Cid)):
                                st.error(f"""
                                    Customer {Cid} can't be removed. They have already made a transaction.
                                """)
                            else:
                                removed = customer.delete_by_id(self.connection, int(Cid))
                                st.experimental_rerun()

            elif self.current_option == "ItemCategory":
                st.info("""
                    Input id or name to search for item category to remove from the database.
                    If there is no input, all entries be shown.
                """)
                choice = st.radio("Search by id/name: ", options=['id', 'name'])

                if choice == "id":
                    category_id = st.number_input(
                        "Input category id: ",
                        step=1,
                        value=0,
                        min_value=0,
                        max_value=item_category.max_id(self.connection) or 0)
                    data = item_category.search_by_id(self.connection, category_id)
                elif choice == "name":
                    category_name = st.text_input("Input category name: ", value="")
                    data = item_category.search_by_name(self.connection, category_name)

                df = pd.DataFrame.from_records(data, columns=self.category_columns)[:1000]

                with st.beta_expander("Show all item categories"):
                    st.dataframe(df)

                with st.beta_expander("Remove item category(s)", expanded=True):
                    if choice == "id":
                        data = item_category.search_by_id(self.connection, category_id)
                    elif choice == "name":
                        selected_ids = st.multiselect("Select category id(s): ",
                                                      df["categoryID"])
                        data = item_category.search_by_name(self.connection,
                                                            category_name)

                    if len(df["categoryID"]) == 1:
                        selected_ids = df["categoryID"].values

                    try:
                        df = pd.concat([
                            pd.DataFrame.from_records(
                                data,
                                columns=self.category_columns).loc[df["categoryID"] == i]
                            for i in selected_ids
                        ],
                                       ignore_index=True)
                    except ValueError:
                        pass
                    st.dataframe(df)

                    if st.button("Remove item category"):
                        for ICid in selected_ids:
                            if item.search_by_category_id(self.connection, int(ICid)):
                                st.error(f"""
                                    Item category {ICid} can't be removed. There is at least an item assigned to it.
                                """)
                            else:
                                removed = item_category.delete_by_id(
                                    self.connection, int(ICid))
                                st.experimental_rerun()

            elif self.current_option == "Buyer":
                pass

            elif self.current_option == "Shop":
                st.info("""
                    Input id or name to search for shop to remove from the database.
                    If there is no input, all entries be shown.
                """)
                choice = st.radio("Search by id/name: ", options=['id', 'name'])

                if choice == "id":
                    shop_id = st.number_input("Input shop id: ",
                                              step=1,
                                              value=0,
                                              min_value=0,
                                              max_value=shop.max_id(self.connection) or 0)
                    data = shop.search_by_id(self.connection, shop_id)
                elif choice == "name":
                    shop_name = st.text_input("Input shop name: ", value="")
                    data = shop.search_by_name(self.connection, shop_name)

                df = pd.DataFrame.from_records(data, columns=self.shop_columns)[:1000]

                with st.beta_expander("Show all shops"):
                    st.dataframe(df)

                with st.beta_expander("Remove shop(s)"):
                    if choice == "id":
                        data = shop.search_by_id(self.connection, shop_id)
                    elif choice == "name":
                        selected_ids = st.multiselect("Select shop id(s): ", df["shopID"])
                        data = shop.search_by_name(self.connection, shop_name)

                    if len(df["shopID"]) == 1:
                        selected_ids = df["shopID"].values

                    try:
                        df = pd.concat([
                            pd.DataFrame.from_records(
                                data, columns=self.shop_columns).loc[df["shopID"] == i]
                            for i in selected_ids
                        ],
                                       ignore_index=True)
                    except ValueError:
                        pass
                    st.dataframe(df)

                    if st.button("Remove shop"):
                        for Sid in selected_ids:
                            if item.search_by_shop_id(self.connection, int(Sid)):
                                st.error(f"""
                                    Shop {Sid} can't be removed. There is at least an item assigned to it.
                            """)
                            else:
                                removed = shop.delete_by_id(self.connection, int(Sid))
                                st.experimental_rerun()

            elif self.current_option == "Item":
                st.info("""
                    Input id or name to search for item to remove from the database.
                    If there is no input, all entries be shown.
                """)
                choice = st.radio("Search by id/name/category/shop: ",
                                  options=['id', 'name', 'category', 'shop'])

                if choice == "id":
                    item_id = st.number_input("Input item id: ",
                                              step=1,
                                              value=0,
                                              min_value=0,
                                              max_value=item.max_id(self.connection) or 0)
                    data = item.search_by_id(self.connection, item_id)
                elif choice == "name":
                    item_name = st.text_input("Input item name (* to search all): ",
                                              value="")
                    data = item.search_by_name(self.connection, item_name)
                elif choice == "category":
                    category_id = st.number_input(
                        "Input category id: ",
                        step=1,
                        value=0,
                        min_value=0,
                        max_value=item_category.max_id(self.connection) or 0)
                    data = item.search_by_category_id(self.connection, category_id)
                elif choice == "shop":
                    shop_id = st.number_input("Input shop id: ",
                                              step=1,
                                              value=0,
                                              min_value=0,
                                              max_value=shop.max_id(self.connection) or 0)
                    data = item.search_by_shop_id(self.connection, shop_id)

                df = pd.DataFrame.from_records(data, columns=self.customer_columns)[:1000]

                with st.beta_expander("Show all items"):
                    st.dataframe(df)

                with st.beta_expander("Remove item(s)", expanded=True):
                    if choice == "id":
                        data = item.search_by_id(self.connection, item_id)
                    elif choice == "name":
                        selected_ids = st.multiselect("Select item id(s): ", df["itemID"])
                        data = item.search_by_name(self.connection, item_name)

                    if len(df["itemID"]) == 1:
                        selected_ids = df["itemID"].values

                    try:
                        df = pd.concat([
                            pd.DataFrame.from_records(
                                data,
                                columns=self.customer_columns).loc[df["itemID"] == i]
                            for i in selected_ids
                        ],
                                       ignore_index=True)
                    except ValueError:
                        pass
                    st.dataframe(df)

                    if st.button("Remove item"):
                        for Iid in selected_ids:
                            removed = item.delete_by_id(self.connection, int(Iid))
                            st.experimental_rerun()

    def _export_data(self, export_path):
        import os
        import csv

        if st.button("Start exporting data"):
            try:
                for table in self.tables:
                    # Export data into CSV file
                    with st.spinner(f"Exporting table '{table}'..."):
                        cursor = self.connection.cursor()
                        cursor.execute(f"SELECT * FROM {table}")
                        filename = os.path.join(export_path, f"{table}.csv")
                        with open(filename, "w+", encoding="utf-8",
                                  newline="") as csv_file:
                            csv_writer = csv.writer(csv_file, delimiter=",")
                            csv_writer.writerow([i[0] for i in cursor.description])
                            csv_writer.writerows(cursor)
                    st.success(f"Data exported Successfully into {filename}")

            except sqlite3.Error as err:
                print(err)
