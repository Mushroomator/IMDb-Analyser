import { Avatar, Heading, HStack, Image, SimpleGrid, Text, VStack } from "@chakra-ui/react";
import eitLogo from "../assets/eit_logo_large_2016.png"
import othLogo from "../assets/OTH_logo_cut_off.png"
import { authorDetails } from "../config";
import { CustomLabel } from "./CustomLabel";

export function Home() {
    const fullname = `${authorDetails.firstName} ${authorDetails.lastName}`;


    return (
        <VStack
            w={"100%"}
            bg={"whiteAlpha.900"}
            boxShadow={"lg"}
            borderRadius={"xl"}
            p={8}>
            <Avatar
                color={"white"}
                fontWeight={"bold"}
                fontSize={"5xl"}
                bg={"blue.500"}
                borderRadius={"full"}
                src={authorDetails.img}
                name={fullname}
                w={["50px", "100px", "150px"]}
                h={["50px", "100px", "150px"]}
                alignSelf={"center"}
                colorScheme={"blue"}
                showBorder={true}
                borderColor={"blue.500"} />
            <Heading>{fullname}</Heading>
            <Text>Assignment</Text>
            <SimpleGrid
                columns={2}
                spacing={5}
                autoColumns={"min-content"}
                gridTemplateColumns={"100px 1fr"}
                justifyContent={"center"}
                p={"10"}>
                <CustomLabel>Course</CustomLabel>
                <Text>Applied Data Science with Python</Text>
                <CustomLabel>Student-ID</CustomLabel>
                <Text>3180640</Text>
                <CustomLabel>Institution</CustomLabel>
                <Text>OTH Regensburg, DE</Text>
                <CustomLabel>Lecturer</CustomLabel>
                <Text>Istvan Lengyel, Eastern Institute of Technology, NZ</Text>
                <CustomLabel>Project</CustomLabel>
                <Text>Project 2: Database of Hollywood Actors and Actresses</Text>
                <CustomLabel>Date</CustomLabel>
                <Text>14/01/2022</Text>
            </SimpleGrid>
            {/* <HStack>
                <Link href="https://imdb.com" isExternal>
                    <Image
                        h={"4rem"}
                        src={imdbLogo}
                        display={"inline"} />
                </Link>
                <Heading fontSize={"2rem"} display={"inline"}>Analyser</Heading>
            </HStack> */}
            <HStack w={"100%"} justifyContent={"space-evenly"} p={15}>
                <Image src={eitLogo} w={"30%"} h={"75px"} objectFit={"contain"} />
                <Image src={othLogo} w={"30%"} h={"75px"} objectFit={"contain"} />
            </HStack>
        </VStack>
    )
}