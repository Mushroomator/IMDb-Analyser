import { Container, GridItem } from "@chakra-ui/react";
import { Outlet } from "react-router-dom";

export function Content() {
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