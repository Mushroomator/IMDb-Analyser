import { Heading, HStack, Image } from "@chakra-ui/react";
import imdbLogo from "../assets/imdb_logo.svg"

export function Home() {

    return (
        <HStack>
            <Heading>Welcome</Heading>
            <Image
                w={"20vh"}
                src={imdbLogo}>

            </Image>
        </HStack>
    )
}