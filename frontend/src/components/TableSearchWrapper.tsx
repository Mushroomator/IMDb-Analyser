import { Box, VStack } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { SearchBar } from "./SearchBar";

export interface ITable<T>{
    data: Array<T>
}

export interface ITableSearchWrapper<T> extends ITable<T> {
    searchFunc: (all: Array<T>, searchStr: string) => Promise<Array<T>> 
    children: (data: Array<T>) => React.ReactNode
    searchPlaceholder: string
    maxH?: string
}

export function TableSearchWrapper<T>({ data, searchFunc, searchPlaceholder, children, maxH = "50vh" }: ITableSearchWrapper<T>) {
    const [searchStr, setSearchStr] = useState<string>("");
    const [curData, setCurData] = useState<Array<T>>(data);

    useEffect(() => {
        const search = async (searchStr: string) => {
            const searchResults = await searchFunc(data, searchStr.toLowerCase());
            setCurData(searchResults);
        }
        search(searchStr);
    }, [searchStr, searchFunc, data])

    return (
        <VStack flexBasis={"100%"} w={"100%"} alignSelf={"normal"} maxH={maxH}>
            <SearchBar
                searchStr={searchStr}
                setSearchStr={setSearchStr}
                withImg={false}
                inputOptions={{
                    size: "sm",
                    placeholder: searchPlaceholder,
                    borderRadius: "2xl"
                }}
            />
            <Box
                w={"100%"}
                overflowY={"scroll"}
                h={"100%"}
                css={{
                    '&::-webkit-scrollbar': {
                        width: '6px',
                    },
                    '&::-webkit-scrollbar-track': {
                        width: '6px',
                    },
                    "::-webkit-scrollbar-corner": {
                        backgroundColor: "transparent"
                    },
                    "&::-webkit-resizer": {
                        backgroundColor: "transparent"
                    },
                    '&::-webkit-scrollbar-thumb': {
                        background: "var(--chakra-colors-gray-200)",
                        borderRadius: "5px"
                    },
                }}
            >
                {children(curData)}
            </Box>
        </VStack>
    )
}