import { DeleteIcon, DownloadIcon, RepeatClockIcon } from "@chakra-ui/icons";
import { Button, Grid, GridItem, Heading, HStack, IconButton, Image, Link, Tooltip, useDisclosure } from "@chakra-ui/react";
import { LegacyRef, useCallback, useRef } from "react";
import { Link as ReactRouterLink } from "react-router-dom";
import logo from "../assets/logo.png";
import { DatabaseDeletionModal } from "./modals/DatabaseDeletionModal";
import { WebscrapingModal } from "./modals/WebscrapingModal";

export function Header() {
    const { isOpen: isOpenConfirmDeletion, onOpen: onOpenConfirmDeletion, onClose: onCloseConfirmDeletion } = useDisclosure()
    const { isOpen: isOpenWebscrape, onOpen: onOpenWebscrape, onClose: onCloseWebscrape } = useDisclosure()
    const focusRef = useRef(null)



    return (
        <GridItem position={"sticky"} top={0} zIndex={"sticky"} maxH={"100%"} h={"100%"} w={"100%"} bg={"white"} gridArea={"header"} borderBottom={"1px"} borderColor={"gray.200"}>
            <Grid
                w={"100%"}
                h={"100%"}
                gridTemplateAreas={
                    [
                        `"left middle middle"`,
                        `"left middle right"`
                    ]}
                gridTemplateRows={"100%"}
                gridTemplateColumns={["60px 1fr 130px", null, null, "300px 1fr 150px"]}
            >
                <GridItem
                    gridArea={"left"}
                >
                    <HStack h={"100%"} maxH={"100%"} alignItems={"center"} justifyContent={"start"} w={"100%"}>
                        <Image ref={focusRef} objectFit={"contain"} p={3} h={"100%"} maxW={"auto"} maxH={"100%"} src={logo} alt="IMDb Analyser Logo" justifySelf={"start"} />
                        <Heading colorScheme={"blue"} display={["none", null, null, "block"]} size={"md"} justifyContent={"start"}>IMDb Analyser</Heading>
                    </HStack>
                </GridItem>
                <GridItem
                    gridArea={"middle"}
                    w={"100%"}
                    h={"100%"}
                    display={"flex"}
                    alignItems={"center"}
                    justifyContent={"center"}>
                    <HStack
                        spacing={[0, null, 5]}
                        h={"100%"}
                        w={"100%"}
                        justifyItems={"start"}
                        alignContent={"center"}
                        justifyContent={"flex-start"}>
                        <Link
                            as={ReactRouterLink}
                            to={"/"}
                            _hover={{ textDecoration: "none" }}

                        >
                            <Button
                                fontSize={"md"}
                                variant={"ghost"}
                                colorScheme={"blue"}
                                _hover={{
                                    outline: "1px solid var(--chakra-colors-blue-500)"
                                }}>
                                Home
                            </Button>
                        </Link>
                        <Link
                            as={ReactRouterLink}
                            to={"/actors"}
                            _hover={{ textDecoration: "none" }}>
                            <Button
                                fontSize={"md"}
                                variant={"ghost"}
                                colorScheme={"blue"}
                                _hover={{
                                    outline: "1px solid var(--chakra-colors-blue-500)"
                                }}>Actors</Button>
                        </Link>
                        <Link
                            as={ReactRouterLink}
                            to={"/movies"}
                            _hover={{ textDecoration: "none" }}

                        >
                            <Button
                                fontSize={"md"}
                                variant={"ghost"}
                                colorScheme={"blue"}
                                _hover={{
                                    outline: "1px solid var(--chakra-colors-blue-500)"
                                }}>
                                Movies
                            </Button>
                        </Link>
                    </HStack>
                </GridItem>
                <GridItem
                    gridArea={"right"}
                    w={"100%"}
                    h={"100%"}
                    display={"flex"}
                    alignItems={"end"}
                >
                    <HStack h={"100%"} w={"100%"} spacing={4} alignContent={"center"} justifyContent={"flex-end"} px={5}>
                        <Tooltip
                            label={"Reload page"}
                            colorScheme={"blue"}
                            aria-label={"Reload page"}
                            hasArrow
                        >
                            <IconButton
                                aria-label="Reload page"
                                icon={<RepeatClockIcon />}
                                colorScheme={"blue"}
                                variant={"outline"}
                                onClick={() => window.location.reload()}
                            >

                            </IconButton>
                        </Tooltip>
                        <Tooltip
                            label={"Web scrape & insert"}
                            colorScheme={"blue"}
                            aria-label={"Web scrape & insert"}
                            hasArrow
                        >
                            <IconButton
                                aria-label="Start web scraping and fill database with content"
                                icon={<DownloadIcon />}
                                colorScheme={"blue"}
                                variant={"outline"}
                                onClick={onOpenWebscrape}
                            >

                            </IconButton>
                        </Tooltip>
                        <Tooltip
                            label={"Delete database content"}
                            colorScheme={"blue"}
                            aria-label="Delete database content"
                            hasArrow
                        >
                            <IconButton
                                aria-label="Delete database content"
                                icon={<DeleteIcon />}
                                variant={"outline"}
                                colorScheme={"blue"}
                                onClick={onOpenConfirmDeletion}>
                            </IconButton>
                        </Tooltip>
                    </HStack>
                </GridItem>
            </Grid>
            <DatabaseDeletionModal finalFocusRef={focusRef} isOpen={isOpenConfirmDeletion} onClose={onCloseConfirmDeletion} />
            <WebscrapingModal finalFocusRef={focusRef} isOpen={isOpenWebscrape} onClose={onCloseWebscrape} />

        </GridItem>
    )
}