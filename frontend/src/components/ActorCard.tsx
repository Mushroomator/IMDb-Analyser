import { Avatar, Button, Grid, GridItem, Heading, Link, Text, VStack } from "@chakra-ui/react";
import { Link as ReactRouterLink } from "react-router-dom";
import { mapSexIdentToTxt } from "../config";
import { IActorAbout } from "../types";

/**
 * Card to display info about an actor/ actress
 * @param props Information about an actor 
 * @returns 
 */
export default function ActorCard({ act_href, act_rank, act_fullname, act_sex, act_img_url, act_bio }: IActorAbout) {

    return (
        <Grid
            w={"100%"}
            p={[3, 5]}
            m={[2, 3]}
            gridTemplateAreas={`
                "image content"
                "image footer"
            `}
            gridTemplateColumns={["50px 1fr", "100px 1fr", "150px 1fr"]}
            gridTemplateRows={["auto 1fr"]}
            bg={"whiteAlpha.900"}
            boxShadow={"lg"}
            borderRadius={"xl"}
            transition={"box-shadow 0.2s, transform 0.150s"}
            _hover={{
                transform: "scale(1.01)",
                transition: "box-shadow 0.2s, transform 0.2s",
                boxShadow: "2xl"
            }}>
            <GridItem
                gridArea={"image"}
                display={"flex"}
            >
                <Avatar
                    borderRadius={"full"}
                    src={act_img_url}
                    name={act_fullname}
                    w={"100%"}
                    h={["50px", "100px", "150px"]}
                    alignSelf={"center"}
                    colorScheme={"blue"}
                    showBorder={true}
                    borderColor={"blue.500"} />
            </GridItem>
            <GridItem
                gridArea={"content"}
                pl={2}>
                <VStack h={"100%"} alignItems={"start"} alignContent={"space-around"} p={[2, 4]}>
                    <Heading fontSize={["md", "lg", "xl", "2xl"]}>{act_fullname}</Heading>
                    <Text fontSize={"sm"} fontWeight={"light"}>{`Rank ${act_rank}\t|\t${mapSexIdentToTxt[act_sex]}`}</Text>
                    <Text display={"none"} w={"100%"} fontSize={["sm", "md"]} noOfLines={2}>{act_bio}</Text>
                </VStack>
            </GridItem>
            <GridItem
                gridArea={"footer"}
                display={"flex"}
                w={"100%"}
                justifyContent={"end"}
                pt={[1, 2, 4]}
                pr={[1, 2, 4]}
            >
                <Link as={ReactRouterLink} to={`/actors/${act_href}`}>
                    <Button
                        variant={"outline"}
                        size={"sm"}
                        colorScheme={"blue"}
                    >
                        Details
                    </Button>
                </Link>
            </GridItem>
        </Grid>
    )
}