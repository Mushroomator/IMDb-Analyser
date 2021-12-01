import { VStack } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useFetch } from "../hooks/useFetch";
import { searchForStrInActorsAbout } from "../searchUtils";
import { IActorAbout, IActorsResponse } from "../types";
import ActorCard from "./ActorCard";
import { SearchBar } from "./SearchBar";

// export interface IActorList {

// }

export function ActorList() {
    // STATE
    const [searchStr, setSearchStr] = useState<string>("");
    const [curActors, setCurActors] = useState<Array<IActorAbout>>([])

    const { isLoading, error, data: allActors } = useFetch<Array<IActorAbout>, IActorsResponse>(
        "/api/actors",
        [],
        resObj => resObj.data,
        { method: "POST" }
    )


    useEffect(() => {
        const searchResults = searchForStrInActorsAbout(allActors, searchStr.toLowerCase());
        setCurActors(searchResults);
    }, [searchStr, allActors])

    return (
        <VStack
            w={"100%"}
            h={"100%"}
        >
            <SearchBar
                inputOptions={{
                    mb: 5
                }}
                searchStr={searchStr}
                setSearchStr={setSearchStr}
                placeholder="Search actors"
            />
            {curActors.map((actor, idx) => (
                <ActorCard key={idx} {...actor} />
            ))}
        </VStack>
    )
}