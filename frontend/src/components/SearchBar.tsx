import { Input, InputProps } from "@chakra-ui/react"

export interface ISearchBar {
    searchStr: string
    setSearchStr: React.Dispatch<React.SetStateAction<string>>
    inputOptions?: InputProps
    placeholder?: string
}


export function SearchBar({ searchStr, setSearchStr, placeholder, inputOptions }: ISearchBar) {

    return (
        <Input
            mx={2}
            variant={"outline"}
            value={searchStr}
            onChange={e => setSearchStr(e.target.value)}
            placeholder={placeholder}
            width={"100%"}
            {...inputOptions}
        />
    )
}