import { Box, Heading, HStack, VStack } from "@chakra-ui/react";
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

    if (isLoading) return <LoadingSpinner />

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
            <MovieTable data={allActors} maxH="72vh"/>
        </VStack>
    )
}