import { Accordion, AccordionButton, AccordionIcon, AccordionItem, AccordionPanel, Avatar, Box, Heading, Link, Spinner, Text, Tooltip, VStack } from "@chakra-ui/react";
import { useParams } from "react-router-dom";
import { Link as ReactRouterLink } from "react-router-dom";
import { actorPrefix, apiPrefix, baseDomain, mapSexIdentToTxt } from "../config";
import { useFetch } from "../hooks/useFetch";
import { IActorDetails, IActorDetailsResponse } from "../types";
import { ActorRating } from "../components/ActorRating";
import { AwardTable } from "../components/AwardTable";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { SearchableMovieTable } from "../components/SearchableMovieTable";
import { CustomAlert } from "../components/CustomAlert";
import { ArrowBackIcon } from "@chakra-ui/icons";

export function ActorDetails() {
    // Read actor ID from URL path
    const { actorId } = useParams();
    const { isLoading, error, data: actorDetails } = useFetch<IActorDetails | null, IActorDetailsResponse>(
        `${apiPrefix}/actors/${actorId}`,
        null,
        resObj => resObj.data,
        { method: "POST" }
    )

    if (error) return <CustomAlert status="error" alertTitle={error.title} alertDesc={error.desc} />
    if (isLoading) return <LoadingSpinner />
    if (!actorDetails || Object.keys(actorDetails).length === 0) {
        return (
            <CustomAlert
                status="info"
                alertTitle="No data"
                alertDesc={`You might need to trigger webscraping using the button on the top right first or there is no actor with the given ID (=${actorId})!`} />
        )
    }

    return (
        <VStack
            bg={"whiteAlpha.900"}
            boxShadow={"lg"}
            borderRadius={"xl"}
            p={8}
            w={"100%"}>
            <Box display={"flex"} w={"100%"} justifyContent={"flex-start"}>
                <Link as={ReactRouterLink} to={`/actors`}>
                    <ArrowBackIcon
                        boxSize={"25px"}
                        justifySelf={"flex-start"}
                        color={"blue.500"}
                        _hover={{
                            borderRadius: "full",
                            border: "1px  solid",
                        }} />
                </Link>
            </Box>
            <Avatar
                onClick={() => window.open(actorDetails.about.act_img_url, "_blank")?.focus()}
                _hover={{
                    cursor: "pointer"
                }}
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
            <Tooltip label={`Click to show on imdb.com`} placement="right" hasArrow>
                <Link href={`${baseDomain}${actorPrefix}${actorId}`} isExternal _hover={{ textDecoration: "None" }}>
                    <Heading >{actorDetails.about.act_fullname}</Heading>
                </Link>

            </Tooltip>

            <Heading size={"sm"}>{`Rank ${actorDetails.about.act_rank}`}</Heading>
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
                        <SearchableMovieTable key={"top5-movie-table"} data={actorDetails.topFiveMovies} maxH="100%" />
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
                        <SearchableMovieTable key={"movie-table"} data={actorDetails.allTimeMovies} />
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


