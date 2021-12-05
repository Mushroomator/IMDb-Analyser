import { SearchIcon } from "@chakra-ui/icons"
import { Input, InputGroup, InputLeftElement, InputProps } from "@chakra-ui/react"

export interface ISearchBar {
    searchStr: string
    setSearchStr: React.Dispatch<React.SetStateAction<string>>
    withImg?: boolean
    inputOptions?: InputProps
    placeholder?: string
}


export function SearchBar({ searchStr, setSearchStr, placeholder, inputOptions, withImg = true }: ISearchBar) {
    return (
        <InputGroup>
            {withImg &&
                <InputLeftElement
                    pointerEvents={"none"}
                    children={<SearchIcon color={"gray.200"} ml={5} />} />
            }
            <Input
                mx={2}
                variant={"outline"}
                value={searchStr}
                onChange={e => setSearchStr(e.target.value)}
                placeholder={placeholder}
                width={"100%"}
                {...inputOptions}
            />
        </InputGroup>
    )
}