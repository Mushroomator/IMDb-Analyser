import { VStack } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { apiPrefix } from "../config";
import { useFetch } from "../hooks/useFetch";
import { searchForStrInActorsAbout } from "../searchUtils";
import { IActorAbout, IActorsResponse } from "../types";
import ActorCard from "../components/ActorCard";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { SearchBar } from "../components/SearchBar";
import { CustomAlert } from "../components/CustomAlert";

export function ActorList() {
    // STATE
    const [searchStr, setSearchStr] = useState<string>("");
    const [curActors, setCurActors] = useState<Array<IActorAbout>>([])

    const { isLoading, error, data: allActors } = useFetch<Array<IActorAbout>, IActorsResponse>(
        `${apiPrefix}/actors`,
        [],
        resObj => resObj.data,
        { method: "POST" }
    )


    useEffect(() => {
        const search = async (searchStr: string) => {
            const searchResults = await searchForStrInActorsAbout(allActors, searchStr.toLowerCase());
            setCurActors(searchResults);
        }
        search(searchStr);
    }, [searchStr, allActors])

    if (error) return <CustomAlert status="error" alertTitle={error.title} alertDesc={error.desc} />
    if (isLoading) return <LoadingSpinner />
    if (allActors.length === 0) {
        return (
            <CustomAlert
                status="info"
                alertTitle="No data"
                alertDesc="You might need to trigger webscraping using the button on the top right first!" />
        )
    }

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