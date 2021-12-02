import { Badge, Link, Table, Tbody, Td, Th, Thead, Tr } from "@chakra-ui/react";
import { baseDomain, moviePrefix } from "../config";
import { searchForStrInMovies } from "../searchUtils";
import { IActorMovie } from "../types";
import { ITable, TableSearchWrapper } from "./TableSearchWrapper";


export function MovieTable({ data }: ITable<IActorMovie>) {
    return (
        <TableSearchWrapper
            searchFunc={searchForStrInMovies}
            data={data}
            searchPlaceholder="Search movies">
            {data => (
                <Table variant={"simple"}>
                    <Thead>
                        <Tr>
                            <Th textTransform={"uppercase"}>{"Title"}</Th>
                            <Th textTransform={"uppercase"}>{"Year"}</Th>
                            <Th textTransform={"uppercase"}>{"Genres"}</Th>
                            <Th textTransform={"uppercase"}>{"Medium type"}</Th>
                            <Th textTransform={"uppercase"}>{"Rating"}</Th>
                        </Tr>
                    </Thead>
                    <Tbody fontSize={"sm"}>
                        {data.map((mov, idx) => (
                            <Tr
                                key={`mov-row-${idx}`}
                                _hover={{
                                    bg: "var(--chakra-colors-gray-100)"
                                }}>

                                <Td>
                                    <Link href={`${baseDomain}${moviePrefix}${mov.mov_href}`} isExternal>
                                        {mov.mov_title}
                                    </Link>
                                </Td>
                                <Td>{mov.mov_year}</Td>
                                <Td>
                                    {mov.genres.map((genre, genreIdx) => (
                                        <Badge
                                            key={`row-${idx}-genre-${genreIdx}`}
                                            colorScheme={"blue"}
                                            variant={"outline"}
                                            m={1}>{genre}</Badge>
                                    ))}
                                </Td>
                                <Td>{mov.met_name}</Td>
                                <Td isNumeric>{mov.mov_rating}</Td>
                            </Tr>
                        ))}
                    </Tbody>
                </Table>

            )}
        </TableSearchWrapper>
    )
}