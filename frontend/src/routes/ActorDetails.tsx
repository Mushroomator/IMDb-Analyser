import { Accordion, AccordionButton, AccordionIcon, AccordionItem, AccordionPanel, Avatar, Box, Heading, Spinner, Text, VStack } from "@chakra-ui/react";
import { useParams } from "react-router-dom";
import { apiPrefix, mapSexIdentToTxt } from "../config";
import { useFetch } from "../hooks/useFetch";
import { IActorDetails, IActorDetailsResponse } from "../types";
import { ActorRating } from "../components/ActorRating";
import { AwardTable } from "../components/AwardTable";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { MovieTable } from "../components/MovieTable";

export function ActorDetails() {
    // Read actor ID from URL path
    const { actorId } = useParams();

    const { isLoading, error, data: actorDetails } = useFetch<IActorDetails | null, IActorDetailsResponse>(
        `${apiPrefix}/actors/${actorId}`,
        null,
        resObj => resObj.data,
        { method: "POST" }
    )

    if (!actorDetails) return <LoadingSpinner/>

    return (
        <VStack
            bg={"whiteAlpha.900"}
            boxShadow={"lg"}
            borderRadius={"xl"}
            p={8}
            w={"100%"}>
            <Avatar
                bg={"blue.500"}
                fontWeight={"bold"}
                fontSize={"5xl"}
                borderRadius={"full"}
                src={actorDetails.about.act_img_url}
                name={actorDetails.about.act_fullname}
                w={["50px", "100px", "150px"]}
                h={["50px", "100px", "150px"]}
                alignSelf={"center"}
                colorScheme={"blue"}
                showBorder={true}
                borderColor={"blue.500"} />
            <Heading>{actorDetails.about.act_fullname}</Heading>
            <Text pb={8} fontSize={"sm"}>{mapSexIdentToTxt[actorDetails.about.act_sex]}</Text>

            <Accordion w={"100%"} defaultIndex={[0]} allowMultiple>
                <AccordionItem w={"100%"}>
                    <h2>
                        <AccordionButton>
                            <Box flex='1' textAlign='left'>
                                <Heading size={"sm"} colorScheme={"blackAlpha"}>Rating</Heading>
                            </Box>
                            <AccordionIcon />
                        </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4} w={"100%"}>
                        <ActorRating overallRating={actorDetails.overallRating} perYearRating={actorDetails.perYearRating} />
                    </AccordionPanel>
                </AccordionItem>
                <AccordionItem w={"100%"}>
                    <h2>
                        <AccordionButton>
                            <Box flex='1' textAlign='left'>
                                <Heading size={"sm"} colorScheme={"blackAlpha"}>Top 5 Movies</Heading>
                            </Box>
                            <AccordionIcon />
                        </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4} w={"100%"}>
                        <MovieTable key={"top5-movie-table"} data={actorDetails.topFiveMovies}/>
                    </AccordionPanel>
                </AccordionItem>
                <AccordionItem>
                    <h2>
                        <AccordionButton>
                            <Box flex='1' textAlign='left'>
                                <Heading size={"sm"} colorScheme={"blackAlpha"}>Biography</Heading>
                            </Box>
                            <AccordionIcon />
                        </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4}>
                        <Text lineHeight={"6"} fontSize={"sm"} textAlign={"justify"} p={4}>{actorDetails.about.act_bio}</Text>
                    </AccordionPanel>
                </AccordionItem>
                <AccordionItem>
                    <h2>
                        <AccordionButton>
                            <Box flex='1' textAlign='left'>
                                <Heading size={"sm"} colorScheme={"blackAlpha"}>Movies</Heading>
                            </Box>
                            <AccordionIcon />
                        </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4}>
                        <MovieTable key={"movie-table"} data={actorDetails.allTimeMovies}/>
                    </AccordionPanel>
                </AccordionItem>
                <AccordionItem>
                    <h2>
                        <AccordionButton>
                            <Box flex='1' textAlign='left'>
                                <Heading size={"sm"} colorScheme={"blackAlpha"}>Awards</Heading>
                            </Box>
                            <AccordionIcon />
                        </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4}>
                        <AwardTable key={"award-table"} data={actorDetails.awards} />
                    </AccordionPanel>
                </AccordionItem>
            </Accordion>
        </VStack>
    )
}


