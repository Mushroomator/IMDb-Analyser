import { Container, GridItem, useColorModeValue } from "@chakra-ui/react";
import colors from "../colors";

export interface IContent {
    children: React.ReactNode
}

export function Content({children}: IContent) {
    const scrollbarColor = useColorModeValue(colors.scrollbarColor.light, colors.scrollbarColor.dark);

    return (
        <GridItem gridArea={"content"} bg={"whiteAlpha.300"}>
            <Container
                h={"100%"}
                maxW={["xs", "2xl", "2xl", "3xl", "4xl"]}
                centerContent
            >
                {children}
            </Container>
        </GridItem>
    )
}