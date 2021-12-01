import { Table, TableBodyProps, TableCaption, TableCaptionProps, TableCellProps, TableColumnHeaderProps, TableHeadProps, TableProps, TableRowProps, Tbody, Td, Th, Thead, Tr } from "@chakra-ui/react";
import { ReactChild, ReactChildren } from "react";
import { isValidArrIdx } from "../utils";

/**
 * Interface for toString() method
 * Object can be "stringified"
 */
export interface IStringer {
    toString: () => string
}

/**
 * Options for column headers
 */
export interface ITableColumnHeader {
    text: IStringer
    style?: TableColumnHeaderProps
}

/**
 * Options for table header
 */
export interface ITableHeader {
    headerColumns: Array<ITableColumnHeader>
    headerStyle?: TableHeadProps
    headerRowStyle?: TableRowProps
}

/**
 * Options for table caption
 */
export interface ITableCaption {
    text: IStringer
    style?: TableCaptionProps
}

/**
 * Options for table body
 */
export interface ITableBody {
    tableBodyStyle?: TableBodyProps
    tableRowStyle?: TableRowProps
    tableCellStyle?: TableCellProps
}

export interface IGenericTable {
    /**
     * Data to display, must be convertable to string
     */
    data: Array<Record<string | number | symbol, IStringer>>
    children?: ReactChild | ReactChildren | ReactChild[] | ReactChildren[]
    tableOptions?: TableProps
    header?: ITableHeader
    tableCaptionOptions?: ITableCaption
    tableBodyOptions?: ITableBody
}



export function GenericTable({ data, tableOptions, header, tableCaptionOptions, tableBodyOptions }: IGenericTable) {

    return (
        <Table {...tableOptions}>
            {tableCaptionOptions &&
                <TableCaption {...tableCaptionOptions.style}>{tableCaptionOptions.text.toString()}</TableCaption>
            }
            {/* Display a header row if specified */}
            {header &&
                <Thead {...header.headerStyle}>
                    <Tr 
                        {...header.headerRowStyle}>
                        {header.headerColumns.map((headerVal, hidx) => (
                            <Th key={`header-${hidx}`} {...headerVal.style}>
                                {headerVal.text.toString()}
                            </Th>
                        ))}
                    </Tr>
                </Thead>
            }
            <Tbody {...tableBodyOptions?.tableBodyStyle}>
                {data.map((row, ridx) => (
                    <Tr
                        key={`row-${ridx}`}
                        {...tableBodyOptions?.tableRowStyle}
                        >
                        {Object.values(row).map((colValue, cidx) => (
                            <Td
                                key={`row-${ridx}-col-${cidx}`}
                                {...tableBodyOptions?.tableCellStyle}
                                >
                                {colValue.toString()}
                            </Td>
                        ))}
                    </Tr>
                ))}
            </Tbody>
        </Table>
    )


}