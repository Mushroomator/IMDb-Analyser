import { Badge, Link, Table, Tbody, Td, Th, Thead, Tr } from "@chakra-ui/react";
import { baseDomain, moviePrefix } from "../config";
import { searchForStrInAwards } from "../searchUtils";
import { IActorAward } from "../types";
import { ITable, TableSearchWrapper } from "./TableSearchWrapper";

export function AwardTable({ data }: ITable<IActorAward>) {
    return (
        <TableSearchWrapper 
            searchFunc={searchForStrInAwards} 
            data={data}
            searchPlaceholder="Search awards">
            {data => (
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
                        {data.map((aw, idx) => (
                            <Tr
                                key={`mov-row-${idx}`}
                                _hover={{
                                    bg: "var(--chakra-colors-gray-100)"
                                }}>

                                <Td>{aw.aw_year}</Td>
                                <Td>{aw.awc_cat_name}</Td>
                                <Td>{aw.aw_description}</Td>
                                <Td>
                                    <Badge colorScheme={"blue"} variant={aw.aw_outcome === "Winner" ? "solid" : "subtle"}>
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
            )}
        </TableSearchWrapper>
    )
}