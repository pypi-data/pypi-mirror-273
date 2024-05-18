def gogotable(headers, rows):  # noqa
    """
    Go Go Table

    :param headers: headers of the table
    :param rows: the data of the table
    :return: a list of strings representing the table
    """

    has_data_rows = True

    # Find the size of each column
    columns_length = []
    for i, _ in enumerate(headers):
        column_length = 0
        try:
            column_length = max(len(str(row[i])) for row in rows)
        except IndexError:
            pass
        except ValueError:
            # There are no rows to calculate the max
            has_data_rows = False

        # Sometimes, the header size is greater than the value
        if len(headers[i]) > column_length:
            column_length = len(headers[i])

        columns_length.append(column_length)

    # Vertical Border
    vb = "|"
    # Horizontal Border
    hb = "-"

    horizontal_border = vb + hb.join(hb * (1 + cl + 1) for cl in columns_length) + vb
    header_cells = [
        f" {header:^{length}} " for header, length in zip(headers, columns_length)
    ]
    header_line = vb + vb.join(header_cells) + vb

    table = [horizontal_border, header_line, horizontal_border]
    if has_data_rows:
        for row in rows:
            data_cells = [
                f" {data:>{length}} " for data, length in zip(row, columns_length)
            ]
            table.append(vb + vb.join(data_cells) + vb)

    table.append(horizontal_border)

    return table
