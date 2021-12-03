import { Table, Tbody, Td, Text, Th, Thead, Tr } from "@chakra-ui/react";
import { maxRating } from "../config";
import { searchForStrInRatings } from "../searchUtils";
import { IPerYearMovieRating } from "../types";
import { ITable, TableSearchWrapper } from "./TableSearchWrapper";


export function PerYearRatingTable({ data }: ITable<IPerYearMovieRating>) {
    return (
        <TableSearchWrapper
            searchFunc={searchForStrInRatings}
            data={data}
            searchPlaceholder="Search ratings">
            {data => (
                <Table variant={"simple"} h={"100%"} w={"100%"}>
                    <Thead>
                        <Tr>
                            <Th textTransform={"uppercase"}>{"Year"}</Th>
                            <Th textTransform={"uppercase"}>{"Rating"}</Th>
                        </Tr>
                    </Thead>

                    <Tbody fontSize={"sm"} h={"100%"} w={"100%"}>
                        {data.map((rating, idx) => (
                            <Tr
                                key={`mov-row-${idx}`}
                                _hover={{
                                    bg: "var(--chakra-colors-gray-100)"
                                }}>

                                <Td>{rating.mov_year}</Td>
                                <Td>
                                    <Text display={"inline"} fontSize={"md"} fontWeight={"bold"}>
                                        {rating.mov_rating.toFixed(1)}
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
            )}
        </TableSearchWrapper>
    )
}