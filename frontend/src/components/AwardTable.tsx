import { Badge, Link, Table, Tbody, Td, Th, Thead, Tr } from "@chakra-ui/react";
import { baseDomain, moviePrefix } from "../config";
import { IActorAward } from "../types";

export interface IMovieTable {
    awards: Array<IActorAward>
}

export function AwardTable({ awards }: IMovieTable) {
    return (
        <Table variant={"simple"}>
            <Thead>
                <Tr>
                    <Th textTransform={"uppercase"}>{"Year"}</Th>
                    <Th textTransform={"uppercase"}>{"Category"}</Th>
                    <Th textTransform={"uppercase"}>{"Description"}</Th>
                    <Th textTransform={"uppercase"}>{"Outcome"}</Th>
                    <Th textTransform={"uppercase"}>{"Movie"}</Th>
                </Tr>
            </Thead>
            <Tbody fontSize={"sm"}>
                {awards.map((aw, idx) => (
                    <Tr
                        key={`mov-row-${idx}`}
                        _hover={{
                            bg: "var(--chakra-colors-gray-100)"
                        }}>

                        <Td>{aw.aw_year}</Td>
                        <Td>{aw.awc_cat_name}</Td>
                        <Td>{aw.aw_description}</Td>
                        <Td>
                            <Badge colorScheme={"blue"} variant={aw.aw_outcome === "Winner" ? "solid": "subtle"}>
                                {aw.aw_outcome}
                            </Badge>
                        </Td>
                        <Td>
                            <Link href={`${baseDomain}${moviePrefix}${aw.aw_movie_href}`} isExternal>
                                {aw.aw_movie_name}
                            </Link>
                        </Td>
                    </Tr>
                ))}
            </Tbody>
        </Table>
    )
}