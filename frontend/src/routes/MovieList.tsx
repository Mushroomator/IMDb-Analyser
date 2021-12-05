import { Heading, VStack } from "@chakra-ui/react";
import { CustomAlert } from "../components/CustomAlert";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { MovieTable } from "../components/MovieTable";
import { apiPrefix } from "../config";
import { useFetch } from "../hooks/useFetch";
import { IActorMovie, IMovieResponse } from "../types";

export function MovieList() {
    const { isLoading, error, data: allActors } = useFetch<Array<IActorMovie>, IMovieResponse>(
        `${apiPrefix}/movies`,
        [],
        resObj => resObj.data,
        { method: "POST" }
    )

    if (error) return <CustomAlert status="error" alertTitle={"test"} alertDesc={"test"} />
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
            bg={"whiteAlpha.900"}
            boxShadow={"lg"}
            borderRadius={"xl"}
            p={8}
        >
            <Heading pb={8}>List of all movies</Heading>
            <MovieTable data={allActors} maxH="72vh" />
        </VStack>
    )
}