import { ChevronDownIcon, ChevronUpIcon } from "@chakra-ui/icons";
import { Badge, HStack, Link, Table, Tbody, Td, Text, Th, Thead, Tr, VStack } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { baseDomain, moviePrefix } from "../config";
import { IActorMovie } from "../types";
import { ITable } from "./TableSearchWrapper";

const text2Col: Record<keyof IActorMovie, string> = {
    mov_title: "Title",
    mov_year: "Year",
    mov_genres: "Genres",
    met_name: "Medium",
    mov_rating: "Rating",
    mov_href: "Movie URL"
}

async function sortAscBy<T>(data: Array<T>, by: keyof T) {
    data.sort((one, other) => {
        const oneVal = one[by]
        const otherVal = other[by]
        if (oneVal < otherVal) {
            if (oneVal > otherVal) return 1;
            else return 0;
        }
        else return -1;
    })
    return data
}

interface ISorted<T> {
    sortedBy: keyof T,
    asc: boolean
}

export function MovieTable({ data, maxH }: ITable<IActorMovie>) {
    const [sortedBy, setSortedBy] = useState<ISorted<IActorMovie>>({ sortedBy: "mov_rating", asc: false })
    const [movies, setMovies] = useState<Array<IActorMovie>>(data);

    // sort once on first render of component
    useEffect(() => {
        const search = async () => {
            await sortAscBy(movies, sortedBy.sortedBy)
        }
        search()
    }, [])

    async function setSorted(prop: keyof IActorMovie) {
        if (sortedBy.sortedBy === prop) {
            setMovies(movies.slice().reverse())
            setSortedBy({ sortedBy: prop, asc: !sortedBy.asc })
        }
        else {
            await sortAscBy<IActorMovie>(movies, prop);
            setSortedBy({ sortedBy: prop, asc: true })
        }
    }


    return (
        <VStack w={"100%"}>
            <HStack justifyContent={"flex-end"} w={"100%"}>
                <Text fontSize="xs" color="gray.500">Sorted by:</Text>
                <Text fontSize="xs" color="gray.500">{text2Col[sortedBy.sortedBy]}</Text>
                {sortedBy.asc ? <ChevronUpIcon color={"gray.500"} /> : <ChevronDownIcon color={"gray.500"} />}
            </HStack>
            <Table variant={"simple"}>
                <Thead>
                    <Tr>
                        <Th
                            borderBottomWidth={"4px"}
                            _hover={{
                                cursor: "pointer",
                                borderBottom: "var(--chakra-colors-gray-600) solid 4px"
                            }}
                            textTransform={"uppercase"} onClick={() => setSorted("mov_title")}>
                            <HStack>
                                {sortedBy.sortedBy === "mov_title" && (sortedBy.asc ? <ChevronUpIcon color={"gray.500"} /> : <ChevronDownIcon color={"gray.500"} />)}
                                <Text>Title</Text>
                            </HStack>
                        </Th>
                        <Th borderBottomWidth={"4px"}
                            _hover={{
                                cursor: "pointer",
                                borderBottom: "var(--chakra-colors-gray-600) solid 4px"
                            }}
                            textTransform={"uppercase"} onClick={() => setSorted("mov_year")}>
                            <HStack>
                                {sortedBy.sortedBy === "mov_year" && (sortedBy.asc ? <ChevronUpIcon color={"gray.500"} /> : <ChevronDownIcon color={"gray.500"} />)}
                                <Text>Year</Text>
                            </HStack>
                        </Th>
                        <Th borderBottomWidth={"4px"}
                            _hover={{
                                cursor: "pointer",
                                borderBottom: "var(--chakra-colors-gray-600) solid 4px"
                            }}
                            textTransform={"uppercase"} onClick={() => setSorted("mov_genres")}>
                            <HStack>
                                {sortedBy.sortedBy === "mov_genres" && (sortedBy.asc ? <ChevronUpIcon color={"gray.500"} /> : <ChevronDownIcon color={"gray.500"} />)}
                                <Text>Genres</Text>
                            </HStack>
                        </Th>
                        <Th borderBottomWidth={"4px"}
                            _hover={{
                                cursor: "pointer",
                                borderBottom: "var(--chakra-colors-gray-600) solid 4px"
                            }}
                            textTransform={"uppercase"} onClick={() => setSorted("met_name")}>
                            <HStack>
                                {sortedBy.sortedBy === "met_name" && (sortedBy.asc ? <ChevronUpIcon color={"gray.500"} /> : <ChevronDownIcon color={"gray.500"} />)}
                                <Text>Medium</Text>
                            </HStack>
                        </Th>
                        <Th borderBottomWidth={"4px"}
                            flexWrap={"nowrap"}
                            _hover={{
                                cursor: "pointer",
                                borderBottom: "var(--chakra-colors-gray-600) solid 4px"
                            }}
                            textTransform={"uppercase"} onClick={() => setSorted("mov_rating")}>
                            <HStack>
                                {sortedBy.sortedBy === "mov_rating" && (sortedBy.asc ? <ChevronUpIcon color={"gray.500"} /> : <ChevronDownIcon color={"gray.500"} />)}
                                <Text>Rating</Text>
                            </HStack>
                        </Th>
                    </Tr>
                </Thead>
                <Tbody fontSize={"sm"}>
                    {movies.map((mov, idx) => (
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
                            <Td>{mov.mov_year === 0 ? "No year" : mov.mov_year}</Td>
                            <Td>
                                {mov.mov_genres.map((genre, genreIdx) => (
                                    <Badge
                                        key={`row-${idx}-genre-${genreIdx}`}
                                        colorScheme={"blue"}
                                        variant={"outline"}
                                        m={1}>{genre}</Badge>
                                ))}
                            </Td>
                            <Td>{mov.met_name}</Td>
                            <Td isNumeric>{mov.mov_rating === 0 ? "No rating" : mov.mov_rating}</Td>
                        </Tr>
                    ))}
                </Tbody>
            </Table>
        </VStack>
    )
}