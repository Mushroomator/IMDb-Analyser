import { Table, Tbody, Td, Text, Th, Thead, Tr } from "@chakra-ui/react";
import { maxRating } from "../config";
import { IPerYearMovieRating } from "../types";

export interface IPerYearRatingTable {
    ratings: Array<IPerYearMovieRating>
}

export function PerYearRatingTable({ ratings }: IPerYearRatingTable) {
    return (
        <Table variant={"simple"}>
            <Thead>
                <Tr>
                    <Th textTransform={"uppercase"}>{"Year"}</Th>
                    <Th textTransform={"uppercase"}>{"Rating"}</Th>
                </Tr>
            </Thead>
            <Tbody fontSize={"sm"}>
                {ratings.map((rating, idx) => (
                    <Tr
                        key={`mov-row-${idx}`}
                        _hover={{
                            bg: "var(--chakra-colors-gray-100)"
                        }}>

                        <Td>{rating.mov_year}</Td>
                        <Td>
                            <Text display={"inline"} fontSize={"md"} fontWeight={"bold"}>
                                {rating.mov_rating}
                            </Text>
                            /
                            <Text display={"inline"}>
                                {maxRating}
                            </Text>
                        </Td>
                    </Tr>
                ))}
            </Tbody>
        </Table>
    )
}