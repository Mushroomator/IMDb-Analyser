import { Heading, HStack, Text, VStack } from "@chakra-ui/react";
import { maxRating } from "../config";

export interface IRating {
    rating: number
}

export function Rating({ rating }: IRating) {
    return (
        <VStack
            justifyContent={"center"}
            h={"100%"}
            flexBasis={"100%"}
            w={"100%"}>
            <Heading size={"md"}>Overall Rating</Heading>
            <HStack alignItems={"baseline"} w={"100%"} justifyContent={"center"}>
                <Text fontSize={"4xl"} fontWeight={"bold"}>
                    {rating}
                </Text>
                <Text fontSize={"md"} fontWeight={"light"}>
                    /{maxRating}
                </Text>

            </HStack>
        </VStack>
    )
}