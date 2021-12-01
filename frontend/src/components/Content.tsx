import { Container, GridItem, useColorModeValue } from "@chakra-ui/react";
import { Outlet } from "react-router-dom";
import colors from "../colors";

export function Content() {
    const scrollbarColor = useColorModeValue(colors.scrollbarColor.light, colors.scrollbarColor.dark);

    return (
        <GridItem gridArea={"content"} bg={"whiteAlpha.300"}>
            <Container
                h={"100%"}
                maxW={["xs", "2xl", "2xl", "3xl", "4xl"]}
                centerContent
                p={4}
            >
                <Outlet/>
            </Container>
        </GridItem>
    )
}