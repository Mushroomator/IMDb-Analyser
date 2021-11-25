import { Input } from "@chakra-ui/react"

export interface ISearchBar{
    searchStr: string
    setSearchStr: React.Dispatch<React.SetStateAction<string>>
}

export function SearchBar({ searchStr, setSearchStr }: ISearchBar) {
    
    return (
        <Input
            mx={2}
            variant={"outline"}
            value={searchStr}
            onChange={e => setSearchStr(e.target.value)}
            placeholder="Search the database"
            width={"100%"}
        />
    )
}