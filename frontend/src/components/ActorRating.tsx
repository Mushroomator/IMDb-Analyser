import { HStack } from "@chakra-ui/react";
import { PerYearRatingTable } from "./PerYearRatingTable";
import { Rating } from "./Rating";
import { IPerYearMovieRating } from "../types";

export interface IActorRating {
    overallRating: number
    perYearRating: Array<IPerYearMovieRating>
}

export function ActorRating({ overallRating, perYearRating }: IActorRating) {
    return (
        <HStack w={"100%"} h={["350px", "250px"]} flexDirection={["column", "row"]}>
            <Rating rating={overallRating}/>
            <PerYearRatingTable key={"per-year-movie-rating-table"} data={perYearRating} />
        </HStack>
    )
}