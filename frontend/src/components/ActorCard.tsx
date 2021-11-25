import { Avatar, Button, Grid, GridItem, Heading, scaleFadeConfig, Text, transition, VStack } from "@chakra-ui/react";
import { transform } from "typescript";
import { IActor } from "../types";

export interface IActorCard {
    actor: IActor
}

export default function ActorCard({ actor }: IActorCard) {
    const fullName = `${actor.firstName} ${actor.lastName}`;
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
            }}
            // border={"1px"}
            // borderColor={"gray.100"}
            
            >
            <GridItem
                gridArea={"image"}
                display={"flex"}
                >
                <Avatar borderRadius={"full"} src={actor.img} name={fullName} w={"100%"} h={["50px", "100px", "150px"]} alignSelf={"center"} colorScheme={"blue"} showBorder={true} borderColor={"blue.500"}/>
            </GridItem>
            <GridItem
                gridArea={"content"}
                pl={2}>
                <VStack h={"100%"} alignItems={"start"} alignContent={"space-around"} p={[2, 4]}>
                    <Heading fontSize={["md", "lg", "xl", "2xl"]}>{fullName}</Heading>
                    <Text fontSize={"sm"} fontWeight={"light"}>{actor.sex}</Text>
                    <Text display={"none"} w={"100%"} fontSize={["sm", "md"]} noOfLines={2}>{actor.bio}</Text>
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
                <Button variant={"outline"} size={"sm"} colorScheme={"blue"}>Details</Button>
            </GridItem>
        </Grid>
    )
}